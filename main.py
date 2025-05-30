import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,QStackedWidget, QLabel, QFontDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
# Import my modules
import data_manager
from ui_views import MainMenuWidget, RegistrationWidget, ScheduleWidget

APP_STYLESHEET = """
QWidget {
    font-family: Vazir, Tahoma, sans-serif; font-size: 10pt; color: #e0e0e0;
    background-color: #2d2d2d;
}
QMainWindow { background-color: #262626; }
QStackedWidget { background-color: transparent; }
QToolTip {
    background-color: #4f4f4f; color: #ffffff; border: 1px solid #606060;
    padding: 5px; border-radius: 4px; font-size: 9pt;
}
QPushButton {
    background-color: #4a4a4a; color: #ffffff; padding: 8px 16px;
    border: 1px solid #5a5a5a; border-radius: 5px; min-height: 28px;
}
QPushButton:hover { background-color: #5a5a5a; border-color: #6a6a6a; }
QPushButton:pressed { background-color: #3a3a3a; }
QPushButton:disabled { background-color: #3f3f3f; color: #8f8f8f; border-color: #4f4f4f; }
MainMenuWidget QPushButton {
    font-size: 13pt; padding: 18px 36px; background-color: #00796b; font-weight: bold;
}
MainMenuWidget QPushButton:hover { background-color: #00897b; }
MainMenuWidget QPushButton:pressed { background-color: #00695c; }
QPushButton#delete_button { background-color: #b71c1c; font-weight: bold; }
QPushButton#delete_button:hover { background-color: #c62828; }
QPushButton#delete_button:pressed { background-color: #a01818; }
QPushButton#back_button { background-color: #546e7a; padding: 7px 14px; max-width: 250px; }
QPushButton#back_button:hover { background-color: #607d8b; }
QPushButton#back_button:pressed { background-color: #455a64; }
QLineEdit, QComboBox {
    padding: 6px 9px; border: 1px solid #505050; border-radius: 4px;
    background-color: #3c3c3c; color: #f0f0f0; min-height: 22px;
}
QLineEdit:focus, QComboBox:focus { border-color: #0097a7; background-color: #424242; }
QComboBox { selection-background-color: #00796b; selection-color: #ffffff; }
QComboBox::drop-down { border: none; background-color: transparent; padding-right: 5px; }
QTableWidget {
    border: 1px solid #4a4a4a; gridline-color: #4f4f4f; background-color: #3a3a3a;
    font-size: 9.5pt; color: #dcdcdc;
}
QTableWidget::item:selected { background-color: #00796b; color: #ffffff; }
QHeaderView::section {
    background-color: #424242; padding: 6px 7px; border: none;
    border-bottom: 1px solid #5a5a5a; font-weight: bold; color: #f0f0f0;
}
QTabWidget::pane {
    border: 1px solid #4a4a4a; border-top: 3px solid #00796b; margin-top: -1px;
    background-color: #3a3a3a;
}
QTabBar::tab {
    background: #424242; border: 1px solid #4a4a4a; border-bottom: none;
    border-top-left-radius: 5px; border-top-right-radius: 5px;
    min-width: 110px; padding: 9px 14px; color: #d0d0d0; font-weight: bold;
    margin-left: 2px;
}
QTabBar::tab:selected, QTabBar::tab:hover { background: #3a3a3a; color: #ffffff; }
QLabel#main_title_label { font-size: 20pt; font-weight: bold; color: #ffffff; }
QLabel#sub_title_label { font-size: 15pt; font-weight: bold; color: #4dd0e1; padding-bottom: 12px; }
QTableWidget#schedule_table QTableWidgetItem { color: #1a237e; font-weight: bold; font-size: 9pt; }
QTableWidget#schedule_table QTableWidgetItem:selected { background-color: #004d40; color: #ffffff; }
QMessageBox { background-color: #3a3a3a; }
QMessageBox QLabel { color: #e0e0e0; font-size: 10pt; }
QMessageBox QPushButton { min-width: 75px; font-weight: bold; }
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("سامانه مدیریت کلاس")
        self.setGeometry(200, 100, 900, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.stack = QStackedWidget()
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

        # Create views
        self.schedule_screen = ScheduleWidget(self.show_main_menu)
        self.registration_screen = RegistrationWidget(self.show_main_menu, self.schedule_screen)
        self.main_menu_screen = MainMenuWidget(self.show_registration_screen, self.show_schedule_screen)
        
        # Add views to stack
        self.stack.addWidget(self.main_menu_screen)    # Index 0
        self.stack.addWidget(self.registration_screen) # Index 1
        self.stack.addWidget(self.schedule_screen)     # Index 2
        
        self.show_main_menu()

    def switch_screen(self, index):
        self.stack.setCurrentIndex(index)

    def show_main_menu(self):
        self.setWindowTitle("سامانه مدیریت کلاس")
        self.switch_screen(0)

    def show_registration_screen(self):
        self.setWindowTitle("ثبت و ویرایش اطلاعات")
        self.registration_screen.populate_all_tables()
        self.switch_screen(1)

    def show_schedule_screen(self):
        self.setWindowTitle("مشاهده زمانبندی")
        self.schedule_screen.populate_schedule_table()
        self.switch_screen(2)
        
    def closeEvent(self, event):
        """Saves data when the application is closed."""
        data_manager.save_all_data()
        event.accept()

if __name__ == "__main__":
    data_manager.load_all_data()
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    font_name = "Vazir"
    try:
        font = QFont(font_name, 10)
        if font.family().lower() != font_name.lower():
            print(f"فونت '{font_name}' پیدا نشد. از فونت پیش‌فرض استفاده می‌شود.")
    except Exception as e:
        print(f"خطا در تنظیم فونت: {e}")
        font = QFont() # Fallback to default
    app.setFont(font)
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())