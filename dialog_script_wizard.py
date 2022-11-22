import os
import re
import subprocess
from app import App

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog, QListWidget
from PyQt5.QtCore import pyqtSignal

from GUI.customs import TitleBar


def detect_pathex(compiler: str, library: str):
    SCRIPT_FILE = App.path.source.join("detect_pathex.pyw")
    with open(SCRIPT_FILE, mode="w") as f:
        f.write(f"""import os
import {library}

print(os.path.dirname(os.path.normpath({library}.__file__)))""")
    p = subprocess.Popen(f"{compiler} {SCRIPT_FILE}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    o, e = p.communicate()
    if e:
        return False, e.decode().split("\r\n")[-2]
    return True, o.decode().split("\r\n")[-2]


class DialogScriptWizard(QDialog):
    finish_signal = pyqtSignal(str)
    empty_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        loadUi(App.path.source.join("GUI", "ui", "dialog.ui"), self)
        TitleBar.setup(self, self.frame, self.frame_28, self.btn_min, None, self.btn_close, self.frame_29, None, self.frame_30)
        self.setModal(True)
        self._pages = [self.page_start, self.page_setup, self.page_data, self.page_pathex]
        self._titles = ["Choose an option", "Setup", "Add data", "Pathex"]
        self._index = 0

        self.btn_cancel.clicked.connect(self.close)
        self.btn_create_empty.clicked.connect(self._on_btn_create_empty_clicked)
        self.btn_using_wizard.clicked.connect(self._on_btn_next_clicked)
        self.btn_back.clicked.connect(self._on_btn_back_clicked)
        self.btn_next.clicked.connect(self._on_btn_next_clicked)
        self.btn_next.hide()
        self.btn_back.hide()
        self._update_page()

        self.line_converter.setFormat("file", ("Executable file", ".exe",), self.btn_path_1, self.label_msg_converter)
        self.line_input.setFormat("file", ("Python file", ".py", ".pyw"), self.btn_path_2, self.label_msg_input, name="Input File")
        self.line_output.setFormat("dir", button=self.btn_path_3, label_msg=self.label_msg_output, name="Output Directory")
        self.line_icon.setFormat("file", ("Icon file", ".ico"), self.btn_path_4, self.label_msg_icon, name="Icon File Path")
        self.line_venv.setFormat("dir", button=self.btn_path_5, label_msg=self.label_9, name="Venv Directory")

        self.cbb_icon.currentIndexChanged.connect(self._on_cbb_icon_changed)
        self._on_cbb_icon_changed(0)

        self.btn_tool_pathex.clicked.connect(self._on_btn_tool_clicked)
        self.frame_20.hide()
        self.label_9.hide()

        self.label_msg_converter.hide()
        self.label_msg_app_name.hide()
        self.label_msg_input.hide()
        self.label_msg_output.hide()
        self.label_msg_icon.hide()

        self.cb_one_file.setChecked(True)
        self.cb_no_console.setChecked(False)
        self.cb_uac_admin.setChecked(False)

        self.list_file_add.setFormat("file", self.btn_add_file, self.btn_rm_file, self.btn_rm_all_file)
        self.list_dir_add.setFormat("dir", self.btn_add_dir, self.btn_rm_dir, self.btn_rm_all_dir)
        self.list_pathex.setFormat("dir", self.btn_add_pathex, self.btn_rm_pathex)

        self.btn_detect_add.clicked.connect(self._on_btn_detect_add_clicked)

        self.line_input.textChanged.connect(self._on_line_input_text_changed)

    def _on_btn_create_empty_clicked(self):
        self.empty_signal.emit()
        self.close()

    def _on_line_input_text_changed(self):
        if self.line_input.valueIsValid():
            if not self.line_name.text():
                self.line_name.setText(os.path.splitext(os.path.basename(self.line_input.text()))[0])

    def _on_btn_detect_add_clicked(self):
        venv = self.line_venv.text()
        lib = self.line_name_lib.text()
        if lib:
            success, out = detect_pathex("python.exe" if not venv else os.path.join(os.path.normpath(venv), "Scripts", "python.exe"), lib)
            if success:
                self.list_pathex.addItem(out)
                if not self.label_9.isHidden():
                    self.label_9.hide()
            else:
                self.label_9.setText(out)
                if self.label_9.isHidden():
                    self.label_9.show()
        else:
            self.label_9.setText("Library name must not be empty")
            if self.label_9.isHidden():
                self.label_9.show()

    def _on_btn_add_file_clicked(self):
        p = QFileDialog.getOpenFileNames(self, "Select files add", "", "All file (*.*)")[0]
        if p:
            self.list_file_add.append()

    def _on_cbb_icon_changed(self, idx):
        if self.cbb_icon.currentText() == "Custom":
            self.line_icon.show()
            self.btn_path_4.show()
        else:
            if not self.line_icon.isHidden():
                self.line_icon.hide()
                self.btn_path_4.hide()

    def __input_setup_valid(self):
        valid = True
        if not self.line_name.text():
            self.label_msg_app_name.setText("Application Name must not be empty")
            if self.label_msg_app_name.isHidden():
                self.label_msg_app_name.show()
        elif re.search(r'[\\/:*?"<>]', self.line_name.text()):
            self.label_msg_app_name.setText("A file name can't contain any of the following characters: \\ / : * ? \" < > |")
            if self.label_msg_app_name.isHidden():
                self.label_msg_app_name.show()
            valid = False
        else:
            if not self.label_msg_app_name.isHidden():
                self.label_msg_app_name.hide()
        list_check_valid = [
            self.line_converter.valueIsValid(required=False),
            self.line_input.valueIsValid(),
            self.line_output.valueIsValid(),
            self.line_icon.valueIsValid()
        ]
        valid = all(list_check_valid)
        return valid

    def _on_btn_next_clicked(self):
        if self._index == 1 and not self.__input_setup_valid():
            return
        self._index += 1
        self._update_page()

    def _on_btn_back_clicked(self):
        self._index -= 1
        self._update_page()

    def _update_page(self):
        if self._index > 0 and self.btn_next.isHidden() and self.btn_back.isHidden():
            self.btn_next.show()
            self.btn_back.show()
        elif self._index >= len(self._pages):
            self.finish_signal.emit(self.__create_code())
            return self.close()
        elif self._index == len(self._pages) - 1:
            self.btn_next.setText("Finish")
        elif self._index == 0:
            self.btn_next.hide()
            self.btn_back.hide()
        elif self._index < len(self._pages) - 1 and self.btn_next.text() == "Finish":
            self.btn_next.setText("Next")
        self.setWindowTitle(self._titles[self._index])
        self.label_8.setText(self._titles[self._index])
        self.stackedWidget.setCurrentWidget(self._pages[self._index])

    def _on_btn_tool_clicked(self):
        if self.frame_20.isHidden():
            self.frame_20.show()
        else:
            self.frame_20.hide()

    def __create_code(self):
        option = ""
        if self.cb_one_file.isChecked():
            option += "one-file\n"
        if self.cb_no_console.isChecked():
            option += "no-console\n"
        if self.cb_uac_admin.isChecked():
            option += "uac-admin\n"
        data = '\n'.join([f'Source {os.path.normpath(item)} DestDir .' for item in self.list_file_add.listText()]
                + [f'Source {os.path.normpath(item)} DestDir {os.path.basename(item)}' for item in self.list_dir_add.listText()])
        pathex = '\n'.join([f'Source {os.path.normpath(item)}' for item in self.list_pathex.listText()])
        code = f"""[Setup]
Converter = {os.path.normpath(self.line_converter.text()) if self.line_converter.text() else "PyInstaller"}
AppName = "{self.line_name.text()}"
InputFile = {os.path.normpath(self.line_input.text())}
OutputDir = {os.path.normpath(self.line_output.text())}
Icon = {os.path.normpath(self.line_icon.text()) if self.cbb_icon.currentText() == "Custom" else self.cbb_icon.currentText()}

[Option]
{option}
[Data]
{data}

[Pathex]
{pathex}"""
        return code
