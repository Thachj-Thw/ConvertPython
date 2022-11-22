from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction, QMenu

from app import App


class Menu(App):
    def __init__(self):
        super().__init__()

        def create_menu(*args):
            menu = QMenu(self)
            for arg in args:
                if isinstance(arg, str):
                    if arg == "separator":
                        menu.addSeparator()
                    else:
                        menu.addAction(arg)
                else:
                    action = QAction((arg[0]), self)
                    if arg[1]:
                        action.setShortcut(QKeySequence(arg[1]))
                    menu.addAction(action)
                    if arg[2]:
                        action.triggered.connect(arg[2])
                    self.addAction(action)
            return menu

        self._menu_file = create_menu(
            ("New File", "ctrl+N", self._on_new),
            ("Open File...", "ctrl+O", self._on_open),
            "separator",
            ("Save", "ctrl+S", self._on_save),
            ("Save as", "ctrl+shift+S", self._on_save_as),
            "separator",
            ("Exit", "", self.close))

        self._menu_edit = create_menu(
            ("Undo", "ctrl+Z", self.txe_code.undo),
            ("Redo", "ctrl+shift+z", self.txe_code.redo),
            "separator",
            ("Cut", "ctrl+X", self.txe_code.cut),
            ("Copy", "ctrl+C", self.txe_code.copy),
            ("Paste", "ctrl+V", self.txe_code.paste))

        self._menu_run = create_menu(
            ("Start convert", "F10", self._on_run),
            ("Stop convert", "F11", self._on_stop))

        self._menu_help = create_menu(
            ("Document", "", self._on_open_document),
            ("About", "", self._on_about))

        self.menu_file.clicked.connect(lambda: self._menu_file.exec_(
            self.menu_file.mapToGlobal(self.menu_file.pos()) + QPoint(0, self.menu_file.height())))
        self.menu_edit.clicked.connect(lambda: self._menu_edit.exec_(
            self.menu_edit.mapToGlobal(self.menu_file.pos()) + QPoint(0, self.menu_edit.height())))
        self.menu_run.clicked.connect(lambda: self._menu_run.exec_(
            self.menu_run.mapToGlobal(self.menu_file.pos()) + QPoint(0, self.menu_run.height())))
        self.menu_help.clicked.connect(lambda: self._menu_help.exec_(
            self.menu_help.mapToGlobal(self.menu_file.pos()) + QPoint(0, self.menu_help.height())))
