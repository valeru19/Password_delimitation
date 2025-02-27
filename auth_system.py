import getpass  # Для скрытого ввода пароля
import json  # Для работы с JSON-файлами
import os  # Для проверки существования файла

# Класс для хранения данных о пользователе
class User:
    def __init__(self, username, password="", is_blocked=False, password_restrictions=False):
        self.username = username  # Имя пользователя
        self.password = password  # Пароль
        self.is_blocked = is_blocked  # Заблокирован ли пользователь
        self.password_restrictions = password_restrictions  # Ограничения на пароль

    def to_dict(self):
        """Преобразует объект пользователя в словарь для сохранения в JSON."""
        return {
            "username": self.username,
            "password": self.password,
            "is_blocked": self.is_blocked,
            "password_restrictions": self.password_restrictions,
        }

    @classmethod
    def from_dict(cls, data):
        """Создает объект пользователя из словаря."""
        return cls(
            data["username"],
            data["password"],
            data["is_blocked"],
            data["password_restrictions"],
        )


# Класс для управления системой аутентификации
class AuthSystem:
    def __init__(self):
        self.users = []  # Список пользователей
        self.current_user = None  # Текущий пользователь
        self.load_users()  # Загрузка пользователей из файла

    def load_users(self):
        """Загружает пользователей из файла users.json. Если файла нет, создает администратора."""
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                users_data = json.load(file)
                self.users = [User.from_dict(user_data) for user_data in users_data]
        else:
            # Создаем администратора по умолчанию
            admin = User("ADMIN", "", False, False)
            self.users.append(admin)
            self.save_users()

    def save_users(self):
        """Сохраняет список пользователей в файл users.json."""
        with open("users.json", "w") as file:
            users_data = [user.to_dict() for user in self.users]
            json.dump(users_data, file, indent=4)

    def find_user(self, username):
        """Ищет пользователя по имени."""
        for user in self.users:
            if user.username == username:
                return user
        return None

    def authenticate(self, username, password):
        """Аутентифицирует пользователя."""
        user = self.find_user(username)
        if not user:
            print("Пользователь не найден.")
            return False
        if user.is_blocked:
            print("Учетная запись заблокирована.")
            return False
        if user.password != password:
            print("Неверный пароль.")
            return False
        self.current_user = user
        return True

    def change_password(self, old_password, new_password):
        """Меняет пароль пользователя."""
        if self.current_user.password != old_password:
            print("Неверный старый пароль.")
            return False
        if self.current_user.password_restrictions and not self.validate_password(new_password):
            print("Пароль не соответствует ограничениям.")
            return False
        self.current_user.password = new_password
        self.save_users()
        print("Пароль успешно изменен.")
        return True

    def validate_password(self, password):
        """Проверяет, соответствует ли пароль ограничениям."""
        # Пример ограничений: пароль должен быть не менее 8 символов и содержать цифры
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        return True


# Класс для режима администратора
class AdminMode:
    def __init__(self, auth_system):
        self.auth_system = auth_system

    def change_admin_password(self):
        """Меняет пароль администратора."""
        old_password = getpass.getpass("Введите старый пароль: ")
        new_password = getpass.getpass("Введите новый пароль: ")
        confirm_password = getpass.getpass("Подтвердите новый пароль: ")
        if new_password != confirm_password:
            print("Пароли не совпадают.")
            return
        if self.auth_system.current_user.password != old_password:
            print("Неверный старый пароль.")
            return
        self.auth_system.current_user.password = new_password
        self.auth_system.save_users()
        print("Пароль администратора успешно изменен.")

    def view_users(self):
        """Показывает список всех пользователей."""
        for user in self.auth_system.users:
            print(f"Имя: {user.username}, Заблокирован: {user.is_blocked}, Ограничения на пароль: {user.password_restrictions}")

    def add_user(self):
        """Добавляет нового пользователя."""
        username = input("Введите имя нового пользователя: ")
        if self.auth_system.find_user(username):
            print("Пользователь с таким именем уже существует.")
            return
        new_user = User(username)
        self.auth_system.users.append(new_user)
        self.auth_system.save_users()
        print(f"Пользователь {username} успешно добавлен.")

    def block_user(self):
        """Блокирует пользователя."""
        username = input("Введите имя пользователя для блокировки: ")
        user = self.auth_system.find_user(username)
        if not user:
            print("Пользователь не найден.")
            return
        user.is_blocked = True
        self.auth_system.save_users()
        print(f"Пользователь {username} заблокирован.")

    def toggle_password_restrictions(self):
        """Включает или отключает ограничения на пароль для пользователя."""
        username = input("Введите имя пользователя: ")
        user = self.auth_system.find_user(username)
        if not user:
            print("Пользователь не найден.")
            return
        user.password_restrictions = not user.password_restrictions
        self.auth_system.save_users()
        status = "включены" if user.password_restrictions else "отключены"
        print(f"Ограничения на пароль для {username} {status}.")


# Класс для режима обычного пользователя
class UserMode:
    def __init__(self, auth_system):
        self.auth_system = auth_system

    def change_password(self):
        """Меняет пароль пользователя."""
        old_password = getpass.getpass("Введите старый пароль: ")
        new_password = getpass.getpass("Введите новый пароль: ")
        confirm_password = getpass.getpass("Подтвердите новый пароль: ")
        if new_password != confirm_password:
            print("Пароли не совпадают.")
            return
        if not self.auth_system.change_password(old_password, new_password):
            return
        print("Пароль успешно изменен.")


# Основная программа
def main():
    auth_system = AuthSystem()

    # Вход в систему
    attempts = 3
    while attempts > 0:
        username = input("Введите имя пользователя: ")
        password = getpass.getpass("Введите пароль: ")
        if auth_system.authenticate(username, password):
            break
        attempts -= 1
        print(f"Осталось попыток: {attempts}")
    else:
        print("Превышено количество попыток. Программа завершена.")
        return

    # Режим администратора
    if auth_system.current_user.username == "ADMIN":
        admin_mode = AdminMode(auth_system)
        while True:
            print("\nРежим администратора:")
            print("1. Сменить пароль администратора")
            print("2. Просмотреть список пользователей")
            print("3. Добавить нового пользователя")
            print("4. Заблокировать пользователя")
            print("5. Включить/отключить ограничения на пароль")
            print("6. Выйти")
            choice = input("Выберите действие: ")
            if choice == "1":
                admin_mode.change_admin_password()
            elif choice == "2":
                admin_mode.view_users()
            elif choice == "3":
                admin_mode.add_user()
            elif choice == "4":
                admin_mode.block_user()
            elif choice == "5":
                admin_mode.toggle_password_restrictions()
            elif choice == "6":
                break
            else:
                print("Неверный выбор.")
    else:
        # Режим обычного пользователя
        user_mode = UserMode(auth_system)
        while True:
            print("\nРежим пользователя:")
            print("1. Сменить пароль")
            print("2. Выйти")
            choice = input("Выберите действие: ")
            if choice == "1":
                user_mode.change_password()
            elif choice == "2":
                break
            else:
                print("Неверный выбор.")


if __name__ == "__main__":
    main()