import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators import LocatorAuthorization, LocatorProfile


class TestAuthorization:
    @pytest.mark.usefixtures("browser")
    @pytest.mark.parametrize("css_selector, link", [
        (LocatorAuthorization.REGISTER_BUTTON, "register"),  # Переход со страницы регистрации
        (LocatorAuthorization.FORGOT_PASSWORD_BUTTON, "forgot-password"),  # Переход со страницы регистрации
        (LocatorAuthorization.PROFILE_BUTTON, ""),  # Переход с главной страницы
        (None, "login"),  # Без перехода
    ])
    def test_successful_authorization(self, browser, wait_modal, authorization, valid_login_credentials,
                                      css_selector, link):
        """Проверяем удачную авторизацию при переходе с разных страниц сайта"""
        
        # Открытие веб-сайта
        browser.get(f"https://stellarburgers.nomoreparties.site/{link}")
        # Ожидаем окончание анимации модального окна
        wait_modal()
        
        # Проверяем нужен ли переход на страницу входа по кнопке
        if css_selector is not None:
            # Нажимаем на кнопку Войти или Личный кабинет
            browser.find_element(By.XPATH, css_selector).click()
        
        # Проходим авторизацию
        authorization(LocatorAuthorization.EMAIL_INPUT, LocatorAuthorization.PASSWORD_INPUT,
                      LocatorAuthorization.SUBMIT_BUTTON,
                      valid_login_credentials["email"], valid_login_credentials["password"])
        
        # Открытие веб-сайта на странице профиля
        browser.get("https://stellarburgers.nomoreparties.site/account")
        time.sleep(2)  # Ожидаем перехода на новую страницу
        
        # Проверяем удачную авторизацию. Текущий url страницы должен быть равен ../account/profile (страницы профиля)
        assert browser.current_url == "https://stellarburgers.nomoreparties.site/account/profile"
    
    @pytest.mark.usefixtures("browser")
    def test_logout_from_account_by_button(self, browser, wait_modal, authorization, valid_login_credentials):
        """Проверяем выход по кнопке из личного кабинета"""
        
        # Открытие веб-сайта
        browser.get(f"https://stellarburgers.nomoreparties.site/login")
        wait_modal()  # Ожидаем окончание анимации модального окна
        
        # Проходим авторизацию
        authorization(LocatorAuthorization.EMAIL_INPUT, LocatorAuthorization.PASSWORD_INPUT,
                      LocatorAuthorization.SUBMIT_BUTTON,
                      valid_login_credentials["email"], valid_login_credentials["password"])
        
        # Переходим на страницу профиля
        browser.get("https://stellarburgers.nomoreparties.site/account")
        wait_modal()  # Ожидаем окончание анимации модального окна
        
        # Нажимаем на кнопку выхода из профиля
        exit_profile_button = browser.find_element(By.XPATH, LocatorProfile.BUTTON_EXIT)
        exit_profile_button.click()
        
        WebDriverWait(browser, 10).until(
            EC.staleness_of(exit_profile_button)
        )  # Ждём перехода на главную страницу
        
        # Открытие веб-сайта на странице входа
        browser.get("https://stellarburgers.nomoreparties.site/account")
        time.sleep(2)
        
        # Проверяем выход из аккаунта. Url страницы должен быть равен ../login (страницы авторизации)
        assert browser.current_url == "https://stellarburgers.nomoreparties.site/login"
