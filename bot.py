import telebot
from datetime import datetime

# 1. التوكن الخاص ببوتك (تأكد من وضعه بشكل صحيح)
API_TOKEN = 'ضع_هنا_توكن_بوتك_القديم'

# 2. آيدي المدير (تم تحديثه برقمك الجديد)
ADMIN_ID = 7478085292  

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    
    # رسالة ترحيب للمستخدم
    bot.reply_to(message, f"أهلاً بك يا {user_name}! أرسل تاريخ ميلادك بهذا الشكل (يوم-شهر-سنة) لأحسب عمرك.\nمثال: 15-05-1995")
    
    # إشعار يصلك أنت فقط كمدير عند دخول أي شخص
    try:
        bot.send_message(ADMIN_ID, f"🔔 مستخدم جديد دخل للبوت!\nالاسم: {user_name}\nالآيدي: {user_id}")
    except Exception as e:
        print(f"خطأ في إرسال إشعار للمدير: {e}")

@bot.message_handler(func=lambda message: True)
def calculate_age(message):
    try:
        # تحويل النص إلى تاريخ
        birth_date = datetime.strptime(message.text, '%d-%m-%Y')
        today = datetime.today()
        
        # حساب العمر
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        bot.reply_to(message, f"عمرك الآن هو: {age} سنة. 🎉")
    except ValueError:
        bot.reply_to(message, "❌ خطأ في التنسيق! يرجى إرسال التاريخ هكذا: يوم-شهر-سنة (مثال: 10-02-1990)")

print("البوت المطور بدأ العمل بنجاح...")
bot.infinity_polling()
