"""Главный модуль приложения"""
import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .config import Config
from .parser import WizzairParser
from .bot import TelegramNotifier

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WizzairMonitor:
    """Главный класс для мониторинга цен на Wizzair"""
    
    def __init__(self):
        self.parser = WizzairParser()
        self.notifier = TelegramNotifier()
        self.scheduler = AsyncIOScheduler()
    
    async def check_and_send_screenshot(self):
        """Делает скриншот и отправляет в Telegram"""
        logger.info("=" * 50)
        logger.info("Запуск проверки цен...")
        
        try:
            # Получаем информацию о рейсе
            flight_info = self.parser.get_flight_info()
            
            # Делаем скриншот страницы
            screenshot_path = self.parser.take_screenshot()
            
            if not screenshot_path:
                await self.notifier.send_error_message("Не удалось создать скриншот страницы")
                return
            
            # Отправляем скриншот в Telegram
            logger.info("Отправляем скриншот в Telegram...")
            await self.notifier.send_screenshot(screenshot_path, flight_info)
            logger.info("Скриншот успешно отправлен!")
            
        except Exception as e:
            logger.error(f"Ошибка при проверке: {e}")
            await self.notifier.send_error_message(f"Произошла ошибка: {str(e)}")
    
    async def start(self):
        """Запускает мониторинг"""
        logger.info("🚀 Запуск Wizzair Screenshot Monitor")
        
        # Проверяем конфигурацию
        try:
            Config.validate()
        except ValueError as e:
            logger.error(f"Ошибка конфигурации: {e}")
            return
        
        logger.info(f"Маршрут: {Config.DEPARTURE_CITY} → {Config.ARRIVAL_CITY}")
        logger.info(f"Дата рейса: {Config.FLIGHT_DATE}")
        logger.info(f"Интервал проверки: {Config.CHECK_INTERVAL} минут")
        
        # Выполняем первую проверку сразу
        await self.check_and_send_screenshot()
        
        # Настраиваем планировщик
        self.scheduler.add_job(
            self.check_and_send_screenshot,
            trigger=IntervalTrigger(minutes=Config.CHECK_INTERVAL),
            id='screenshot_check',
            name='Проверка цен Wizzair',
            replace_existing=True
        )
        
        # Запускаем планировщик
        self.scheduler.start()
        logger.info("✅ Планировщик запущен")
        
        try:
            # Держим приложение запущенным
            while True:
                await asyncio.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            logger.info("Получен сигнал остановки")
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Корректное завершение работы"""
        logger.info("Остановка приложения...")
        self.scheduler.shutdown()
        await self.notifier.close()
        logger.info("Приложение остановлено")


async def main():
    """Точка входа в приложение"""
    monitor = WizzairMonitor()
    await monitor.start()


if __name__ == "__main__":
    asyncio.run(main())
