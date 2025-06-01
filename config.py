import os
PROGRAM_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_PATH = os.path.join(PROGRAM_FOLDER, "schedule_data.json")
WEEK_DAYS = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه"]
DAY_TIMES = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']