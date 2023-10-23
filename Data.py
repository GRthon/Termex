from pyrogram.types import InlineKeyboardButton


class Data:
    generate_single_button = [
        InlineKeyboardButton("انـشاء جـلـسة", callback_data="generate")
    ]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton(text="رجـوع", callback_data="home")],
    ]

    generate_button = [generate_single_button]

    buttons = [
        generate_single_button,
        [
            InlineKeyboardButton(

                "𝗦𝗘𝗖𝗨𝗥𝗘 𝗚𝗥 ", url="https://t.me/G_Rthon"
            )
        ],
        [
            InlineKeyboardButton(" طࢪيقـة الاستـخـدام؟ ", callback_data="help"),
            InlineKeyboardButton(" حـول البـوت ", callback_data="about"),
        ],
        [InlineKeyboardButton("𝗗𝗘𝗩", url="https://t.me/e_x_e")],
    ]

    START = """  - اهـلا {} 
مࢪحبـاً بـك فـي {}
بـوت يسـاعـدك في استـخـࢪاج كود تيلـيثـون او كـود بايـࢪوجـرام
    """
    
    HELP = """
  - طـࢪيقـة الاستـخـدام؟ . 
  
/about - حـول البـوت
/help - مسـاعـدة
/start - بـدء الاسـتخـࢪاج
/repo - اعـطـاء ريبـو الـبوت
/generate - اسـتخـࢪاج الجـلسـات 
/cancel - الغـاء الاستـخـࢪاج 
/restart - ترسيـت البـوت
"""
    
    # About Message
    ABOUT = """
حـول البوت 
بوت استخـࢪاج كـود تيليـثون وبايروجـࢪام مقـدم مـن 𝗚𝗥 

قناة السورس : [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/G_Rthon)
لغة البرمجة : [ᴘʏʀᴏɢʀᴀᴍ](docs.pyrogram.org)
اللغة : [ᴘʏᴛʜᴏɴ](www.python.org)
𝗗𝗘𝗩 : @G_Rthon
    """
    
    # Repo Message
    REPO = """
انا بوت وظيفتي اساعدك باستخراج كود بايروجرام و تيليثون

𝗗𝗘𝗩𝗦 : [𝗚𝗥](https://t.me/G_Rthon)
السورس [𝗦𝗘𝗖𝗨𝗥𝗘 𝗚𝗥](https://t.me/G_Rthon)
   """
