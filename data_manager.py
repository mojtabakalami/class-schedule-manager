import json
from config import DATA_FILE_PATH

all_classes_list = []
all_students_list = []
all_universities_list = []

def save_all_data():

    global all_classes_list, all_students_list, all_universities_list
    try:
        data_to_save = {
            "classes": all_classes_list,
            "students": all_students_list,
            "universities": all_universities_list
        }
        with open(DATA_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"خطا در ذخیره داده‌ها: {e}")
    except Exception as e:
        print(f"یک خطای غیرمنتظره در هنگام ذخیره رخ داد: {e}")

def load_all_data():

    global all_classes_list, all_students_list, all_universities_list
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
            all_classes_list = loaded_data.get("classes", [])
            all_students_list = loaded_data.get("students", [])
            all_universities_list = loaded_data.get("universities", [])
    except FileNotFoundError:
        print("فایل داده پیدا نشد. با داده خالی شروع می‌شود.")
        all_classes_list, all_students_list, all_universities_list = [], [], []
    except json.JSONDecodeError:
        print("خطا در خواندن فایل داده (فرمت نامعتبر). با داده خالی شروع می‌شود.")
        all_classes_list, all_students_list, all_universities_list = [], [], []
    except Exception as e:
        print(f"یک خطای غیرمنتظره در هنگام بارگذاری رخ داد: {e}")
        all_classes_list, all_students_list, all_universities_list = [], [], []