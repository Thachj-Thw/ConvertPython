import os

from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5.QtGui import QColor, QTextCursor
from PyQt5.QtWidgets import (QMainWindow, QSizeGrip, QFrame, QPushButton, QGraphicsDropShadowEffect,
                             QLayout, QLineEdit, QFileDialog, QListWidget, QLabel, QTextEdit, QMenu,
                             QAction)


class TitleBar(QMainWindow):

    def maximize_restore(self):
        if self._max.isChecked():
            self.showMaximized()
            if self._l_shadow:
                self._l_shadow.setContentsMargins(0, 0, 0, 0)
            if self._main:
                self._main.setStyleSheet("QFrame#main{border-radius: 0px;}")
            self._max.setToolTip("Restore Down")
        else:
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            if self._l_shadow:
                self._l_shadow.setContentsMargins(9, 9, 9, 9)
            if self._main:
                self._main.setStyleSheet("")
            self._max.setToolTip("Maximize")

    def update_pos(self, pos):
        self._drag_pos = pos

    def setup(
        self,
        frame_main: QFrame = None,
        frame_move: QFrame = None,
        btn_minimize: QPushButton = None,
        btn_maximize: QPushButton = None,
        btn_close: QPushButton = None,
        frame_btns: QFrame = None,
        layout_shadow: QLayout = None,
        size_grip: QFrame = None,
    ):
        self._main = frame_main
        self._move = frame_move
        self._min = btn_minimize
        self._max = btn_maximize
        self._close = btn_close
        self._f_btns = frame_btns
        self._l_shadow = layout_shadow
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        if self._main:
            self._main.setGraphicsEffect(
                QGraphicsDropShadowEffect(blurRadius=15, offset=QPoint(3, 3), color=QColor("#000")))

        if self._min:
            self._min.clicked.connect(lambda: self.showMinimized())
            self._min.setToolTip("Minimize")

        if self._max:
            self._max.setCheckable(True)
            self._max.clicked.connect(lambda: TitleBar.maximize_restore(self))
            self._max.setToolTip("Maximize")

        if self._close:
            self._close.clicked.connect(lambda: self.close())
            self._close.setToolTip("Close")

        def move_window(event):
            if event.buttons() == Qt.LeftButton:
                if self._max:
                    if self._max.isChecked():
                        self._max.setChecked(False)
                        ratio = event.x() / self.width()
                        TitleBar.maximize_restore(self)
                        w = self._f_btns.width() if self._f_btns else 0
                        x = min(self.width() - w, ratio * self.width())
                        self.move(event.globalPos() - QPoint(x, event.y() + 9 if self._l_shadow else event.y()))
                if hasattr(self, "_drag_pos"):
                    self.move(self.pos() + event.globalPos() - self._drag_pos)
                    self._drag_pos = event.globalPos()
                    event.accept()
                else:
                    event.ignore()

        def release_window(event):
            if self._max:
                if self.y() + event.y() <= 0 and not self._max.isChecked():
                    self._max.setChecked(True)
                    TitleBar.maximize_restore(self)

        if self._move:
            self._move.mouseMoveEvent = move_window
            self._move.mouseReleaseEvent = release_window
        self.mousePressEvent = lambda event: TitleBar.update_pos(self, event.globalPos())
        if size_grip:
            QSizeGrip(size_grip)



class LineEditDragDrop(QLineEdit):

    class Format(object):
        ALL = "all"
        DIR = "dir"
        FILE = "file"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.format = "all"
        self.tail = tuple()
        self.ftype = ""
        self.button = None
        self.label_msg = None
        self.name = ""

    def setFormat(self, new_format, tail=tuple(), button=None, label_msg=None, name=""):
        self.format = new_format
        self.name = name
        if tail:
            self.tail = tail[1:]
            self.ftype = tail[0]
        if isinstance(button, QPushButton):
            self.button = button
            self.button.clicked.connect(self._on_button_clicked)
        if isinstance(label_msg, QLabel):
            self.label_msg = label_msg

    def valueIsValid(self, alert=True, required=True):
        if not self.isHidden():
            if required and not self.text():
                if alert:
                    self.__alert(self.name + " must not be empty")
                return False
            elif self.format == "file":
                if not os.path.isfile(self.text()) and os.path.splitext(os.path.basename(self.text()))[-1] in self.tail:
                    if alert:
                        self._alert("Invalid value")
                    return False
            elif self.format == "dir":
                if not os.path.isdir(self.text()):
                    if alert:
                        self._alert("Invalid value")
                    return False
        return True

    def __alert(self, msg):
        if self.label_msg:
            if msg:
                self.label_msg.setText(msg)
                if self.label_msg.isHidden():
                    self.label_msg.show()
            else:
                if not self.label_msg.isHidden():
                    self.label_msg.hide()

    def _on_button_clicked(self):
        if self.format == "file":
            p = QFileDialog.getOpenFileName(self, "Choose a file", "", self.ftype + " (*" + " *".join(self.tail) + ")" if self.tail else "All file (*.*)")[0]
            if p:
                self.setText(p)
        elif self.format == "dir":
            p = QFileDialog.getExistingDirectory(self, "Choose a directory")
            if p:
                self.setText(p)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            if url := event.mimeData().urls():
                if url[0].isLocalFile():
                    if self.format == "all":
                        event.setDropAction(Qt.CopyAction)
                        return event.accept()
                    if self.format == "dir":
                        if os.path.isdir(url[0].toLocalFile()):
                            event.setDropAction(Qt.CopyAction)
                            return event.accept()
                    elif self.format == "file":
                        f = url[0].toLocalFile()
                        if os.path.isfile(f):
                            if os.path.splitext(os.path.basename(f))[-1] in self.tail:
                                event.setDropAction(Qt.CopyAction)
                                return event.accept()
        event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            self.setText(event.mimeData().urls()[0].toLocalFile())
        else:
            event.ignore()


class ListWidgetDragDrop(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.format = "all"
        self.tail = tuple()
        self.ftype = ""
        self.button_add = None
        self.button_rm = None
        self.button_rm_all = None
        # self.setSelectionModel()

    def setFormat(self, new_format, button_add=None, button_rm=None, button_rm_all=None, tail=tuple()):
        self.format = new_format
        if tail:
            self.tail = tail[1:]
            self.ftype = tail[0]
        if isinstance(button_add, QPushButton):
            self.button_add = button_add
            self.button_add.clicked.connect(self._on_button_add_clicked)
        if isinstance(button_rm, QPushButton):
            self.button_rm = button_rm
            self.button_rm.clicked.connect(lambda: self.takeItem(self.currentRow()))
        if isinstance(button_rm_all, QPushButton):
            self.button_rm_all = button_rm_all
            self.button_rm_all.clicked.connect(self.clear)

    def _on_button_add_clicked(self):
        if self.format == "dir":
            ps = QFileDialog.getExistingDirectory(self, "Choose a folders")
            if ps:
                self.addItem(ps)
        elif self.format == "file":
            ps = QFileDialog.getOpenFileNames(self, "Select files", "", self.ftype + " (*" + " *".join(self.tail) + ")" if self.tail else "All file (*.*)")[0]
            if ps:
                self.addItems(ps)

    def listItems(self):
        return [self.item(i) for i in range(self.count())]

    def listText(self):
        return [self.item(i).text() for i in range(self.count())]

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
             urls = event.mimeData().urls()
             for url in urls:
                if url.isLocalFile():
                    if self.format == "all":
                        event.setDropAction(Qt.CopyAction)
                        return event.accept()
                    if self.format == "dir":
                        if os.path.isdir(url.toLocalFile()):
                            event.setDropAction(Qt.CopyAction)
                            return event.accept()
                    elif self.format == "file":
                        f = url.toLocalFile()
                        if os.path.isfile(f):
                            if not self.tail:
                                event.setDropAction(Qt.CopyAction)
                                return event.accept()
                            if os.path.splitext(os.path.basename(f))[-1] in self.tail:
                                event.setDropAction(Qt.CopyAction)
                                return event.accept()
        event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if self.format == "all":
                for url in event.mimeData().urls():
                    if url.isLocalFile():
                        self.addItem(os.path.normpath(url.toLocalFile()))
            if self.format == "file":
                for url in event.mimeData().urls():
                    if url.isLocalFile():
                        p = os.path.normpath(url.toLocalFile())
                        if os.path.isfile(p):
                            self.addItem(p)
            elif self.format == "dir":
                for url in event.mimeData().urls():
                    if url.isLocalFile():
                        p = os.path.normpath(url.toLocalFile())
                        if os.path.isdir(p):
                            self.addItem(p)
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()



class TextEditCode(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_convert = QAction("Start convert", self)
        self.start_convert.setShortcut("f10")
        self.stop_convert = QAction("Stop convert", self)
        self.stop_convert.setShortcut("f11")
        self.switch_to_relative_path = QAction("Switch to relative path", self)
        self.switch_to_absolute_path = QAction("Switch to absolute path", self)
        self.undo_action = QAction("Undo", self)
        self.undo_action.setShortcut("ctrl+z")
        self.undo_action.triggered.connect(self.undo)
        self.redo_action = QAction("Redo", self)
        self.redo_action.setShortcut("ctrl+shift+z")
        self.redo_action.triggered.connect(self.redo)
        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut("ctrl+x")
        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut("ctrl+c")
        self.copy_action.triggered.connect(self.copy)
        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut("ctrl+v")
        self.paste_action.triggered.connect(self.paste)
        self.delete_action = QAction("Delete", self)
        self.delete_action.triggered.connect(self.__delete_action_event)
        self.select_all_action = QAction("Select All", self)
        self.select_all_action.setShortcut("ctrl+a")

        self.__menu = QMenu(self)
        self.__menu.addAction(self.start_convert)
        self.__menu.addAction(self.stop_convert)
        self.__menu.addSeparator()
        self.__menu.addAction(self.switch_to_relative_path)
        self.__menu.addAction(self.switch_to_absolute_path)
        self.__menu.addSeparator()
        self.__menu.addAction(self.undo_action)
        self.__menu.addAction(self.redo_action)
        self.__menu.addSeparator()
        self.__menu.addAction(self.cut_action)
        self.__menu.addAction(self.copy_action)
        self.__menu.addAction(self.paste_action)
        self.__menu.addAction(self.delete_action)
        self.__menu.addSeparator()
        self.__menu.addAction(self.select_all_action)

    def __delete_action_event(self):
        cursor = self.textCursor()
        position = cursor.selectionStart()
        cursor.removeSelectedText()
        cursor.setPosition(position)
        self.setTextCursor(cursor)

    def keyPressEvent(self, event):
        if event.key() == (Qt.Key_Control and Qt.Key_Z):
            self.undo()
        super().keyPressEvent(event)

    def undo(self):
        self.blockSignals(True)
        super().undo()
        self.blockSignals(False)
        return super().undo()

    def contextMenuEvent(self, event):
        self.__menu.exec_(event.globalPos())
