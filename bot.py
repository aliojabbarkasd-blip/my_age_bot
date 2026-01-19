import telebot
from datetime import datetime

# --- الإعدادات ---
TOKEN = "8518076756:AAE8yCWwRAwdqtErUnRoQQv05wzi53DSX-o"
CHANNEL_ID = "@اسم_قناتك" # <--- غير هذا المعرف لاسم قناتك الحقيقي (مثلاً @my_channel)

bot = telebot.TeleBot(TOKEN)

# دالة التأكد من الاشتراك
def is_subscribed(user_id):
    try:
        # إذا كان البوت أدمن بالقناة سيستطيع فحص المشتركين
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        # في حال حدوث خطأ بالفحص (مثلاً البوت ليس أدمن)، سيسمح للمستخدم بالدخول لضمان العمل
        return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):
        bot.reply_to(message, "أهلاً بك! أنا بوت حساب العمر. 🎂\nأرسل تاريخ ميلادك الآن بهذا الشكل: سنة/شهر/يوم\nمثلاً: 1998/05/15")
    else:
        bot.reply_to(message, f"⚠️ عذراً! يجب عليك الاشتراك في القناة أولاً لتتمكن من استخدام البوت:\n{CHANNEL_ID}\n\nبعد الاشتراك، أرسل /start")

@bot.message_handler(func=lambda m: True)
def calculate(message):
    user_id = message.from_user.id
    # التأكد من الاشتراك قبل كل عملية
    if not is_subscribed(user_id):
        bot.reply_to(message, f"❌ توقف! اشترك بالقناة أولاً:\n{CHANNEL_ID}")
        return

    try:
        # معالجة التاريخ المرسل
        birth_date = datetime.strptime(message.text, "%Y/%m/%d")
        today = datetime.now()
        
        # معادلة حساب العمر بدقة
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        bot.reply_to(message, f"عمرك الآن هو: {age} سنة. 🎉")
    except:
        bot.reply_to(message, "خطأ في التنسيق! أرسل التاريخ هكذا: سنة/شهر/يوم\nمثلاً: 2000/01/01")

# تشغيل البوت
print("البوت بدأ العمل بنجاح...")
bot.infinity_polling()
