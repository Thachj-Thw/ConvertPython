import os

from module import Path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi

import text_editor
from GUI.customs import TitleBar


class App(QMainWindow):
    __version__ = "1.0"
    path = Path(__file__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        loadUi(App.path.source.join("GUI", "ui", "index.ui"), self)
        self.setWindowTitle("Convert Python " + App.__version__)
        icon = self.path.source.join("GUI", "Images", "Logo", "logoPython.png")
        self.setWindowIcon(QIcon(icon))
        pixmap = QPixmap()
        pixmap.load(icon)
        self.label.setPixmap(pixmap.scaled(self.label.width()//2, self.label.height()//2, Qt.AspectRatioMode.KeepAspectRatio))
        TitleBar.setup(self, frame_move=self.frame_5, btn_minimize=self.btn_min, btn_maximize=self.btn_max,
                       btn_close=self.btn_close, size_grip=self.frame_8)
        self._file = ""

    def _set_file(self, path):
        self._file = os.path.normpath(path) if path else ""
        if self._file:
            self.label_2.setText(self._file + " - Convert Python " + App.__version__)
        else:
            self.label_2.setText("Untitled - Convert Python " + App.__version__)

    def _file_data(self):
        if os.path.isfile(self._file):
            with open(self._file, "r", encoding='utf-8') as f:
                data = f.read()
            return data
        return ""

    def _load_file(self):
        if self._file:
            code = self._file_data()
            if code:
                self.txe_code.setPlainText(code)
            else:
                if self._question_message(f'File path "{self._file}" not existed!\n Do you want to save as it?'):
                    self._save_file()

    def _save_file(self):
        if self._file:
            with open(self._file, mode="w", encoding="utf-8") as f:
                f.write(self.txe_code.toPlainText())

    def test(self):
        cursor = QTextCursor(self.txe_code.document())
        cursor.beginEditBlock()
        position = self.txe_code.textCursor().position()
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.insertHtml("Test")
        cursor.setPosition(position)
        self.txe_code.setTextCursor(cursor)
        cursor.endEditBlock()

    def _show_code(self, code):
        self.txe_code.blockSignals(True)
        cursor = QTextCursor(self.txe_code.document())
        cursor.beginEditBlock()
        position = self.txe_code.textCursor().position()
        line = code.split('\n')
        self.line_number.setPlainText("\n".join("  "+str(i) for i in range(1, len(line) + 1)))
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.insertHtml(text_editor.highlight(code))
        cursor.setPosition(position)
        self.txe_code.setTextCursor(cursor)
        cursor.endEditBlock()
        self.txe_code.blockSignals(False)

    def _logs(self, logs: str):
        if "Error, " in logs:
            self.txe_out.insertHtml(f'<span style="font-size: 13px; font-weight: 400; color: #cf2727; font-style: normal; white-space: pre-wrap;">{logs}\n</span>')
        elif "WARNING" in logs:
            self.txe_out.insertHtml(f'<span style="font-size: 13px; font-weight: 400; color: #cfb027; font-style: normal; white-space: pre-wrap;">{logs}\n</span>')
        else:
            self.txe_out.insertHtml(f'<span style="white-space: pre-wrap;">{logs}\n</span>')
        if "Building EXE from EXE-00.toc completed successfully" in logs:
            self.txe_out.insertHtml(f'<span style="font-size: 13px; font-weight: 400; color: #27cf57; font-style: normal; white-space: pre-wrap;">SUCCESSFULLY\n</span>')
        cursor = self.txe_out.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.txe_out.setTextCursor(cursor)

    Button = QMessageBox.StandardButton
    Icon = QMessageBox.Icon

    def _messagebox(self, icon, title, message, buttons):
        return QMessageBox(icon, title, message, buttons).exec_()

    def _warning_message(self, message):
        self._messagebox(App.Icon.Warning, "Convert Python Warning", message, App.Button.Ok | App.Button.Cancel)

    def _error_message(self, message):
        self._messagebox(App.Icon.Critical, "Convert Python Error", message, App.Button.Ok | App.Button.Cancel)

    def _question_message(self, message):
        return self._messagebox(App.Icon.Question, "Convert Python Question", message, App.Button.Yes | App.Button.No) == App.Button.Yes

    def _alert(self, message):
        self._messagebox(App.Icon.Information, "Convert Python Alert", message, App.Button.Ok | App.Button.Cancel)
