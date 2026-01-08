"""Парсер данных с сайта Wizzair (версия со скриншотами)"""
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import logging
from datetime import datetime
from typing import Optional
import time
import random
import os
from .config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WizzairParser:
    """Класс для создания скриншотов страницы Wizzair"""
    
    def __init__(self):
        self.url = Config.WIZZAIR_URL
    
    def _get_driver(self):
        """Создает undetected Chrome driver для обхода защиты"""
        options = uc.ChromeOptions()
        # ОТКЛЮЧАЕМ headless режим - работаем с видимым браузером!
        # options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--lang=en-GB')
        
        # undetected_chromedriver автоматически обходит многие защиты
        driver = uc.Chrome(options=options, version_main=None)
        
        return driver
    
    def _human_like_scroll(self, driver):
        """Имитация человеческой прокрутки страницы"""
        try:
            # Получаем высоту страницы
            total_height = driver.execute_script("return document.body.scrollHeight")
            viewport_height = driver.execute_script("return window.innerHeight")
            
            # Скроллим вниз маленькими шагами
            current_position = 0
            scroll_step = random.randint(100, 200)
            
            logger.info("🖱️  Имитируем прокрутку страницы (медленно, как человек)...")
            
            while current_position < total_height - viewport_height:
                # Прокручиваем на случайное расстояние
                scroll_amount = random.randint(scroll_step - 50, scroll_step + 100)
                current_position += scroll_amount
                
                driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(random.uniform(0.8, 1.5))  # Более медленная прокрутка
                
                # Иногда останавливаемся (читаем контент)
                if random.random() < 0.3:
                    time.sleep(random.uniform(1.5, 3.0))
                
                # Иногда прокручиваем назад (как настоящий пользователь)
                if random.random() < 0.25:
                    back_scroll = random.randint(50, 200)
                    current_position -= back_scroll
                    driver.execute_script(f"window.scrollTo(0, {current_position});")
                    time.sleep(random.uniform(0.5, 1.2))
            
            # Останавливаемся внизу страницы
            logger.info("⏸️  Пауза внизу страницы...")
            time.sleep(random.uniform(2.0, 4.0))
            
            # Прокручиваем наверх постепенно
            logger.info("📜 Медленно прокручиваем обратно наверх...")
            while current_position > 0:
                scroll_back = random.randint(200, 400)
                current_position -= scroll_back
                if current_position < 0:
                    current_position = 0
                driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(random.uniform(0.5, 1.0))
            
            # Финальная пауза наверху
            time.sleep(random.uniform(1.5, 2.5))
            
        except Exception as e:
            logger.debug(f"Ошибка при прокрутке: {e}")
    
    def _accept_cookies(self, driver):
        """Попытка принять cookies"""
        try:
            logger.info("🍪 Ищем и принимаем cookies...")
            
            # Пробуем через JavaScript найти и кликнуть на кнопку
            scripts = [
                # Вариант 1: Ищем кнопки с текстом Accept
                """
                var buttons = document.querySelectorAll('button, a, div[role="button"]');
                for (var i = 0; i < buttons.length; i++) {
                    var text = buttons[i].textContent.toLowerCase();
                    if (text.includes('accept') || text.includes('agree') || text.includes('consent')) {
                        buttons[i].click();
                        return true;
                    }
                }
                return false;
                """,
                # Вариант 2: Популярные селекторы cookie баннеров
                """
                var selectors = [
                    '#onetrust-accept-btn-handler',
                    '.cookie-accept',
                    '[data-testid="cookie-accept"]',
                    'button[id*="accept"]',
                    'button[class*="accept"]'
                ];
                for (var i = 0; i < selectors.length; i++) {
                    var elem = document.querySelector(selectors[i]);
                    if (elem) {
                        elem.click();
                        return true;
                    }
                }
                return false;
                """
            ]
            
            for script in scripts:
                try:
                    result = driver.execute_script(script)
                    if result:
                        logger.info("✅ Cookies приняты через JavaScript")
                        time.sleep(random.uniform(1.0, 2.0))
                        return True
                except Exception as e:
                    continue
            
            logger.debug("Кнопка cookies не найдена")
            return False
            
        except Exception as e:
            logger.debug(f"Ошибка при принятии cookies: {e}")
            return False
    
    def take_screenshot(self) -> Optional[str]:
        """
        Делает скриншот страницы Wizzair с проверкой на ошибки сессии
        
        Returns:
            Путь к файлу скриншота или None при ошибке
        """
        driver = None
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Попытка {attempt + 1}/{max_retries}: Открываем страницу: {self.url}")
                
                driver = self._get_driver()
                driver.get(self.url)
                
                # Ждем загрузки страницы (увеличенное время)
                wait_time = random.uniform(5, 8)
                logger.info(f"⏳ Ожидаем загрузки страницы ({wait_time:.1f} секунд)...")
                time.sleep(wait_time)
                
                # Пытаемся принять cookies
                self._accept_cookies(driver)
                
                # Даём время на загрузку после принятия cookies
                wait_time = random.uniform(3, 5)
                logger.info(f"⏳ Загрузка контента после cookies ({wait_time:.1f} сек)...")
                time.sleep(wait_time)
                
                # Проверяем на наличие сообщения об истечении сессии
                page_source = driver.page_source.lower()
                
                if "session has ended" in page_source or "inactivity" in page_source:
                    logger.warning(f"⚠️ Обнаружено сообщение об истечении сессии (попытка {attempt + 1})")
                    
                    # Пробуем обновить страницу
                    driver.refresh()
                    time.sleep(5)
                    
                    # Проверяем снова
                    page_source = driver.page_source.lower()
                    if "session has ended" in page_source or "inactivity" in page_source:
                        logger.warning("Сообщение всё ещё присутствует, пробуем заново...")
                        driver.quit()
                        driver = None
                        time.sleep(3)
                        continue
                
                # Имитируем поведение пользователя - прокручиваем страницу
                self._human_like_scroll(driver)
                
                # Даём дополнительное время на полную загрузку всех цен
                wait_time = random.uniform(8, 12)
                logger.info(f"⏳ Финальное ожидание загрузки цен ({wait_time:.1f} секунд)...")
                time.sleep(wait_time)
                
                # Генерируем имя файла с timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"wizzair_{Config.DEPARTURE_CITY}_{Config.ARRIVAL_CITY}_{Config.FLIGHT_DATE}_{timestamp}.png"
                filepath = os.path.join(Config.SCREENSHOTS_DIR, filename)
                
                # Делаем скриншот всей страницы
                driver.save_screenshot(filepath)
                
                logger.info(f"✅ Скриншот успешно сохранён: {filepath}")
                return filepath
                
            except Exception as e:
                logger.error(f"❌ Ошибка при создании скриншота (попытка {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    logger.info("Пробуем ещё раз через 5 секунд...")
                    time.sleep(5)
            finally:
                if driver:
                    driver.quit()
                    driver = None
        
        logger.error(f"❌ Не удалось создать скриншот после {max_retries} попыток")
        return None
    
    def get_flight_info(self) -> dict:
        """Возвращает информацию о рейсе"""
        return {
            'departure_city': Config.DEPARTURE_CITY,
            'arrival_city': Config.ARRIVAL_CITY,
            'flight_date': Config.FLIGHT_DATE,
            'checked_at': datetime.now().isoformat()
        }

