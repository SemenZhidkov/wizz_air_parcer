"""Конфигурация приложения"""
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class Config:
    """Класс конфигурации"""
    
    # Telegram настройки
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    
    # URL для парсинга
    WIZZAIR_URL = os.getenv('WIZZAIR_URL')
    
    # Параметры рейса
    FLIGHT_DATE = os.getenv('FLIGHT_DATE', '2026-03-08')
    DEPARTURE_CITY = os.getenv('DEPARTURE_CITY', 'EVN')
    ARRIVAL_CITY = os.getenv('ARRIVAL_CITY', 'MIL')
    
    # Интервал проверки (в минутах)
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 30))
    
    # Путь к директории со скриншотами
    SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'screenshots')
    
    @classmethod
    def validate(cls):
        """Проверка наличия обязательных параметров"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env")
        if not cls.TELEGRAM_CHAT_ID:
            raise ValueError("TELEGRAM_CHAT_ID не установлен в .env")
        if not cls.WIZZAIR_URL:
            raise ValueError("WIZZAIR_URL не установлен в .env")
        
        # Создаём директорию для скриншотов если её нет
        import os
        os.makedirs(cls.SCREENSHOTS_DIR, exist_ok=True)
