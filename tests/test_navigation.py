import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators import LocatorNavigation


class TestNavigation:
    @pytest.mark.usefixtures("browser")
    @pytest.mark.parametrize("locator, link, required_url", [
        (LocatorNavigation.PROFILE_BUTTON, "", "login"),
        (LocatorNavigation.CONSTRUCTOR_BUTTON, "login", ""),
        (LocatorNavigation.LOGO_BUTTON, "login", ""),
    ])
    def test_navigate_navbar_button(self, browser, wait_modal, locator, link, required_url):
        """Проверяем переход кнопки Личный кабинет с главной страницы и
        переход кнопки Конструктор и кнопки с лого со страницы Личного кабинета"""
        
        # Открытие веб-сайта на странице
        browser.get(f"https://stellarburgers.nomoreparties.site/{link}")
        wait_modal()  # Ожидаем окончание анимации модального окна
        
        # Нажимаем на соответствующую кнопку (Конструктор / лого / личный кабинет)
        browser.find_element(By.XPATH, locator).click()
        time.sleep(2)  # Ожидаем перехода на новую страницу
        
        # получаем текущую ссылку на страницу
        url = browser.current_url
        
        # Проверяем полученный url страницы с required_url
        assert url == f"https://stellarburgers.nomoreparties.site/{required_url}"
    
    @pytest.mark.usefixtures("browser")
    def test_navigate_to_constructor_from_menu_homepage(self, browser, wait_modal):
        """Проверяем переходы по категориям из меню в разделе Конструктор"""
        
        # Открытие веб-сайта на главной страницы
        browser.get("https://stellarburgers.nomoreparties.site/")
        wait_modal()  # Ожидаем пока закроется модальное окно
        
        # button_categories_ingredient и names_ingredient_menu [::-1] переворачиваем, чтобы начать итерацию с конца
        # Получаем кнопки категорий
        button_categories_ingredient = browser.find_elements(
            By.XPATH, LocatorNavigation.BUTTON_CATEGORIES_INGREDIENT)[::-1]
        # Получаем название категорий в самом меню
        names_ingredient_menu = browser.find_elements(By.XPATH, LocatorNavigation.H2_MENU_INGREDIENT)[::-1]
        
        # Итерируемся по категориям и названием меню
        for button, name_ingredient in zip(button_categories_ingredient, names_ingredient_menu):
            time.sleep(1)
            button.click()  # Нажимаем на одну из категорий [Начинки, Соусы, Булки]
            
            # видимость элемента в меню
            element = WebDriverWait(browser, 10).until(EC.visibility_of(name_ingredient))
            
            # Проверяем название элемента из меню и сравниваем с названием нажатой кнопки из категорий
            assert element.text == button.text
