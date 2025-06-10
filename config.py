import os
import sys

def get_app_data_path(app_name, filename):


    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        application_path = os.path.dirname(sys.executable)
    else:
        
        application_path = os.path.dirname(os.path.abspath(__file__))


    if sys.platform == "win32":
        app_data_dir = os.path.join(os.getenv('APPDATA'), app_name)

        app_data_dir = os.path.join(os.path.expanduser('~/Library/Application Support'), app_name)
    else:

        app_data_dir = os.path.join(os.path.expanduser('~/.local/share'), app_name)
 

    if not os.path.exists(app_data_dir):
        os.makedirs(app_data_dir)

    return os.path.join(app_data_dir, filename)


DATA_FILE_PATH = get_app_data_path('ClassSchedulerApp', 'schedule_data.json')

PROGRAM_FOLDER = os.path.dirname(DATA_FILE_PATH)

WEEK_DAYS = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه"]
DAY_TIMES = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']