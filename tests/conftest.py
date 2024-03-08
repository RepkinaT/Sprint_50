import time

import pytest
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", type=str)


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    driver = None
    if browser_name == "firefox":
        driver = wd.Firefox()
    elif browser_name == "chrome":
        driver = wd.Chrome()
    
    yield driver
    
    driver.quit()


@pytest.fixture
def wait_modal(browser):
    # Фикстура для ожидания модального окна
    def _wait_modal():
        # Ждём когда прогрузится модальное окно с анимацией.
        modal_element = WebDriverWait(browser, 1000000).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Modal_modal_overlay__x2ZCr"))
        )
        WebDriverWait(browser, 1000000).until(
            EC.invisibility_of_element(modal_element)  # Ожидаем сокрытие модального окна
        )
        time.sleep(0.5)
    
    return _wait_modal


@pytest.fixture
def valid_login_credentials():
    # Фикстура корректных данных для авторизации
    return {
        "email": "testtestov19999@yandex.ru",
        "password": "123456789"
    }


@pytest.fixture
def valid_registration_credentials():
    # Фикстура корректных данных для регистрации
    return {
        "name": "Test Validov",
        "email": "testtvalivov1999@example.com",
        "password": "46587948978416389"
    }


@pytest.fixture
def invalid_registration_credentials():
    # Фикстура некорректных данных для регистрации
    return {
        "name": "Test Testov",
        "email": "invalid@example.com",
        "password": "89"
    }


@pytest.fixture
def authorization(browser):
    # Фикстура для авторизации
    def _authorization(locator_email, locator_password, locator_button, email, password):
        # Получаем тег input для ввода email
        email_input = browser.find_element(By.XPATH, locator_email)
        # Получаем тег input для ввода пароля
        pass_input = browser.find_element(By.XPATH, locator_password)
        
        # Вносим данные в форму
        for _input, data in zip((email_input, pass_input), (email, password)):
            _input.clear()  # Очищаем поле
            _input.send_keys(data)  # Вставляем данные в поле input
        
        # Нажимаем кнопку войти
        submit_button = browser.find_element(By.XPATH, locator_button)
        submit_button.click()
        
        WebDriverWait(browser, 10).until(
            EC.staleness_of(submit_button)
        )  # Ждём перехода на другую страницу
    
    return _authorization
