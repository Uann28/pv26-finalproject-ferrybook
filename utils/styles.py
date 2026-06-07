STYLESHEET = """
/* ── Global ── */
* {
    font-family: 'Segoe UI', 'Arial', sans-serif;
}
QMainWindow, QDialog {
    background-color: #0F1923;
}
QWidget {
    background-color: #0F1923;
    color: #E8EDF2;
    font-size: 13px;
}

/* ── Sidebar ── */
#sidebar {
    background-color: #0A1118;
    border-right: 1px solid #1E2D3D;
    min-width: 220px;
    max-width: 220px;
}
#logo_label {
    color: #00D4FF;
    font-size: 20px;
    font-weight: bold;
    padding: 20px 16px 8px 16px;
}
#subtitle_label {
    color: #4A7FA0;
    font-size: 10px;
    padding: 0 16px 20px 16px;
}
#user_info_frame {
    background-color: #12202E;
    border-radius: 8px;
    margin: 8px 12px;
    padding: 8px;
}
#user_name_label {
    color: #E8EDF2;
    font-size: 12px;
    font-weight: bold;
}
#user_role_label {
    color: #00D4FF;
    font-size: 10px;
}
#nav_button {
    background-color: transparent;
    color: #7A9BB5;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    text-align: left;
    font-size: 13px;
    margin: 2px 8px;
}
#nav_button:hover {
    background-color: #1A2D40;
    color: #E8EDF2;
}
#nav_button_active {
    background-color: #00416A;
    color: #00D4FF;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: bold;
    margin: 2px 8px;
    border-left: 3px solid #00D4FF;
}
#section_label {
    color: #3A5A70;
    font-size: 10px;
    font-weight: bold;
    padding: 12px 20px 4px 20px;
    letter-spacing: 1px;
}
#logout_button {
    background-color: #2A1020;
    color: #FF6B6B;
    border: 1px solid #4A1520;
    border-radius: 8px;
    padding: 8px 16px;
    margin: 8px 12px;
    font-size: 12px;
}
#logout_button:hover {
    background-color: #4A1520;
}

/* ── Content Area ── */
#content_area {
    background-color: #0F1923;
}
#page_title {
    color: #E8EDF2;
    font-size: 22px;
    font-weight: bold;
}
#page_subtitle {
    color: #4A7FA0;
    font-size: 12px;
}

/* ── Cards ── */
#stat_card {
    background-color: #12202E;
    border-radius: 12px;
    border: 1px solid #1E3550;
    padding: 20px;
    min-width: 160px;
}
#stat_card_value {
    color: #00D4FF;
    font-size: 28px;
    font-weight: bold;
}
#stat_card_label {
    color: #7A9BB5;
    font-size: 12px;
}
#stat_card_icon {
    font-size: 24px;
}

/* ── Buttons ── */
QPushButton {
    background-color: #1A3A5C;
    color: #E8EDF2;
    border: 1px solid #2A5A8C;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #2A5A8C;
    border-color: #00D4FF;
}
QPushButton:pressed {
    background-color: #00416A;
}
#btn_primary {
    background-color: #00416A;
    color: #00D4FF;
    border: 1px solid #00D4FF;
    border-radius: 6px;
    padding: 9px 20px;
    font-weight: bold;
}
#btn_primary:hover {
    background-color: #005A9C;
}
#btn_success {
    background-color: #0D3320;
    color: #00FF99;
    border: 1px solid #00FF99;
    border-radius: 6px;
    padding: 9px 20px;
    font-weight: bold;
}
#btn_success:hover {
    background-color: #0A5530;
}
#btn_danger {
    background-color: #3A0A10;
    color: #FF6B6B;
    border: 1px solid #FF6B6B;
    border-radius: 6px;
    padding: 9px 20px;
    font-weight: bold;
}
#btn_danger:hover {
    background-color: #5A1020;
}
#btn_warning {
    background-color: #3A2A00;
    color: #FFD700;
    border: 1px solid #FFD700;
    border-radius: 6px;
    padding: 9px 20px;
    font-weight: bold;
}
#btn_warning:hover {
    background-color: #5A4000;
}

/* ── Tables ── */
QTableWidget {
    background-color: #12202E;
    border: 1px solid #1E3550;
    border-radius: 8px;
    gridline-color: #1A2D40;
    color: #E8EDF2;
    font-size: 12px;
    selection-background-color: #00416A;
}
QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #1A2D40;
}
QTableWidget::item:selected {
    background-color: #00416A;
    color: #00D4FF;
}
QHeaderView::section {
    background-color: #0A1118;
    color: #00D4FF;
    padding: 10px 8px;
    border: none;
    border-bottom: 2px solid #00416A;
    font-weight: bold;
    font-size: 12px;
}
QHeaderView {
    background-color: #0A1118;
}
QTableWidget QScrollBar:vertical {
    background: #0A1118;
    width: 8px;
    border-radius: 4px;
}
QTableWidget QScrollBar::handle:vertical {
    background: #1E3550;
    border-radius: 4px;
}

/* ── Inputs ── */
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QComboBox {
    background-color: #12202E;
    border: 1px solid #1E3550;
    border-radius: 6px;
    padding: 8px 12px;
    color: #E8EDF2;
    font-size: 13px;
    selection-background-color: #00416A;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QDateEdit:focus, QTimeEdit:focus, QComboBox:focus {
    border: 1px solid #00D4FF;
    background-color: #162535;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox::down-arrow {
    image: none;
    border: none;
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #00D4FF;
}
QComboBox QAbstractItemView {
    background-color: #12202E;
    border: 1px solid #00D4FF;
    color: #E8EDF2;
    selection-background-color: #00416A;
}
QDateEdit::drop-down, QTimeEdit::drop-down {
    border: none;
    width: 20px;
}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background-color: #1A3A5C;
    border: none;
    width: 16px;
}

/* ── Labels ── */
QLabel {
    color: #E8EDF2;
}
#form_label {
    color: #7A9BB5;
    font-size: 12px;
    font-weight: bold;
}
#section_header {
    color: #00D4FF;
    font-size: 15px;
    font-weight: bold;
    padding: 8px 0 4px 0;
    border-bottom: 1px solid #1E3550;
}

/* ── Group Box ── */
QGroupBox {
    border: 1px solid #1E3550;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    color: #7A9BB5;
    font-weight: bold;
    font-size: 12px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #00D4FF;
}

/* ── Scroll Areas ── */
QScrollArea { border: none; background: transparent; }
QScrollBar:vertical {
    background: #0A1118;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #1E3550;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar:horizontal {
    background: #0A1118;
    height: 8px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: #1E3550;
    border-radius: 4px;
}

/* ── Tab Widget ── */
QTabWidget::pane {
    border: 1px solid #1E3550;
    border-radius: 8px;
    background: #12202E;
}
QTabBar::tab {
    background: #0A1118;
    color: #7A9BB5;
    padding: 8px 20px;
    border-radius: 4px 4px 0 0;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #00416A;
    color: #00D4FF;
    font-weight: bold;
}

/* ── Dialog ── */
QDialog {
    background-color: #0F1923;
}

/* ── Message Box ── */
QMessageBox {
    background-color: #0F1923;
}
QMessageBox QLabel {
    color: #E8EDF2;
}
QMessageBox QPushButton {
    min-width: 80px;
}

/* ── Status bar ── */
QStatusBar {
    background-color: #0A1118;
    color: #4A7FA0;
    border-top: 1px solid #1E2D3D;
    font-size: 11px;
}

/* ── Frame dividers ── */
#divider {
    background-color: #1E3550;
    max-height: 1px;
    min-height: 1px;
}

/* ── Badge ── */
#badge_success {
    background-color: #0D3320;
    color: #00FF99;
    border: 1px solid #00AA66;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: bold;
}
#badge_warning {
    background-color: #3A2A00;
    color: #FFD700;
    border: 1px solid #AA8800;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: bold;
}
#badge_danger {
    background-color: #3A0A10;
    color: #FF6B6B;
    border: 1px solid #AA2222;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: bold;
}
#badge_info {
    background-color: #00416A;
    color: #00D4FF;
    border: 1px solid #0066AA;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: bold;
}

/* ── Toolbar ── */
#toolbar_frame {
    background-color: #0A1118;
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 8px;
}

/* ── Login ── */
#login_card {
    background-color: #12202E;
    border: 1px solid #1E3550;
    border-radius: 16px;
    padding: 40px;
}
#login_title {
    color: #00D4FF;
    font-size: 28px;
    font-weight: bold;
}
#login_subtitle {
    color: #4A7FA0;
    font-size: 13px;
}
"""
