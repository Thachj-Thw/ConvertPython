import os
import re

from PyQt5.QtWidgets import QFileDialog
from dialog_script_wizard import DialogScriptWizard

from menu import Menu
from run import Run


class Events(Menu, Run):
    def __init__(self):
        super().__init__()
        self.btn_new.clicked.connect(self._on_new)
        self.btn_open.clicked.connect(self._on_open)
        self.btn_save.clicked.connect(self._on_save)
        self.btn_run.clicked.connect(self._on_run)
        self.btn_stop.clicked.connect(self._on_stop)

        self.txe_code.textChanged.connect(self._on_code_changed)
        self.txe_code.start_convert.triggered.connect(self._on_run)
        self.txe_code.stop_convert.triggered.connect(self._on_stop)
        self.txe_code.switch_to_relative_path.triggered.connect(self._on_switch_to_relative_path)
        self.txe_code.switch_to_absolute_path.triggered.connect(self._on_switch_to_absolute_path)
        self.btn_clear.clicked.connect(self.txe_out.clear)
        self.__dialog = None

    def _on_switch_to_absolute_path(self):
        if not self._file:
            if self._question_message("You must save the file first"):
                self._on_save()
        if self._file:
            code = self.txe_code.toPlainText()
            new_code = re.sub(re.escape("*ThisDir*"), re.escape(os.path.dirname(os.path.normpath(self._file))), code)
            self._show_code(new_code)

    def _on_switch_to_relative_path(self):
        if not self._file:
            if self._question_message("You must save the file"):
                self._on_save()
        if self._file:
            code = self.txe_code.toPlainText()
            new_code = re.sub(re.escape(os.path.dirname(os.path.normpath(self._file))), "*ThisDir*", code)
            self._show_code(new_code)

    def _on_run(self):
        if not self.txe_code.toPlainText():
            return self._error_message("Code is empty!")
        self.splitter.setSizes([300, 170])
        self._start_convert()

    def _on_stop(self):
        self._stop_convert()

    def _on_new(self):
        if self._file_data() != self.txe_code.toPlainText():
            if self._question_message("Do you want to save changes?"):
                self._save_file()
        self.__dialog = DialogScriptWizard(self)
        self.__dialog.finish_signal.connect(self._on_create_finished)
        self.__dialog.empty_signal.connect(self._on_create_empty)
        self.__dialog.show()

    def _on_create_finished(self, code):
        self._set_file("")
        self.txe_code.setPlainText(code)

    def _on_create_empty(self):
        self._set_file("")
        self.txe_code.setPlainText("")

    def _on_open(self):
        if self._file_data() != self.txe_code.toPlainText():
            if self._question_message("Do you want to save changes?"):
                self._save_file()
        _path = QFileDialog.getOpenFileName(self, "Choose a python convert file", "", "Python Convert File (*.pycvt)")[0]
        if _path:
            self._set_file(_path)
            self._load_file()

    def _on_save(self):
        if not self._file:
            _path = QFileDialog.getSaveFileName(self, "Save", "", "Python Convert (*.pycvt)")[0]
            if _path:
                if os.path.splitext(os.path.basename(_path))[1] != ".pycvt":
                    _path += ".pycvt"
                self._set_file(_path)
            else:
                return
        self._save_file()

    def _on_save_as(self):
        _path = QFileDialog.getSaveFileName(self, "Save", "", "Python Convert (*.pycvt)")[0]
        if _path:
            if os.path.splitext(os.path.basename(_path))[1] != ".pycvt":
                _path += ".pycvt"
            self._set_file(_path)
            self._save_file()

    def _on_open_document(self):
        pass

    def _on_about(self):
        pass

    def closeEvent(self, event):
        if self._is_converting():
            if self._question_message("Converting! Do you want to stop?"):
                self._stop_convert()
            else:
                event.ignore()
                return super().closeEvent(event)
        if self._file_data() != self.txe_code.toPlainText():
            if self._question_message("Do you want to save changes?"):
                self._on_save()
        event.accept()
        return super().closeEvent(event)

    def _on_code_changed(self):
        self._show_code(self.txe_code.toPlainText())
