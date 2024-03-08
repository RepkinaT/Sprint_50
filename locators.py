class LocatorRegistration:
    # Форма регистрации
    FORM = "//form[contains(@class, 'Auth_form__3qKeq')]"
    
    # Поля Input формы регистрации
    NAME_INPUT = FORM + "//fieldset[1]//input"  # name
    EMAIL_INPUT = FORM + "//fieldset[2]//input"  # email
    PASSWORD_INPUT = FORM + "//fieldset[3]//input"  # password
    
    # Кнопка submit в форме регистрации
    SUBMIT_BUTTON = FORM + "//button"
    
    # тег p в котором выводится ошибка пароля
    ERROR_MESSAGE = "//p[contains(@class, 'input__error')]"


class LocatorAuthorization:
    # Форма регистрации
    FORM = "//form[contains(@class, 'Auth_form__3qKeq')]"
    
    # Поля Input формы регистрации
    EMAIL_INPUT = FORM + "//fieldset[1]//input"  # email
    PASSWORD_INPUT = FORM + "//fieldset[2]//input"  # password
    
    # Кнопка отправки формы
    SUBMIT_BUTTON = FORM + "//button"
    
    # Кнопка Войти на странице регистрации
    REGISTER_BUTTON = "//a[contains(@class, 'Auth_link__1fOlj')]"
    # Кнопка Войти на странице восстановления пароля
    FORGOT_PASSWORD_BUTTON = "//a[contains(@class, 'Auth_link__1fOlj')]"
    # Кнопка Личный кабинет на главной станице
    PROFILE_BUTTON = "//button[contains(@class, 'button_button__33qZ0')]"


class LocatorNavigation:
    # Кнопка Конструктор в navbar
    CONSTRUCTOR_BUTTON = "(//a[contains(@class, 'AppHeader_header__link__3D_hX')])[1]"
    # Кнопка Личный кабинет в navbar
    PROFILE_BUTTON = "(//a[contains(@class, 'AppHeader_header__link__3D_hX')])[3]"
    # Кнопка с лого в navbar
    LOGO_BUTTON = "//div[@class='AppHeader_header__logo__2D0X2']/a"
    
    # Секция с ингредиентами и меню
    SECTION_INGREDIENTS = "//section[contains(@class, 'BurgerIngredients_ingredients__1N8v2')]"
    # Кнопки с категориями ингредиентов
    BUTTON_CATEGORIES_INGREDIENT = SECTION_INGREDIENTS + "//div[1]//div"
    # Название ингредиентов в самом меню
    H2_MENU_INGREDIENT = SECTION_INGREDIENTS + "//div[2]//h2"


class LocatorProfile:
    # Кнопка выхода из профиля
    BUTTON_EXIT = "//button[contains(@class, 'Account_button__14Yp3')]"
    
    UL = "//ul[contains(@class, 'Profile_profileList__3vTor')]"
    # Поле input в личном кабинете, который соответствует имени
    NAME_PROFILE = UL + "/li[1]//input"
    # Поле input в личном кабинете, который соответствует логину/email
    LOGIN_PROFILE = UL + "/li[2]//input"
