"""Telegram бот для отправки уведомлений"""
import asyncio
import logging
from typing import Dict
from aiogram import Bot
from aiogram.types import FSInputFile
from .config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Класс для отправки уведомлений в Telegram"""
    
    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        self.chat_id = Config.TELEGRAM_CHAT_ID
    
    async def send_message(self, text: str):
        """Отправляет сообщение в Telegram"""
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=text, parse_mode='HTML')
            logger.info("Сообщение успешно отправлено в Telegram")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
    
    async def send_screenshot(self, screenshot_path: str, flight_info: Dict):
        """Отправляет скриншот страницы Wizzair в Telegram"""
        try:
            # Формируем подпись к фото
            caption = f"✈️ <b>Wizzair - {flight_info['departure_city']} → {flight_info['arrival_city']}</b>\n\n"
            caption += f"📅 <b>Дата рейса:</b> {flight_info['flight_date']}\n"
            caption += f"🕐 <b>Проверено:</b> {flight_info['checked_at'][:19].replace('T', ' ')}\n\n"
            caption += f"<i>Скриншот страницы с актуальными ценами</i>"
            
            # Отправляем фото
            photo = FSInputFile(screenshot_path)
            await self.bot.send_photo(
                chat_id=self.chat_id,
                photo=photo,
                caption=caption,
                parse_mode='HTML'
            )
            logger.info(f"Скриншот успешно отправлен в Telegram: {screenshot_path}")
        except Exception as e:
            logger.error(f"Ошибка при отправке скриншота: {e}")
    
    async def send_error_message(self, error_text: str):
        """Отправляет сообщение об ошибке"""
        message = f"⚠️ <b>Ошибка при создании скриншота</b>\n\n{error_text}"
        await self.send_message(message)
    
    async def close(self):
        """Закрывает соединение с ботом"""
        await self.bot.session.close()
