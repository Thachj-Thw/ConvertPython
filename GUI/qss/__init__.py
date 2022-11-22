DEFAULT = """
/****************************DEFAULTS**********************************/

/**********************************ALL**********************************/
* {
    color: #c3c0c4;
    font: 13px;
}

QWidget {
    background: #19181a;
}

/******************************QPushButton******************************/
QPushButton {
    background: transparent;
    padding: 0.2em 0.5em 0.2em 0.5em;
}

QPushButton::hover{
    background: rgba(255, 255, 255, 0.07);
}

QPushButton:pressed {
    background: transparent;
}


/*******************************QToolTip*********************************/
QToolTip {
    background: #373438;
    border: none;
    padding: 2px;
}


/*******************************QScrollBar*******************************/

/************horizontal*****************/
QScrollBar:horizontal {
    border: none;
    background: transparent;
    height: 15px;
}

QScrollBar::handle:horizontal {
    background: rgba(255, 255, 255, 0.1);
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background: #4e4a4f;
}


QScrollBar::add-line:horizontal {
    border: none;
    background: transparent;
    width: 0px;
    height: 0px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
    border: none;
    background: transparent;
    width: 0px;
    height: 0px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
    border: none;
    width: 0px;
    height: 0px;
    background: transparent;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: transparent;
}

/******************vertical******************/
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 15px;
}

QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.1);
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #4e4a4f;
}

QScrollBar::add-line:vertical {
    border: none;
    background: transparent;
    width: 0px;
    height: 0px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    border: none;
    background: transparent;
    width: 0px;
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar:left-arrow:vertical, QScrollBar::right-arrow:vertical {
    border: none;
    width: 0px;
    height: 0px;
    background: transparent;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
}


/*****************************QMenu****************************/
QMenu {
    padding: 0px;
    margin: 0px;
    border: none;
}

QMenu::item:selected {
    background: rgba(255, 255, 255, 0.1);
    color: #ebc4ff;
}


QMainWindow::separator {
    color: #e1dce3;
    background: #e1dce3;
}


/*************************QGroupBox*******************************/

QGroupBox {
    background-color: transparent;
    border: 1px solid #4f4652;
    border-radius: 2px;
    margin-top: 3ex;
    color: #af8fba;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 3px;
    background-color: #19181a;
    left: 5px;
}


/*************************QCheckBox*******************************/

QCheckBox {
    spacing: 5px;
}

QCheckBox::indicator {
    width: 13px;
    height: 13px;
}

QCheckBox::indicator:unchecked {
    image: url(:/icons/cil-media-stop.png);
}

QCheckBox::indicator:checked {
    image: url(:/icons/cil-task.png);
}

/********************************QDialog**************************/

QDialog #frame{
    background: #19181a;
}

QDialog QWidget {
    background: #19181a;
}

QDialog QFrame, QDialog QLabel {
    background: transparent;
}

QDialog QPushButton {
    background: #90449c;
    color: #19181a;
    border-radius: 2px;
    padding: 0.3em 0.6em 0.3em 0.6em;
}

QDialog QPushButton::hover {
    background: #bd61c7;
}


QDialog QLineEdit {
    background-color: #18161a;
    border: 1px solid #2f2733;
    border-radius: 2px;
    padding: 4px;
}


QDialog QComboBox {
    background-color: #19181a;
    border-radius: 2px;
    border: 1px solid #2f2733;
    padding: 4px;
}


QDialog QComboBox::down-arrow {
    image: url(:/icons/cil-chevron-bottom.png);
    background-color: transparent;
    width: 13px;
    height: 13px;
}

QDialog QComboBox::drop-down {
    background-color: transparent;
    border: none;
    border-radius: 1px;
    width: 20px;
}

QDialog QComboBox QAbstractItemView{
    selection-background-color: #7a4e70;
    border: 1px solid #333233;
    margin: 1px;
}

QDialog QComboBox QAbstractItemView::item {
    padding: 3px;
}


QDialog QLineEdit:disabled {
    border: none;
}

QDialog QPushButton:disabled {
    color: #4a494a;
}

QDialog QListView {
    border: none;
}


/*******************CUSTOM***********************/
#frame {
    border-top: 1px solid #555157;
}

#txe_code, #txe_out {
    border: none;
    font: 13px;
}

#line_number {
    border-right: 1px solid #555157;
    color: rgba(255, 255, 255, 0.5);
    font: 13px;
}

#frame_9 {
    border-top: 1px solid #555157;
}

#btn_clear {
    image: url(:/icons/cil-trash.png);
    width: 17px;
    height: 17px;
}

#btn_min {
    image: url(:/icons/cil-window-minimize.png);
}

#btn_max:!checked {
    image: url(:/icons/cil-window-maximize.png);
}

#btn_max:checked {
    image: url(:/icons/cil-window-restore.png);
}

#btn_close {
    image: url(:/icons/cil-x.png);
}

#btn_close::hover {
    background: rgba(255, 0, 0, 0.5);
}

#btn_new {
    image: url(:/icons/cil-file.png);
    width: 20px;
}

#btn_open {
    image: url(:/icons/cil-folder-open.png);
    width: 20px;
}

#btn_save {
    image: url(:/icons/cil-save.png);
    width: 20px;
}

#btn_run {
    image: url(:/icons/cil-media-play.png);
    width: 20px;
}

#btn_stop {
    image: url(:/icons/cil-media-stop.png);
    width: 20px;
}


QDialog #label_8 {
    font: 15px;
    font-weight: bold;
}

QDialog #btn_create_empty,
QDialog #btn_using_wizard,
QDialog #btn_add_file,
QDialog #btn_rm_file,
QDialog #btn_add_dir,
QDialog #btn_rm_dir,
QDialog #btn_tool_pathex,
QDialog #btn_add_pathex,
QDialog #btn_rm_pathex,
QDialog #btn_detect_add,
QDialog #btn_rm_all_file,
QDialog #btn_rm_all_dir {
    background: rgba(255, 255, 255, 0.04);
    color: #c3c0c4;
    border-radius: 2px;
}

QDialog #btn_create_empty::hover,
QDialog #btn_using_wizard::hover,
QDialog #btn_add_file::hover,
QDialog #btn_rm_file::hover,
QDialog #btn_add_dir::hover,
QDialog #btn_rm_dir::hover,
QDialog #btn_tool_pathex::hover,
QDialog #btn_add_pathex::hover,
QDialog #btn_rm_pathex::hover,
QDialog #btn_detect_add::hover,
QDialog #btn_rm_all_file::hover,
QDialog #btn_rm_all_dir::hover {
    background: #353336;
}

QDialog #btn_next, QDialog #btn_back, QDialog #btn_cancel{
    width: 70px;
}


QDialog #btn_path_1,
QDialog #btn_path_2,
QDialog #btn_path_3,
QDialog #btn_path_4,
QDialog #btn_path_5 {
    width: 10px;
    height: 10px;
    padding: 9px;
    background-color: transparent;
    border-radius: 2px;
    color: #c3c0c4;
    margin-left: 1px;
}

QDialog #btn_path_1::hover,
QDialog #btn_path_2::hover,
QDialog #btn_path_3::hover,
QDialog #btn_path_4::hover,
QDialog #btn_path_5::hover {
    background-color: #29262b;
}

QDialog #btn_close, QDialog #btn_min {
    background: transparent;
}

QDialog #btn_min::hover{
    background: rgba(255, 255, 255, 0.07);
}

QDialog #list_pathex {
    border: 1px solid #4f4652;
    border-radius: 2px;
}

QDialog #label_9,
QDialog #label_msg_converter,
QDialog #label_msg_app_name,
QDialog #label_msg_input,
QDialog #label_msg_output,
QDialog #label_msg_icon {
    color: #c23232;
    font: 11px;
}

QDialog #list_file_add, QDialog #list_dir_add {
    margin-top: 3px;
}
"""