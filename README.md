# Password_delimitation
Документация

1. Описание программы
Программа реализует систему разграничения доступа пользователей на основе парольной аутентификации. Она поддерживает два режима работы:

Режим администратора: Позволяет управлять пользователями (добавлять, блокировать, настраивать ограничения на пароли).

Режим обычного пользователя: Позволяет изменять пароль.

2. Требования
Python 3.x

Модули: getpass, json, os

3. Функционал
Аутентификация: Пользователь вводит имя и пароль. Пароль скрывается символами *.

Режим администратора:

Смена пароля администратора.

Просмотр списка пользователей.

Добавление нового пользователя.

Блокировка пользователя.

Включение/отключение ограничений на пароли.

Режим пользователя:

Смена пароля.

Сохранение данных: Данные о пользователях сохраняются в файл users.json.

4. Запуск программы
Сохраните код в файл auth_system.py.

Запустите программу:

bash
Copy
python auth_system.py
По умолчанию создается администратор с именем ADMIN и пустым паролем.

5. Пример использования
Войдите как администратор:

Имя: ADMIN

Пароль: (оставьте пустым)

Добавьте новых пользователей и настройте их параметры.

Войдите как обычный пользователь и смените пароль.

6. Ограничения
Пароль должен содержать не менее 8 символов и хотя бы одну цифру (если включены ограничения).

После трех неудачных попыток ввода пароля программа завершает работу.

7. Доработка
Добавьте больше ограничений на пароли (например, обязательное использование специальных символов).

Реализуйте графический интерфейс с помощью библиотеки tkinter.
