import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators import LocatorRegistration, LocatorAuthorization, LocatorProfile


class TestRegistration:
    @staticmethod
    def input_registration_form(browser, name, email, password):
        """ Вносим переданные данные в форму регистрации """
        
        # Получаем тег input для ввода имени
        name_input = browser.find_element(By.XPATH, LocatorRegistration.NAME_INPUT)
        # Получаем тег input для ввода email
        email_input = browser.find_element(By.XPATH, LocatorRegistration.EMAIL_INPUT)
        # Получаем тег input для ввода пароля
        pass_input = browser.find_element(By.XPATH, LocatorRegistration.PASSWORD_INPUT)
        
        # Вносим данные в форму
        for _input, data in zip((name_input, email_input, pass_input), (name, email, password)):
            _input.clear()  # Очищаем поле
            _input.send_keys(data)  # Вставляем данные в поле input
        
        # Кликаем кнопку submit в форме
        browser.find_element(By.XPATH, LocatorRegistration.SUBMIT_BUTTON).click()
        time.sleep(2)
    
    @pytest.mark.usefixtures("browser")
    def test_registration_correct_data(self, browser, wait_modal, authorization, valid_registration_credentials):
        """ Проверка успешной регистрации с корректными данными """
        
        # Открытие веб-сайта на главной страницы
        browser.get("https://stellarburgers.nomoreparties.site/register")
        wait_modal()  # Ожидаем окончание анимации модального окна
        
        name = valid_registration_credentials["name"]
        email = valid_registration_credentials["email"]
        password = valid_registration_credentials["password"]
        
        # Вносим некорректные данные в форму регистрации
        self.input_registration_form(browser, name, email, password)
        
        wait_modal()  # Ожидаем окончание анимации модального окна
        
        # Авторизовываемся под созданным аккаунтом
        authorization(LocatorAuthorization.EMAIL_INPUT, LocatorAuthorization.PASSWORD_INPUT,
                      LocatorAuthorization.SUBMIT_BUTTON, email, password)
        
        # После авторизации открываем страницу в профиля
        browser.get("https://stellarburgers.nomoreparties.site/account")
        time.sleep(1)
        
        # Получаем данные об имени и логине
        name_profile = browser.find_element(By.XPATH, LocatorProfile.NAME_PROFILE).get_attribute("value")
        login_profile = browser.find_element(By.XPATH, LocatorProfile.LOGIN_PROFILE).get_attribute("value")
        
        # Проверка успешной регистрации. Имя профиля и login должны совпадать с данными name и email при регистрации
        assert name_profile == name and login_profile == email
    
    @pytest.mark.usefixtures("browser")
    def test_registration_incorrect_password(self, browser, wait_modal, invalid_registration_credentials):
        """ Проверка вывода ошибки "Некорректный пароль" """
        
        # Открытие веб-сайта на главной страницы
        browser.get("https://stellarburgers.nomoreparties.site/register")
        # Ожидаем окончание анимации модального окна
        wait_modal()
        
        # Вносим некорректные данные в форму регистрации
        self.input_registration_form(browser, invalid_registration_credentials["name"],
                                     invalid_registration_credentials["email"],
                                     invalid_registration_credentials["password"])
        
        # Ждем подгрузки элемента с ошибкой
        error = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, LocatorRegistration.ERROR_MESSAGE))
        )
        
        # Проверка наличие ошибки при вводе некорректного пароля. error.text должен быть равен "Некорректный пароль"
        assert error is not None and error.text == "Некорректный пароль"
