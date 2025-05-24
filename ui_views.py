# ui_views.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor
import data_manager
import utils
from ui_dialogs import AddEditUniversityDialog, AddEditClassDialog, AddEditStudentDialog
from config import WEEK_DAYS, DAY_TIMES

class MainMenuWidget(QWidget):
    def __init__(self, show_registration_screen_callback, show_schedule_screen_callback, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(40)
        title_label = QLabel("سامانه مدیریت کلاس و زمانبندی")
        title_label.setObjectName("main_title_label")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.register_info_button = QPushButton(" ثبت / ویرایش اطلاعات ")
        self.view_schedule_button = QPushButton(" مشاهده جدول زمانبندی ")
        self.register_info_button.setMinimumSize(QSize(350, 65))
        self.view_schedule_button.setMinimumSize(QSize(350, 65))
        self.register_info_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.view_schedule_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(title_label)
        layout.addWidget(self.register_info_button)
        layout.addWidget(self.view_schedule_button)
        self.register_info_button.clicked.connect(show_registration_screen_callback)
        self.view_schedule_button.clicked.connect(show_schedule_screen_callback)

class RegistrationWidget(QWidget):
    def __init__(self, show_main_menu_callback, schedule_widget, parent=None):
        super().__init__(parent)
        self.show_main_menu_callback = show_main_menu_callback
        self.schedule_widget = schedule_widget # Reference to update schedule view
        
        main_layout = QVBoxLayout(self)
        title_label = QLabel("مدیریت اطلاعات دانشگاه، کلاس و دانش‌جو")
        title_label.setObjectName("sub_title_label")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        self.create_university_tab()
        self.create_class_tab()
        self.create_student_tab()

        self.back_button = QPushButton("بازگشت به منوی اصلی")
        self.back_button.setObjectName("back_button")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.clicked.connect(self.show_main_menu_callback)
        main_layout.addWidget(self.back_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.populate_all_tables()

    def create_university_tab(self):
        self.uni_tab = QWidget()
        layout = QVBoxLayout(self.uni_tab)
        self.uni_table = self.create_table(["شناسه", "نام دانشگاه"])
        self.uni_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.uni_table)
        
        btn_layout = QHBoxLayout()
        self.add_uni_btn = QPushButton("افزودن دانشگاه")
        self.edit_uni_btn = QPushButton("ویرایش دانشگاه")
        self.del_uni_btn = QPushButton("حذف دانشگاه")
        self.del_uni_btn.setObjectName("delete_button")
        btn_layout.addStretch()
        btn_layout.addWidget(self.add_uni_btn)
        btn_layout.addWidget(self.edit_uni_btn)
        btn_layout.addWidget(self.del_uni_btn)
        layout.addLayout(btn_layout)
        
        self.tab_widget.addTab(self.uni_tab, "مدیریت دانشگاه‌ها")
        
        self.add_uni_btn.clicked.connect(self.add_university)
        self.edit_uni_btn.clicked.connect(self.edit_university)
        self.del_uni_btn.clicked.connect(self.delete_university)

    def create_class_tab(self):
        self.class_tab = QWidget()
        layout = QVBoxLayout(self.class_tab)
        self.class_table = self.create_table(["شناسه", "نام کلاس", "دانشگاه", "روز", "شروع", "پایان"])
        self.class_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.class_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.class_table)
        
        btn_layout = QHBoxLayout()
        self.add_class_btn = QPushButton("ثبت کلاس")
        self.edit_class_btn = QPushButton("ویرایش کلاس")
        self.del_class_btn = QPushButton("حذف کلاس")
        self.del_class_btn.setObjectName("delete_button")
        btn_layout.addStretch()
        btn_layout.addWidget(self.add_class_btn)
        btn_layout.addWidget(self.edit_class_btn)
        btn_layout.addWidget(self.del_class_btn)
        layout.addLayout(btn_layout)
        
        self.tab_widget.addTab(self.class_tab, "مدیریت کلاس‌ها")
        
        self.add_class_btn.clicked.connect(self.add_class)
        self.edit_class_btn.clicked.connect(self.edit_class)
        self.del_class_btn.clicked.connect(self.delete_class)

    def create_student_tab(self):
        self.student_tab = QWidget()
        layout = QVBoxLayout(self.student_tab)
        self.student_table = self.create_table(["شناسه", "نام دانش‌جو", "شماره دانشجویی", "دانشگاه", "کلاس"])
        self.student_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.student_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.student_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.student_table)
        
        btn_layout = QHBoxLayout()
        self.add_student_btn = QPushButton("افزودن دانشجو")
        self.edit_student_btn = QPushButton("ویرایش دانشجو")
        self.del_student_btn = QPushButton("حذف دانشجو")
        self.del_student_btn.setObjectName("delete_button")
        btn_layout.addStretch()
        btn_layout.addWidget(self.add_student_btn)
        btn_layout.addWidget(self.edit_student_btn)
        btn_layout.addWidget(self.del_student_btn)
        layout.addLayout(btn_layout)
        
        self.tab_widget.addTab(self.student_tab, "مدیریت دانش‌جویان")
        
        self.add_student_btn.clicked.connect(self.add_student)
        self.edit_student_btn.clicked.connect(self.edit_student)
        self.del_student_btn.clicked.connect(self.delete_student)

    def create_table(self, headers):
        table = QTableWidget()
        table.setObjectName("info_table")
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSortingEnabled(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        return table

    def populate_all_tables(self):
        self.populate_university_table()
        self.populate_class_table()
        self.populate_student_table()

    def populate_university_table(self):
        self.uni_table.setSortingEnabled(False)
        self.uni_table.setRowCount(0)
        for row, uni in enumerate(sorted(data_manager.all_universities_list, key=utils.sort_universities_by_name)):
            self.uni_table.insertRow(row)
            id_item = QTableWidgetItem(str(uni.get('id')))
            id_item.setData(Qt.ItemDataRole.UserRole, uni.get('id'))
            self.uni_table.setItem(row, 0, id_item)
            self.uni_table.setItem(row, 1, QTableWidgetItem(uni.get('name')))
        self.uni_table.setSortingEnabled(True)

    def populate_class_table(self):
        self.class_table.setSortingEnabled(False)
        self.class_table.setRowCount(0)
        for row, cls in enumerate(sorted(data_manager.all_classes_list, key=utils.sort_classes_by_day_and_time)):
            self.class_table.insertRow(row)
            id_item = QTableWidgetItem(str(cls.get('id')))
            id_item.setData(Qt.ItemDataRole.UserRole, cls.get('id'))
            self.class_table.setItem(row, 0, id_item)
            self.class_table.setItem(row, 1, QTableWidgetItem(cls.get('name')))
            self.class_table.setItem(row, 2, QTableWidgetItem(utils.get_university_name(cls.get('university_id'))))
            day = WEEK_DAYS[cls['day_index']] if 'day_index' in cls and 0 <= cls['day_index'] < len(WEEK_DAYS) else '؟'
            start = DAY_TIMES[cls['start_time_index']] if 'start_time_index' in cls and 0 <= cls['start_time_index'] < len(DAY_TIMES) else '؟'
            end = DAY_TIMES[cls['end_time_index'] - 1] if 'end_time_index' in cls and 0 < cls['end_time_index'] <= len(DAY_TIMES) else '؟'
            self.class_table.setItem(row, 3, QTableWidgetItem(day))
            self.class_table.setItem(row, 4, QTableWidgetItem(start))
            self.class_table.setItem(row, 5, QTableWidgetItem(end))
        self.class_table.setSortingEnabled(True)

    def populate_student_table(self):
        self.student_table.setSortingEnabled(False)
        self.student_table.setRowCount(0)
        for row, std in enumerate(sorted(data_manager.all_students_list, key=utils.sort_students_by_name)):
            self.student_table.insertRow(row)
            id_item = QTableWidgetItem(str(std.get('id')))
            id_item.setData(Qt.ItemDataRole.UserRole, std.get('id'))
            self.student_table.setItem(row, 0, id_item)
            self.student_table.setItem(row, 1, QTableWidgetItem(std.get('name')))
            self.student_table.setItem(row, 2, QTableWidgetItem(std.get('student_id')))
            self.student_table.setItem(row, 3, QTableWidgetItem(utils.get_university_name(std.get('university_id'))))
            self.student_table.setItem(row, 4, QTableWidgetItem(utils.get_class_name_for_display(std.get('class_id'))))
        self.student_table.setSortingEnabled(True)

    def get_selected_id(self, table):
        selected_rows = table.selectionModel().selectedRows()
        if not selected_rows:
            return None
        return table.item(selected_rows[0].row(), 0).data(Qt.ItemDataRole.UserRole)
    
    def add_university(self):
        dialog = AddEditUniversityDialog(self)
        if dialog.exec():
            data = dialog.get_input_data()
            if any(u.get('name', '').lower() == data['name'].lower() for u in data_manager.all_universities_list):
                QMessageBox.warning(self, "خطا", f"دانشگاهی با نام '{data['name']}' قبلا ثبت شده است.")
                return
            data['id'] = utils.get_next_available_id(data_manager.all_universities_list)
            data_manager.all_universities_list.append(data)
            self.update_all_views()

    def edit_university(self):
        uni_id = self.get_selected_id(self.uni_table)
        if uni_id is None:
            QMessageBox.warning(self, "انتخاب نشده", "لطفا یک دانشگاه را برای ویرایش انتخاب کنید.")
            return
        uni_data = next((u for u in data_manager.all_universities_list if u.get('id') == uni_id), None)
        if uni_data:
            dialog = AddEditUniversityDialog(self, uni_data)
            if dialog.exec():
                updated_data = dialog.get_input_data()
                if any(u.get('id') != uni_id and u.get('name', '').lower() == updated_data['name'].lower() for u in data_manager.all_universities_list):
                    QMessageBox.warning(self, "خطا", f"دانشگاه دیگری با نام '{updated_data['name']}' وجود دارد.")
                    return
                uni_data['name'] = updated_data['name']
                self.update_all_views()
    
    def delete_university(self):
        uni_id = self.get_selected_id(self.uni_table)
        if uni_id is None:
            QMessageBox.warning(self, "انتخاب نشده", "لطفا یک دانشگاه را برای حذف انتخاب کنید.")
            return
        
        uni_name = utils.get_university_name(uni_id)
        reply = QMessageBox.question(self, "تایید حذف", f"آیا از حذف دانشگاه '{uni_name}' مطمئن هستید؟\nاین عمل باعث حذف کلاس‌ها و دانشجویان مرتبط نمی‌شود، بلکه ارتباط آن‌ها قطع خواهد شد.", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            data_manager.all_universities_list = [u for u in data_manager.all_universities_list if u.get('id') != uni_id]
            for cls in data_manager.all_classes_list:
                if cls.get('university_id') == uni_id:
                    cls['university_id'] = None
            for std in data_manager.all_students_list:
                if std.get('university_id') == uni_id:
                    std['university_id'] = None
            self.update_all_views()

    def add_class(self):
        if not data_manager.all_universities_list:
            QMessageBox.information(self, "نیازمندی", "ابتدا باید حداقل یک دانشگاه ثبت کنید.")
            return
        dialog = AddEditClassDialog(self)
        if dialog.exec():
            data = dialog.get_input_data()
            data['id'] = utils.get_next_available_id(data_manager.all_classes_list)
            data_manager.all_classes_list.append(data)
            self.update_all_views()
            
    def edit_class(self):
        class_id = self.get_selected_id(self.class_table)
        if class_id is None:
            QMessageBox.warning(self, "انتخاب نشده", "لطفا یک کلاس را برای ویرایش انتخاب کنید.")
            return
        class_data = utils.get_class_details_by_id(class_id)
        if class_data:
            dialog = AddEditClassDialog(self, class_data)
            if dialog.exec():
                updated_data = dialog.get_input_data()
                class_data.update(updated_data)
                self.update_all_views()

    def delete_class(self):
        class_id = self.get_selected_id(self.class_table)
        if class_id is None:
            QMessageBox.warning(self, "انتخاب نشده", "لطفا یک کلاس را برای حذف انتخاب کنید.")
            return
        
        class_name = utils.get_class_name_for_display(class_id)
        reply = QMessageBox.question(self, "تایید حذف", f"آیا از حذف کلاس '{class_name}' مطمئن هستید؟\nدانشجویان این کلاس بدون کلاس خواهند شد.", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            data_manager.all_classes_list = [c for c in data_manager.all_classes_list if c.get('id') != class_id]
            for std in data_manager.all_students_list:
                if std.get('class_id') == class_id:
                    std['class_id'] = None
            self.update_all_views()

    def add_student(self):
        if not data_manager.all_universities_list:
            QMessageBox.information(self, "نیازمندی", "ابتدا باید حداقل یک دانشگاه ثبت کنید.")
            return
        dialog = AddEditStudentDialog(self)
        if dialog.exec():
            data = dialog.get_input_data()
            data['id'] = utils.get_next_available_id(data_manager.all_students_list)
            data_manager.all_students_list.append(data)
            self.populate_student_table()

    def edit_student(self):
        student_id = self.get_selected_id(self.student_table)
        if student_id is None:
            QMessageBox.warning(self, "انتخاب نشده", "لطفا یک دانشجو را برای ویرایش انتخاب کنید.")
            return
        student_data = next((s for s in data_manager.all_students_list if s.get('id') == student_id), None)
        if student_data:
            dialog = AddEditStudentDialog(self, student_data)
            if dialog.exec():
                updated_data = dialog.get_input_data()
                student_data.update(updated_data)
                self.populate_student_table()

    def delete_student(self):
        student_id = self.get_selected_id(self.student_table)
        if student_id is None:
            QMessageBox.warning(self, "انتخاب نشده", "لطفا یک دانشجو را برای حذف انتخاب کنید.")
            return
        
        student_name = next((s.get('name') for s in data_manager.all_students_list if s.get('id') == student_id), "N/A")
        reply = QMessageBox.question(self, "تایید حذف", f"آیا از حذف دانشجو '{student_name}' مطمئن هستید؟", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            data_manager.all_students_list = [s for s in data_manager.all_students_list if s.get('id') != student_id]
            self.populate_student_table()
    
    def update_all_views(self):
        """Updates all tables in this widget and the schedule view."""
        self.populate_all_tables()
        self.schedule_widget.populate_schedule_table()

class ScheduleWidget(QWidget):
    def __init__(self, show_main_menu_callback, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        title_label = QLabel("جدول زمانبندی هفتگی کلاس‌ها")
        title_label.setObjectName("sub_title_label")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        self.schedule_table = QTableWidget(len(WEEK_DAYS), len(DAY_TIMES))
        self.schedule_table.setObjectName("schedule_table")
        self.schedule_table.setVerticalHeaderLabels(WEEK_DAYS)
        self.schedule_table.setHorizontalHeaderLabels(DAY_TIMES)
        self.schedule_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.schedule_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.schedule_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_layout.addWidget(self.schedule_table)
        
        self.back_button = QPushButton("بازگشت به منوی اصلی")
        self.back_button.setObjectName("back_button")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        main_layout.addWidget(self.back_button, 0, Qt.AlignmentFlag.AlignCenter)

        self.back_button.clicked.connect(show_main_menu_callback)
        self.schedule_table.cellClicked.connect(self.show_class_students)
        
        self.populate_schedule_table()

    def populate_schedule_table(self):
        self.schedule_table.clearContents()
        for r in range(self.schedule_table.rowCount()):
            for c in range(self.schedule_table.columnCount()):
                self.schedule_table.setSpan(r, c, 1, 1)

        for cls in data_manager.all_classes_list:
            day, start, end = cls.get('day_index',-1), cls.get('start_time_index',-1), cls.get('end_time_index',-1)
            if not (0 <= day < len(WEEK_DAYS) and 0 <= start < end <= len(DAY_TIMES)):
                continue

            duration = end - start
            display_text = f"{cls.get('name', '')}\n({utils.get_university_name(cls.get('university_id'))})"
            item = QTableWidgetItem(display_text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setBackground(QColor("lightblue"))
            item.setData(Qt.ItemDataRole.UserRole, cls.get('id'))
            item.setToolTip(f"{utils.get_class_name_for_display(cls.get('id'))}")
            
            self.schedule_table.setItem(day, start, item)
            if duration > 1:
                self.schedule_table.setSpan(day, start, 1, duration)

    def get_class_id_from_cell(self, row, column):
        item = self.schedule_table.item(row, column)
        if item:
            return item.data(Qt.ItemDataRole.UserRole)
        # Check for span
        for c in range(column, -1, -1):
            if self.schedule_table.columnSpan(row, c) > 1:
                item = self.schedule_table.item(row, c)
                if item and c + self.schedule_table.columnSpan(row, c) > column:
                    return item.data(Qt.ItemDataRole.UserRole)
        return None

    def show_class_students(self, row, column):
        class_id = self.get_class_id_from_cell(row, column)
        if class_id is None:
            return
        
        class_info = utils.get_class_details_by_id(class_id)
        if class_info:
            students_in_class = [f"- {s.get('name')} ({s.get('student_id')})" for s in data_manager.all_students_list if s.get('class_id') == class_id]
            class_display_name = utils.get_class_name_for_display(class_id)
            
            if students_in_class:
                message = f"دانشجویان کلاس '{class_display_name}':\n\n" + "\n".join(students_in_class)
            else:
                message = f"کلاس '{class_display_name}' دانشجویی ندارد."
            
            QMessageBox.information(self, "لیست دانشجویان کلاس", message)