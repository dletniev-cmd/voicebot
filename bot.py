import asyncio
import logging
import os
import tempfile

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from groq import Groq

from config import BOT_TOKEN, GROQ_API_KEY

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
groq_client = Groq(api_key=GROQ_API_KEY)


async def download_file(bot: Bot, file_id: str) -> bytes:
    file = await bot.get_file(file_id)
    result = await bot.download_file(file.file_path)
    return result.read()


async def transcribe_audio(audio_bytes: bytes, filename: str = "audio.ogg") -> str:
    loop = asyncio.get_event_loop()

    def _transcribe():
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        try:
            with open(tmp_path, "rb") as f:
                result = groq_client.audio.transcriptions.create(
                    file=(filename, f, "audio/ogg"),
                    model="whisper-large-v3",
                    response_format="text",
                    language=None,
                    temperature=0.0,
                )
            return result
        finally:
            os.unlink(tmp_path)

    return await loop.run_in_executor(None, _transcribe)


def format_transcription(text: str) -> str:
    text = text.strip()
    if not text:
        return "<i>не удалось распознать</i>"
    return f"<i>гс в текст</i>\n<blockquote expandable>{text}</blockquote>"


@dp.message(Command("start"))
async def cmd_start(message: Message):
    me = await bot.get_me()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="добавить в группу",
            url=f"https://t.me/{me.username}?startgroup=true"
        )]
    ])
    await message.answer(
        "привет — я расшифровываю голосовые сообщения и кружки 🎙\n\n"
        "добавь меня в группу — и я буду автоматически переводить их в текст",
        reply_markup=keyboard
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "просто отправь голосовое или кружок — я отвечу расшифровкой\n\n"
        "работает в группах и в личке\n"
        "язык определяется автоматически"
    )


async def handle_audio_message(message: Message, file_id: str, filename: str):
    reply = await message.reply("слушаю 🎧")

    try:
        audio_bytes = await download_file(bot, file_id)
        text = await transcribe_audio(audio_bytes, filename)
        result = format_transcription(text)
        await reply.edit_text(result, parse_mode="HTML")
        logger.info("transcribed %s chars in chat %s", len(text), message.chat.id)
    except Exception as e:
        logger.error("transcription error: %s", e, exc_info=True)
        await reply.edit_text("не удалось расшифровать, попробуй ещё раз")


@dp.message(F.voice)
async def handle_voice(message: Message):
    await handle_audio_message(message, message.voice.file_id, "voice.ogg")


@dp.message(F.video_note)
async def handle_video_note(message: Message):
    await handle_audio_message(message, message.video_note.file_id, "video_note.mp4")


async def main():
    logger.info("бот запущен")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
