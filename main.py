import sys
import os

from module import alert_excepthook, hide_console
from PyQt5.QtWidgets import QApplication

from events import Events
from GUI.images import icons
from GUI.qss import DEFAULT
from cache import Cache


class Main(Events):
    def __init__(self):
        super().__init__()
        self.txe_code.setUndoRedoEnabled(True)
        self.line_number.append("  1")
        self.txe_code.verticalScrollBar().valueChanged.connect(self.line_number.verticalScrollBar().setValue)
        self.splitter.setSizes([300, 0])
        self.__cache = Cache("data", ".ConvertPython")
        self.__cache.setup(("file", lambda: self._file, self._set_file, ""))
        self.__cache.load()
        if len(sys.argv) > 1:
            if os.path.isfile(sys.argv[1]) and os.path.splitext(os.path.basename(sys.argv[1]))[-1] == ".pycvt":
                self._set_file(sys.argv[1])
            else:
                self._set_file("")
        self.show()

    def closeEvent(self, event):
        self.__cache.update()
        super().closeEvent(event)

    def focus_changed(self, focus):
        app.blockSignals(True)
        if self.isActiveWindow():
            self._load_file()
        app.blockSignals(False)


if __name__ == "__main__":
    alert_excepthook()
    app = QApplication(sys.argv)
    window = Main()
    window.setStyleSheet(DEFAULT)
    app.focusWindowChanged.connect(window.focus_changed)
    hide_console()
    sys.exit(app.exec_())
