from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
)

@Client.on_message(filters.private & ~filters.forwarded & filters.command("generate"))
async def main(_, msg):
    await msg.reply(
        "الان قم باختيار الجلسة",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("بايـروجـرام", callback_data="pyrogram"),
                    InlineKeyboardButton("تيلـيثـون", callback_data="telethon"),
                ]
            ]
        ),
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply(
        "- يتم الان بدأ صنع الكود {}...".format(
            "Telethon" if telethon else "Pyrogram"
        )
    )
    user_id = msg.chat.id
    api_id_msg = await bot.ask(
        user_id, "الان ارسل ايبي ايدي المكون من 8 ارقام API_ID .\n`19662621`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "هناك مشكلة! يرجى التأكد من الايبي ايدي و اعادة استخراج الجلسة من جديد /start",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    api_hash_msg = await bot.ask(
       user_id, "الان ارسل ايبي هاش API_HASH .\n`24c2270e7f1336eb59ca6c48e42ec6ca`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(
        user_id,
        "الان ارسل رقم الهاتف الخاص بك phone number مع كتابة رمز الدوله. \nمثل : +9640000000000",
        filters=filters.text,
    )
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("الان قم بارسال الكود")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply(
            "الايبي ايدي والايي هاش فيهم خطأ الرجاء اعادة الاستخراج من جديد",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply(
            "رقم الهاتف خطا رجاءً ارسال رقم الهاتف مع رمز الدوله الخاصه بك",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    try:
        phone_code_msg = await bot.ask(user_id, "الان تم ارسال اليك كود التحقق من تيليكرام قم بنسخ الكود وضع مسافه ما بين كل رقم مثل : 5 7 7 7 6", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply(
            "لقد تجاوزت الحد الزمني 10 دقائق قم ب اعادة استخراج الجلسة من جديد",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply(
            "رقم الهاتف خطا رجاءً ارسال رقم الهاتف مع رمز الدوله الخاصه بك",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply(
            "كود التحقق خطأ الرجاء الأستخراج مره اخرى والتأكد من وضع مسافه بين الأرقام عند ارسال الكود",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(
                user_id,
                "الان ارسل رمز التحقق بخطوتين",
                filters=filters.text,
                timeout=300,
            )
        except TimeoutError:
            await msg.reply(
                "انتهت مهلة استخراج الجلسة يرجى اعادة من جديد /start",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply(
                "خطأ؟ يرجى اعادة استخراج من جديد وتاكد من ارسال رمز التحقق",
                quote=True,
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "{} كود سيشن \n\n`{}` \n\n ملاحظه : لا تشارك هذا الكواد الى الأشخاص غير الثقة Dev:  @G_Rthon".format(
"تيـليـثون" if telethon else "بايـروجـرام", string_session
    )
    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    await phone_code_msg.reply(
        "{} كود سيشن \n\n تم  ارسال الكود تاكد من الرسائل المحفوظة  \n\n".format(
            "تيـليـثون" if telethon else "بايـروجـرام"
        )
    )


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply(
            "تم الغاء عملية الاسـتخراج",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif "/restart" in msg.text:
        await msg.reply(
            "تم الانتهاء من ترسيت البوت!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("تم إلغاء الجلسة!", quote=True)
        return True
    else:
        return False 
