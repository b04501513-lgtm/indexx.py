#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║       CS2 SKIN ELON BOT — bitta fayl    ║
╚══════════════════════════════════════════╝

O'rnatish:
    pip install python-telegram-bot==20.7

Ishga tushirish:
    python cs2_bot.py
"""

import logging
from telegram import (
    Update,
    InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler,
)

# ╔══════════════════════════════════════════╗
# ║      SOZLAMALAR — shu yerni o'zgartiring        ║
# ╚══════════════════════════════════════════╝

BOT_TOKEN    = "8630123637:AAFgg68MI6Z_7pnSsIcmzHmGS1cMgsIn6Dk"    # @BotFather dan olingan token
ADMIN_ID     = 7771311007                # Sizning Telegram ID (@userinfobot)
CHANNEL_ID   = "https://t.me/sk1nstore_771"          # Kanal username (@cs2_market_uz)
ADMIN_CARD   = "9860 1234 5678 9012"    # To'lov kartasi
CARD_OWNER   = "Abdullayev Jasur"       # Karta egasi
PRICE_PER_AD = 1000                   # 1 ta e'lon narxi (so'm)

# ════════════════════════════════════════════

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ConversationHandler bosqichlari
SKIN_NAME, SKIN_FLOAT, SKIN_PRICE, SKIN_EXTRA, SKIN_PHOTO, AWAITING_PAYMENT = range(6)

# Foydalanuvchi ma'lumotlari
db: dict = {}

# ─────────────────────────────────────────
# Asosiy Menyu (pastki tugmalar — rasmga o'xshash)
# ─────────────────────────────────────────
MAIN_MENU = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🔫 Skin Sotish"),      KeyboardButton("ℹ️ Qanday ishlaydi?")],
        [KeyboardButton("📢 Kanal"),             KeyboardButton("📞 Aloqa")],
    ],
    resize_keyboard=True,
    is_persistent=True,
)


# ─────────────────────────────────────────
# /start
# ─────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = user.id
    if uid in db:
        del db[uid]

    await update.message.reply_text(
        f"👋 Salom, <b>{user.first_name}</b>!\n\n"
        f"🎮 <b>CS2 Skin Market</b> botiga xush kelibsiz!\n\n"
        f"📢 Kanalimiz: {CHANNEL_ID}\n\n"
        f"Skinlaringizni sotishga e'lon bering — tez va oson!\n\n"
        f"⬇️ Quyidagi menyudan tanlang:",
        reply_markup=MAIN_MENU,
        parse_mode="HTML",
    )
    return ConversationHandler.END


# ─────────────────────────────────────────
# Menyu tugmalari
# ─────────────────────────────────────────
async def menu_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ <b>Qanday ishlaydi?</b>\n\n"
        f"1️⃣ <b>Skin Sotish</b> tugmasini bosing\n"
        f"2️⃣ Skin nomi, float, narx va rasm yuboring\n"
        f"3️⃣ Hizmat haqi to'lang — <b>{PRICE_PER_AD:,} so'm</b>\n"
        f"4️⃣ To'lov chekini yuboring\n"
        f"5️⃣ Admin tasdiqlasa — e'lon kanalga joylashadi ✅\n\n"
        f"📢 Kanal: {CHANNEL_ID}",
        parse_mode="HTML",
        reply_markup=MAIN_MENU,
    )


async def menu_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("📢 Kanalga O'tish", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}")]]
    await update.message.reply_text(
        f"📢 Bizning kanal: <b>{CHANNEL_ID}</b>\n\nBarcha e'lonlar shu yerda chiqadi!",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="HTML",
    )


async def menu_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 <b>Aloqa</b>\n\n"
        "Savol yoki muammo bo'lsa adminga yozing:\n"
        "👤 @admin_username",   # <- o'zgartiring
        parse_mode="HTML",
        reply_markup=MAIN_MENU,
    )


# ─────────────────────────────────────────
# Skin sotish — bosqichlar
# ─────────────────────────────────────────
async def sell_skin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔫 <b>Skin nomini kiriting:</b>\n<i>Misol: AK-47 | Asiimov</i>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )
    return SKIN_NAME


async def got_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db[update.effective_user.id] = {"name": update.message.text}
    await update.message.reply_text(
        "💧 <b>Skin flotini kiriting:</b>\n<i>Misol: 0.15 yoki FN / MW / FT / WW / BS</i>",
        parse_mode="HTML",
    )
    return SKIN_FLOAT


async def got_float(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db[update.effective_user.id]["float"] = update.message.text
    await update.message.reply_text(
        "💰 <b>Narxini kiriting:</b>\n<i>Misol: 150,000 so'm yoki $45</i>",
        parse_mode="HTML",
    )
    return SKIN_PRICE


async def got_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db[update.effective_user.id]["price"] = update.message.text
    await update.message.reply_text(
        "📝 <b>Qo'shimcha ma'lumot kiriting:</b>\n"
        "<i>StatTrak, stiker, holati, aloqa va h.k.\n"
        "Agar yo'q bo'lsa — Yo'q deb yozing</i>",
        parse_mode="HTML",
    )
    return SKIN_EXTRA


async def got_extra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db[update.effective_user.id]["extra"] = update.message.text
    await update.message.reply_text(
        "📸 <b>Skin rasmini yuboring:</b>\n"
        "<i>Screenshot yoki fotosuratni to'g'ridan-to'g'ri yuboring</i>",
        parse_mode="HTML",
    )
    return SKIN_PHOTO


async def got_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    user = update.effective_user

    if not update.message.photo:
        await update.message.reply_text("❌ Iltimos, rasm yuboring!")
        return SKIN_PHOTO

    d = db.setdefault(uid, {})
    d["photo"]    = update.message.photo[-1].file_id
    d["username"] = f"@{user.username}" if user.username else user.first_name

    preview = (
        f"✅ <b>E'loningiz tayyor! Ko'rib chiqing:</b>\n\n"
        f"🔫 <b>Skin:</b> {d['name']}\n"
        f"💧 <b>Float:</b> {d['float']}\n"
        f"💰 <b>Narx:</b> {d['price']}\n"
        f"📝 <b>Qo'shimcha:</b> {d['extra']}\n"
        f"👤 <b>Aloqa:</b> {d['username']}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💳 <b>Hizmat narxi:</b> {PRICE_PER_AD:,} so'm / 1 ta e'lon\n\n"
        f"To'lov uchun quyidagi kartaga o'tkating:\n"
        f"🏦 <b>Karta:</b> <code>{ADMIN_CARD}</code>\n"
        f"👤 <b>Egasi:</b> {CARD_OWNER}\n\n"
        f"To'lovdan so'ng <b>chekni</b> shu botga yuboring.\n"
        f"Admin tasdiqlasa, e'loningiz kanalga joylashtiriladi 🚀"
    )
    kb = [[InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")]]
    await update.message.reply_photo(
        photo=d["photo"],
        caption=preview,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(kb),
    )
    return AWAITING_PAYMENT


# ─────────────────────────────────────────
# To'lov chekini qabul qilish
# ─────────────────────────────────────────
async def got_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    user = update.effective_user

    if uid not in db:
        await update.message.reply_text("❌ Ma'lumot topilmadi. /start bosing.", reply_markup=MAIN_MENU)
        return ConversationHandler.END

    if update.message.photo:
        proof_id = update.message.photo[-1].file_id
        is_photo = True
    elif update.message.document:
        proof_id = update.message.document.file_id
        is_photo = False
    else:
        await update.message.reply_text(
            "📸 Iltimos, to'lov chekini <b>rasm</b> yoki <b>fayl</b> ko'rinishida yuboring.",
            parse_mode="HTML",
        )
        return AWAITING_PAYMENT

    d = db[uid]
    d["proof"]    = proof_id
    d["is_photo"] = is_photo

    admin_txt = (
        f"🔔 <b>Yangi e'lon so'rovi!</b>\n\n"
        f"👤 {user.full_name}  ({d.get('username', '')})\n"
        f"🆔 <code>{uid}</code>\n\n"
        f"🔫 <b>Skin:</b> {d['name']}\n"
        f"💧 <b>Float:</b> {d['float']}\n"
        f"💰 <b>Narx:</b> {d['price']}\n"
        f"📝 <b>Qo'shimcha:</b> {d['extra']}\n\n"
        f"💳 To'lov cheki quyida 👇"
    )
    kb = [[
        InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_{uid}"),
        InlineKeyboardButton("❌ Rad etish",  callback_data=f"reject_{uid}"),
    ]]

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=d["photo"],
        caption=f"🖼 Skin rasmi — {d['name']}",
    )
    if is_photo:
        await context.bot.send_photo(
            chat_id=ADMIN_ID, photo=proof_id,
            caption=admin_txt, parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(kb),
        )
    else:
        await context.bot.send_document(
            chat_id=ADMIN_ID, document=proof_id,
            caption=admin_txt, parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(kb),
        )

    await update.message.reply_text(
        "✅ <b>Chekingiz adminga yuborildi!</b>\n\n"
        "⏳ Admin tekshirib, tasdiqlasa e'loningiz kanalga joylashtiriladi.\n"
        "Odatda <b>5–15 daqiqa</b> ichida javob beriladi.",
        parse_mode="HTML",
        reply_markup=MAIN_MENU,
    )
    return ConversationHandler.END


# ─────────────────────────────────────────
# Admin: tasdiqlash
# ─────────────────────────────────────────
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.from_user.id != ADMIN_ID:
        await q.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    uid = int(q.data.split("_")[1])
    if uid not in db:
        await q.edit_message_caption("❌ Ma'lumot topilmadi (allaqachon qayta ishlangan).")
        return

    d = db[uid]
    post = (
        f"🔫 <b>{d['name']}</b>\n\n"
        f"💧 <b>Float:</b> {d['float']}\n"
        f"💰 <b>Narx:</b> {d['price']}\n"
        f"📝 <b>Qo'shimcha:</b> {d['extra']}\n\n"
        f"👤 <b>Sotuvchi:</b> {d.get('username', 'N/A')}\n\n"
        f"#CS2 #Skin #Sotiladi"
    )
    try:
        await context.bot.send_photo(
            chat_id=CHANNEL_ID, photo=d["photo"], caption=post, parse_mode="HTML",
        )
        await context.bot.send_message(
            chat_id=uid,
            text=(
                "🎉 <b>Tabriklaymiz!</b>\n\n"
                f"E'loningiz <b>{CHANNEL_ID}</b> kanalga muvaffaqiyatli joylashtirildi! 🚀\n\n"
                "Ko'proq skin sotmoqchimisiz? /start bosing."
            ),
            parse_mode="HTML",
            reply_markup=MAIN_MENU,
        )
        await q.edit_message_caption(
            f"✅ Tasdiqlandi va kanalga joylashtirildi!\nFoydalanuvchi: {d.get('username', uid)}",
            parse_mode="HTML",
        )
        del db[uid]
    except Exception as e:
        logger.error(e)
        await q.edit_message_caption(f"❌ Xato: {e}")


# ─────────────────────────────────────────
# Admin: rad etish
# ─────────────────────────────────────────
async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.from_user.id != ADMIN_ID:
        await q.answer("❌ Siz admin emassiz!", show_alert=True)
        return

    uid = int(q.data.split("_")[1])
    try:
        await context.bot.send_message(
            chat_id=uid,
            text=(
                "❌ <b>E'loningiz rad etildi.</b>\n\n"
                "Sabab: to'lov tasdiqlanmadi yoki ma'lumotlar noto'g'ri.\n"
                "Muammo bo'lsa adminga murojaat qiling.\n"
                "Qayta urinish: /start"
            ),
            parse_mode="HTML",
            reply_markup=MAIN_MENU,
        )
    except Exception as e:
        logger.error(e)

    if uid in db:
        del db[uid]

    await q.edit_message_caption("❌ Rad etildi. Foydalanuvchiga xabar yuborildi.", parse_mode="HTML")


# ─────────────────────────────────────────
# Bekor qilish
# ─────────────────────────────────────────
async def cancel_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    uid = update.effective_user.id
    if uid in db:
        del db[uid]
    await update.callback_query.message.reply_text("❌ Bekor qilindi.", reply_markup=MAIN_MENU)
    return ConversationHandler.END


async def cancel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in db:
        del db[uid]
    await update.message.reply_text("❌ Bekor qilindi.", reply_markup=MAIN_MENU)
    return ConversationHandler.END


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def main():
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(10)      # sekinlikni kamaytiradi
        .read_timeout(10)
        .write_timeout(10)
        .pool_timeout(10)
        .build()
    )

    conv = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^🔫 Skin Sotish$"), sell_skin_start),
        ],
        states={
            SKIN_NAME:        [MessageHandler(filters.TEXT & ~filters.COMMAND, got_name)],
            SKIN_FLOAT:       [MessageHandler(filters.TEXT & ~filters.COMMAND, got_float)],
            SKIN_PRICE:       [MessageHandler(filters.TEXT & ~filters.COMMAND, got_price)],
            SKIN_EXTRA:       [MessageHandler(filters.TEXT & ~filters.COMMAND, got_extra)],
            SKIN_PHOTO:       [MessageHandler(filters.PHOTO, got_photo)],
            AWAITING_PAYMENT: [MessageHandler(filters.PHOTO | filters.Document.ALL, got_payment)],
        },
        fallbacks=[
            CallbackQueryHandler(cancel_btn, pattern="^cancel$"),
            CommandHandler("cancel", cancel_cmd),
            CommandHandler("start", start),
        ],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)

    # Pastki menyu tugmalari
    app.add_handler(MessageHandler(filters.Regex("^ℹ️ Qanday ishlaydi\\?$"), menu_info))
    app.add_handler(MessageHandler(filters.Regex("^📢 Kanal$"), menu_channel))
    app.add_handler(MessageHandler(filters.Regex("^📞 Aloqa$"), menu_contact))

    # Admin tugmalari
    app.add_handler(CallbackQueryHandler(approve, pattern=r"^approve_\d+$"))
    app.add_handler(CallbackQueryHandler(reject,  pattern=r"^reject_\d+$"))

    logger.info("🤖 CS2 Skin Bot ishga tushdi!")
    app.run_polling(
        drop_pending_updates=True,  # eski xabarlarni o'tkazib yuboradi
        poll_interval=0,            # maksimal tezlik
        timeout=10,
    )


if __name__ == "__main__":
    main()
