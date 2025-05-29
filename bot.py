import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# --- Config ---
ADMIN_IDS = [7409502548]  # <-- Замінити на свій реальний Telegram ID

# --- Global memory to track user package selections ---
USER_PACKAGE_SELECTIONS = {}

# --- Package-specific content ---
PACKAGE_CONTENT = {
    "base": {
        "album_photo": [
            "AgACAgIAAxkBAAIBS2g4hDyCuZrHDzCnStGvxEFvioqaAAKM8zEbD1DJSaWS_VqMyqXuAQADAgADeQADNgQ",
            "AgACAgIAAxkBAAIBTWg4hFlgvvCswbQXymqg-bb1FTQFAAKN8zEbD1DJSVVJn3GV6cvyAQADAgADeQADNgQ"
        ],
        "single_items": []
    },
    "vip": {
        "album_photo": [
            "AgACAgIAAxkBAAIBT2g4hHPszR_HOVfz9fEq9gOUEh5jAAKO8zEbD1DJSeesZZIrhiKMAQADAgADdwADNgQ",
            "AgACAgIAAxkBAAIBYmg4iRF6jqxP_09VsjG4ru60UZHgAAKr8zEbD1DJSYd5XaJvA7OKAQADAgADdwADNgQ",
            "AgACAgIAAxkBAAIBZGg4iUDBtjUiA7bClZEOjY43zZbfAAKu8zEbD1DJSagMhu-rWylRAQADAgADeQADNgQ",
            "AgACAgIAAxkBAAIBZmg4iXMK2fkwRBLHtsQ9IYMntv6nAAKy8zEbD1DJSXgunLoSQ9-WAQADAgADeQADNgQ"
        ],
        "single_items": [
            {"type": "video", "file_id": "BAACAgIAAxkBAAIBYGg4iM4MPxdS1eN-5PY-yozR-I3ZAAL0cwACD1DJSdOSEbBt8-ieNgQ"}
        ]
    },
    "vipplus": {
        "album_photo": ["AgACAgIAAxkBAAIBaGg4iY2ERsgMTmPap_KApw1vGesjAAK08zEbD1DJSQ9xcDi9qwSiAQADAgADeQADNgQ"],
        "single_items": []
    }
}


import os
TOKEN = os.getenv("TOKEN")

# --- Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 Плани підписки", callback_data="plans")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text(
            "✨ <b>Ласкаво просимо до VIP-зони</b> ✨\n\n"
            "Привіт 👋 Раді тебе бачити тут!\n"
            "Ознайомся з нашими ексклюзивними пакетами доступу нижче:",
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            "✨ <b>Ласкаво просимо до VIP-зони</b> ✨\n\n"
            "Привіт 👋 Раді тебе бачити тут!\n"
            "Ознайомся з нашими ексклюзивними пакетами доступу нижче:",
            parse_mode='HTML',
            reply_markup=reply_markup
        )

# --- Send Plans ---
async def send_plans(chat_id, bot):
    keyboard = [
        [InlineKeyboardButton("🥉 Обрати BASE", callback_data="select_base")],
        [InlineKeyboardButton("🥈 Обрати VIP", callback_data="select_vip")],
        [InlineKeyboardButton("🥇 Обрати VIP+", callback_data="select_vipplus")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_from_plans")]
    ]
    await bot.send_message(
        chat_id=chat_id,
        text=(
            "💎 <b>Пакети доступу до VIP-контенту</b> 💎\n\n"
            "🥉 <b>BASE</b> — <b>80₴</b>\n"
            "   📦 Базовий набір ексклюзивного контенту\n"
            "   🌸 Ніжні образи без зайвого\n\n"
            "🥈 <b>VIP</b> — <b>250₴</b>\n"
            "   🔥 Більше відвертості та естетики\n"
            "   🎥 Бонус: коротке відео-сюрприз\n\n"
            "🥇 <b>VIP+</b> — <b>500₴</b>\n"
            "   💫 Повний набір без обмежень\n"
            "   🎞️ Ексклюзивні фото і відео, яких немає ніде\n\n"
            "ℹ️ <i>Обери свій рівень і переходь до інструкції з оплаті.</i>"
        ),
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- Callback Handler ---
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "plans":
        await send_plans(query.message.chat_id, context.bot)

    elif query.data == "back_from_plans":
        await start(update, context)

    elif query.data == "back_from_package":
        await send_plans(query.message.chat_id, context.bot)

    elif query.data.startswith("select_"):
        level = query.data.split("_")[1]
        USER_PACKAGE_SELECTIONS[query.from_user.id] = level
        payment_info = {
            "base": ("80₴", "🥉 BASE", "AgACAgIAAxkBAAMtaDdcQrO2yK0aqIInTDOhoAIDmxQAAkX6MRs19blJI4Te4Kkdyg8BAAMCAAN3AAM2BA"),
            "vip": ("250₴", "🥈 VIP", "AgACAgIAAxkBAAM8aDddkvFoS1yqq6cAAZBi6Tch0VhCAAJM-jEbNfW5Sdl1sj_dsdraAQADAgADeAADNgQ"),
            "vipplus": ("500₴", "🥇 VIP+", "AgACAgIAAxkBAAM-aDddsqheZlNKjKDdn9oyEulJwSwAAk36MRs19blJNRe0eFLDDagBAAMCAAN4AAM2BA")
        }
        amount, label, file_id = payment_info[level]
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_from_package")]]
        await query.edit_message_media(
            media=InputMediaPhoto(
                media=file_id,
                caption=(
                    f"🔐 Ти обрав {label}\n"
                    f"💸 Вартість: {amount}\n\n"
                    f"ℹ️ Надішли оплату на карту: <code>4483 8200 3220 0296</code>\n"
                    "Після цього надішли фото квитанції у цей бот."
                ),
                parse_mode="HTML"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# --- Photo Handler ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    caption = f"📥 Нова квитанція від @{user.username or user.first_name} (ID: {user.id})"

    for admin_id in ADMIN_IDS:
        await context.bot.forward_message(chat_id=admin_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        keyboard = [[InlineKeyboardButton("✅ Підтвердити", callback_data=f"confirm_{user.id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=admin_id, text=caption, reply_markup=reply_markup)

    await update.message.reply_text("✅ Дякую, чек отримано! Очікуй підтвердження від адміністрації.")

# --- Confirm Handler ---
from telegram import InputMediaPhoto, InputMediaVideo

async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = int(query.data.split("_")[1])
    level = USER_PACKAGE_SELECTIONS.get(user_id)

    if not level:
        await context.bot.send_message(chat_id=user_id, text="⚠️ Сталася помилка: не знайдено обраного пакету.")
        return

    content = PACKAGE_CONTENT.get(level, {})

    # Надіслати альбом фото, якщо є
    album_photos = content.get("album_photo", [])
    if album_photos:
        media_group = [InputMediaPhoto(media=file_id) for file_id in album_photos]
        await context.bot.send_media_group(chat_id=user_id, media=media_group)

    # Надіслати інші медіа (наприклад відео)
    for item in content.get("single_items", []):
        if item["type"] == "photo":
            await context.bot.send_photo(chat_id=user_id, photo=item["file_id"])
        elif item["type"] == "video":
            await context.bot.send_video(chat_id=user_id, video=item["file_id"])

    await context.bot.send_message(chat_id=user_id, text="🎉 Підписка активована! Дякуємо за покупку.")
    await query.edit_message_text("✅ Підписка підтверджена.")

# --- Get File ID ---
async def capture_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.photo:
        file_id = msg.photo[-1].file_id
        await msg.reply_text(f"🖼 <b>Photo</b> file_id:\n<code>{file_id}</code>", parse_mode="HTML")

    elif msg.video:
        file_id = msg.video.file_id
        await msg.reply_text(f"🎥 <b>Video</b> file_id:\n<code>{file_id}</code>", parse_mode="HTML")

    elif msg.document:
        # Перевіримо, що це відео-документ (не gif)
        mime_type = msg.document.mime_type or ""
        if mime_type.startswith("video/"):
            file_id = msg.document.file_id
            await msg.reply_text(f"📁 <b>Video Document</b> file_id:\n<code>{file_id}</code>", parse_mode="HTML")
        else:
            await msg.reply_text(f"📎 Document MIME: {mime_type}\n⚠️ Не підтримується для /get_id")

    else:
        await msg.reply_text("⚠️ Не знайдено підтримуваного медіа.")


# --- Main ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_callback, pattern="^(plans|select_base|select_vip|select_vipplus|back_from_plans|back_from_package)$"))
app.add_handler(CallbackQueryHandler(confirm_payment, pattern="^confirm_\\d+$"))
app.add_handler(MessageHandler(
    (filters.PHOTO | filters.VIDEO | filters.Document.VIDEO) & filters.CaptionRegex("^/get_id$"),
    capture_file_id
))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == '__main__':
    print("Bot is running...")
    app.run_polling()
