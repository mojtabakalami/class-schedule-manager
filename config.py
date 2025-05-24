# config.py
import os

# مسیر پوشه‌ای که برنامه در آن قرار دارد
PROGRAM_FOLDER = os.path.dirname(os.path.abspath(__file__))

# مسیر کامل فایل ذخیره‌سازی داده‌ها
DATA_FILE_PATH = os.path.join(PROGRAM_FOLDER, "schedule_data.json")

# لیست روزهای هفته
WEEK_DAYS = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه"]

# لیست بازه‌های زمانی در طول روز
DAY_TIMES = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']