# ui_dialogs.py
from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QComboBox, 
                             QDialogButtonBox, QMessageBox)
import data_manager
import utils
from config import WEEK_DAYS, DAY_TIMES

class AddEditUniversityDialog(QDialog):
    def __init__(self, parent=None, university_data=None):
        super().__init__(parent)
        self.university_info = university_data
        self.setWindowTitle("ویرایش دانشگاه" if university_data else "افزودن دانشگاه جدید")
        self.setMinimumWidth(300)
        self.dialog_layout = QFormLayout(self)
        self.name_input_field = QLineEdit(university_data.get('name', '') if university_data else '')
        self.dialog_layout.addRow("نام دانشگاه:", self.name_input_field)
        self.dialog_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.dialog_buttons.accepted.connect(self.check_and_accept)
        self.dialog_buttons.rejected.connect(self.reject)
        self.dialog_layout.addWidget(self.dialog_buttons)

    def check_and_accept(self):
        if not self.name_input_field.text().strip():
            QMessageBox.warning(self, "ورودی ناقص", "لطفا نام دانشگاه را وارد کنید.")
            return
        self.accept()

    def get_input_data(self):
        return {'name': self.name_input_field.text().strip()}

class AddEditClassDialog(QDialog):
    def __init__(self, parent=None, class_data=None):
        super().__init__(parent)
        self.class_info = class_data
        self.setWindowTitle("ویرایش کلاس" if class_data else "ثبت کلاس جدید")
        self.setMinimumWidth(400)
        self.dialog_layout = QFormLayout(self)
        self.dialog_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)

        self.name_input_field = QLineEdit()
        self.university_selection_combo = QComboBox()
        self.day_selection_combo = QComboBox()
        self.start_time_selection_combo = QComboBox()
        self.end_time_selection_combo = QComboBox()

        self.fill_university_combo()
        self.day_selection_combo.addItem("--- روز ---", -1)
        for i, day_name in enumerate(WEEK_DAYS):
            self.day_selection_combo.addItem(day_name, i)

        self.start_time_selection_combo.addItem("--- شروع ---", -1)
        self.end_time_selection_combo.addItem("--- پایان ---", -1)
        for i, time_text in enumerate(DAY_TIMES):
            self.start_time_selection_combo.addItem(time_text, i)
        
        for i in range(len(DAY_TIMES)):
            if i + 1 < len(DAY_TIMES):
                end_time_display_text = f"تا {DAY_TIMES[i+1]}"
            else:
                last_hour = int(DAY_TIMES[i].split(':')[0])
                end_time_display_text = f"تا {last_hour + 1:02d}:00"
            self.end_time_selection_combo.addItem(end_time_display_text, i + 1)
            if i + 1 >= len(DAY_TIMES):
                break

        self.dialog_layout.addRow("نام کلاس:", self.name_input_field)
        self.dialog_layout.addRow("نام دانشگاه:", self.university_selection_combo)
        self.dialog_layout.addRow("روز هفته:", self.day_selection_combo)
        self.dialog_layout.addRow("ساعت شروع:", self.start_time_selection_combo)
        self.dialog_layout.addRow("ساعت پایان:", self.end_time_selection_combo)

        if class_data:
            self.name_input_field.setText(class_data.get('name', ''))
            uni_id = class_data.get('university_id', -1)
            uni_index = self.university_selection_combo.findData(uni_id)
            if uni_index >= 0: self.university_selection_combo.setCurrentIndex(uni_index)
            day_index = class_data.get('day_index', -1)
            self.day_selection_combo.setCurrentIndex(self.day_selection_combo.findData(day_index))
            start_index = class_data.get('start_time_index', -1)
            self.start_time_selection_combo.setCurrentIndex(self.start_time_selection_combo.findData(start_index))
            end_index = class_data.get('end_time_index', -1)
            self.end_time_selection_combo.setCurrentIndex(self.end_time_selection_combo.findData(end_index))
        
        self.dialog_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.dialog_buttons.accepted.connect(self.check_and_accept)
        self.dialog_buttons.rejected.connect(self.reject)
        self.dialog_layout.addWidget(self.dialog_buttons)

    def fill_university_combo(self):
        self.university_selection_combo.clear()
        self.university_selection_combo.addItem("--- انتخاب دانشگاه ---", -1)
        if not data_manager.all_universities_list:
            self.university_selection_combo.setEnabled(False)
        else:
            self.university_selection_combo.setEnabled(True)
            sorted_universities = sorted(data_manager.all_universities_list, key=utils.sort_universities_by_name)
            for uni in sorted_universities:
                self.university_selection_combo.addItem(uni.get('name'), uni.get('id'))

    def check_and_accept(self):
        name = self.name_input_field.text().strip()
        uni_id = self.university_selection_combo.currentData()
        day_idx = self.day_selection_combo.currentData()
        start_idx = self.start_time_selection_combo.currentData()
        end_idx = self.end_time_selection_combo.currentData()

        if not name or uni_id == -1 or day_idx == -1 or start_idx == -1 or end_idx == -1:
            QMessageBox.warning(self, "ورودی ناقص", "لطفا تمام فیلدها را پر کنید.")
            return
        if start_idx >= end_idx:
            QMessageBox.warning(self, "زمان نامعتبر", "ساعت پایان باید بعد از ساعت شروع باشد.")
            return
        
        ignore_id = self.class_info.get('id') if self.class_info else None
        if utils.check_time_collision(day_idx, start_idx, end_idx, class_to_ignore_id=ignore_id):
            QMessageBox.warning(self, "تداخل زمانبندی", "زمان انتخاب شده با کلاس دیگری تداخل دارد.")
            return
        self.accept()

    def get_input_data(self):
        return {
            'name': self.name_input_field.text().strip(),
            'university_id': self.university_selection_combo.currentData(),
            'day_index': self.day_selection_combo.currentData(),
            'start_time_index': self.start_time_selection_combo.currentData(),
            'end_time_index': self.end_time_selection_combo.currentData(),
        }

class AddEditStudentDialog(QDialog):
    def __init__(self, parent=None, student_data=None):
        super().__init__(parent)
        self.student_info = student_data
        self.setWindowTitle("ویرایش دانشجو" if student_data else "ثبت دانشجو جدید")
        self.setMinimumWidth(400)
        self.dialog_layout = QFormLayout(self)
        self.dialog_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        
        self.name_input_field = QLineEdit()
        self.student_id_input_field = QLineEdit()
        self.university_selection_combo = QComboBox()
        self.class_selection_combo = QComboBox()
        self.class_selection_combo.setToolTip("دانش‌جو می‌تواند به هیچ کلاسی اختصاص نداشته باشد")

        self.fill_university_combo()
        self.fill_class_combo()
        
        self.dialog_layout.addRow("نام دانش‌جو:", self.name_input_field)
        self.dialog_layout.addRow("شماره دانشجویی:", self.student_id_input_field)
        self.dialog_layout.addRow("انتخاب دانشگاه:", self.university_selection_combo)
        self.dialog_layout.addRow("انتخاب کلاس:", self.class_selection_combo)
        
        self.university_selection_combo.currentIndexChanged.connect(self.fill_class_combo)

        if student_data:
            self.name_input_field.setText(student_data.get('name', ''))
            self.student_id_input_field.setText(student_data.get('student_id', ''))
            uni_id = student_data.get('university_id', -1)
            uni_index = self.university_selection_combo.findData(uni_id)
            if uni_index >= 0: self.university_selection_combo.setCurrentIndex(uni_index)
            
            # This logic ensures the previously selected class is shown correctly
            self.update_class_combo_for_edit()

        self.dialog_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.dialog_buttons.accepted.connect(self.check_and_accept)
        self.dialog_buttons.rejected.connect(self.reject)
        self.dialog_layout.addWidget(self.dialog_buttons)

    def fill_university_combo(self):
        self.university_selection_combo.clear()
        self.university_selection_combo.addItem("--- انتخاب دانشگاه ---", -1)
        if not data_manager.all_universities_list:
            self.university_selection_combo.setEnabled(False)
        else:
            self.university_selection_combo.setEnabled(True)
            sorted_universities = sorted(data_manager.all_universities_list, key=utils.sort_universities_by_name)
            for uni in sorted_universities:
                self.university_selection_combo.addItem(uni.get('name'), uni.get('id'))

    def fill_class_combo(self):
        self.class_selection_combo.clear()
        self.class_selection_combo.addItem("--- بدون کلاس ---", None)
        selected_university_id = self.university_selection_combo.currentData()
        
        available_classes = []
        if selected_university_id != -1 and selected_university_id is not None:
            available_classes = [c for c in data_manager.all_classes_list if c.get('university_id') == selected_university_id]
        else:
            available_classes = data_manager.all_classes_list
            
        if not available_classes:
            self.class_selection_combo.setEnabled(False)
        else:
            self.class_selection_combo.setEnabled(True)
            sorted_classes = sorted(available_classes, key=utils.sort_classes_by_day_and_time)
            for c in sorted_classes:
                display_text = utils.get_class_name_for_display(c.get('id'))
                self.class_selection_combo.addItem(display_text, c.get('id'))
        
        self.update_class_combo_for_edit()

    def update_class_combo_for_edit(self):
        if self.student_info and self.student_info.get('class_id') is not None:
            previous_class_id = self.student_info.get('class_id')
            if self.class_selection_combo.findData(previous_class_id) == -1:
                display_text = utils.get_class_name_for_display(previous_class_id) or f"کلاس حذف شده (ID: {previous_class_id})"
                self.class_selection_combo.addItem(f"کلاس قبلی: {display_text}", previous_class_id)
            self.class_selection_combo.setCurrentIndex(self.class_selection_combo.findData(previous_class_id))
        else:
            self.class_selection_combo.setCurrentIndex(0)
            
    def check_and_accept(self):
        name = self.name_input_field.text().strip()
        student_id = self.student_id_input_field.text().strip()
        university_id = self.university_selection_combo.currentData()
        if not name or not student_id:
            QMessageBox.warning(self, "ورودی ناقص", "لطفا نام و شماره دانشجویی را وارد کنید.")
            return
        if university_id == -1 or university_id is None:
            QMessageBox.warning(self, "ورودی ناقص", "لطفا دانشگاه دانشجو را انتخاب کنید.")
            return
        self.accept()

    def get_input_data(self):
        return {
            'name': self.name_input_field.text().strip(),
            'student_id': self.student_id_input_field.text().strip(),
            'university_id': self.university_selection_combo.currentData(),
            'class_id': self.class_selection_combo.currentData()
        }