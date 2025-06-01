import data_manager
from config import WEEK_DAYS, DAY_TIMES

def get_university_name(university_id_number):
    if university_id_number is None:
        return "تعیین نشده"
    try:
        target_id_number = int(university_id_number)
    except (ValueError, TypeError):
        return "نامعتبر"
    for university in data_manager.all_universities_list:
        if university.get('id') == target_id_number:
            return university.get('name', 'نامشخص')
    return "یافت نشد"

def get_class_details_by_id(class_id_number):
    if class_id_number is None:
        return None
    try:
        target_id_number = int(class_id_number)
    except (ValueError, TypeError):
        return None
    for class_item in data_manager.all_classes_list:
        if class_item.get('id') == target_id_number:
            return class_item
    return None

def get_class_name_for_display(class_id_number):
    details = get_class_details_by_id(class_id_number)
    if details:
        day_index = details.get('day_index', -1)
        start_index = details.get('start_time_index', -1)
        end_index = details.get('end_time_index', -1)

        if 0 <= day_index < len(WEEK_DAYS):
            day_text = WEEK_DAYS[day_index]
        else:
            day_text = '؟'

        if 0 <= start_index < len(DAY_TIMES):
            start_text = DAY_TIMES[start_index]
        else:
            start_text = '؟'

        if end_index > 0 and end_index - 1 < len(DAY_TIMES):
            end_text = DAY_TIMES[end_index - 1]
        else:
            end_text = '؟'
            
        return f"{details.get('name', '')} ({day_text} {start_text}-{end_text})"
    else:
        return "کلاس نامشخص"

def get_next_available_id(data_entry_list):
    if not data_entry_list:
        return 1
    highest_id = max(item.get('id', 0) for item in data_entry_list)
    return highest_id + 1

def check_time_collision(day_index_number, start_index, end_index, class_to_ignore_id=None):
    for existing_class in data_manager.all_classes_list:
        if class_to_ignore_id is not None and existing_class.get('id') == class_to_ignore_id:
            continue
        if existing_class.get('day_index') == day_index_number:
            existing_start_index = existing_class.get('start_time_index')
            existing_end_index = existing_class.get('end_time_index')
            if start_index < existing_end_index and existing_start_index < end_index:
                return True
    return False

def sort_universities_by_name(university):
    return university.get('name', '')

def sort_classes_by_day_and_time(class_item):
    return (class_item.get('day_index', 9), class_item.get('start_time_index', 99))

def sort_students_by_name(student):
    return student.get('name', '')