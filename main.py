import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

TOKEN = "9287007550:AAE_08mQHSBMJcTSC1OnCEl2wodjjeeEDM4"
CHANNEL_ID = "@kanalingiz_usernami"

bot = Bot(token=TOKEN)
router = Router()
dp = Dispatcher()

MOVIES = {
    "1": "BAACAgIAAxkBAAE...",
    "2": "BAACAgIAAxkBAAE...",
}

async def check_subscription(user_id: int) -> bool:
  try:
    member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    if member.status in ["member", "administrator", "creator"]:
      return True
  except Exception:
    pass
  return False

@router.message(CommandStart())
async def cmd_start(message: Message):
  user_id = message.from_user.id
  is_subscribed = await check_subscription(user_id)

  if not is_subscribed:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url="https://t.me/kanalingiz_usernami")],
            [InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub")]
        ]
    )
    await message.answer("Assalomu alaykum! Botimizdan foydalanish uchun avval kanalimizga obuna bo'ling:", reply_markup=keyboard)
  else:
    await message.answer("Xush kelibsiz! Marhamat, kino kodini yuboring:")

@router.callback_query(F.data == "check_sub")
async def verify_subscription(callback: CallbackQuery):
  user_id = callback.from_user.id
  is_subscribed = await check_subscription(user_id)

  if is_subscribed:
    await callback.message.delete()
    await callback.message.answer("Rahmat! Obuna tasdiqlandi. Endi kino kodini yuborishingiz mumkin:")
  else:
    await callback.answer("Siz hali kanalga obuna bo'lmadingiz!", show_alert=True)

@router.message(F.text)
async def send_movie(message: Message):
  user_id = message.from_user.id
  is_subscribed = await check_subscription(user_id)

  if not is_subscribed:
    await message.answer("Iltimos, avval kanalimizga obuna bo'ling va obunani tekshiring!")
    return

  code = message.text.strip()
  if code in MOVIES:
    await message.answer_video(video=MOVIES[code], caption="Marhamat, kinongiz!")
  else:
    await message.answer("Bunday kodli kino topilmadi.")

dp.include_router(router)

async def main():
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)

if __name__ == "__main__":
  asyncio.run(main())
