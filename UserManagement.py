import hashlib
import uuid

class User:
    """
    Базовый класс, представляющий пользователя.
    """
    users = []  # Список для хранения всех пользователей

    def __init__(self, username, email, password):
        # Проверка уникальности имени пользователя
        if any(u.username == username for u in User.users):
            raise ValueError(f"Пользователь с именем {username} уже существует.")
        self.username = username
        self.email = email
        self.password = User.hash_password(password)
        User.users.append(self)

    @staticmethod
    def hash_password(password):
        """Хеширование пароля"""
        salt = uuid.uuid4().hex
        hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
        return f"{salt}${hashed}"

    @staticmethod
    def check_password(stored_password, provided_password):
        """Проверка пароля"""
        salt, hashed = stored_password.split('$')
        return hashed == hashlib.sha256((salt + provided_password).encode('utf-8')).hexdigest()

    def get_details(self):
        return f"Пользователь: {self.username}, Email: {self.email}"


class Customer(User):
    """
    Класс, представляющий клиента, наследующий класс User.
    """
    def __init__(self, username, email, password, address):
        super().__init__(username, email, password)
        self.address = address

    def get_details(self):
        return f"Клиент: {self.username}, Email: {self.email}, Адрес: {self.address}"


class Admin(User):
    """
    Класс, представляющий администратора, наследующий класс User.
    """
    def __init__(self, username, email, password, admin_level):
        super().__init__(username, email, password)
        self.admin_level = admin_level

    def get_details(self):
        return f"Администратор: {self.username}, Email: {self.email}, Уровень: {self.admin_level}"

    @staticmethod
    def list_users():
        """Выводит список всех пользователей"""
        return [u.get_details() for u in User.users]

    @staticmethod
    def delete_user(username):
        """Удаляет пользователя по имени пользователя"""
        user = next((u for u in User.users if u.username == username), None)
        if user:
            User.users.remove(user)
            return f"Пользователь {username} удален."
        return f"Пользователь {username} не найден."


class AuthenticationService:
    """
    Сервис для управления регистрацией и аутентификацией пользователей.
    """
    def __init__(self):
        self.current_user = None
        self.session_token = None

    def register(self, user_class, username, email, password, *args):
        """Регистрация нового пользователя"""
        try:
            user = user_class(username, email, password, *args)
            return f"{user_class.__name__} {username} успешно зарегистрирован."
        except ValueError as e:
            return str(e)

    def login(self, username, password):
        """Аутентификация пользователя"""
        user = next((u for u in User.users if u.username == username), None)
        if not user:
            return f"Пользователь {username} не найден."
        if not User.check_password(user.password, password):
            return "Неверный пароль."
        self.current_user = user
        self.session_token = uuid.uuid4().hex
        return f"{username} успешно вошел в систему. Токен сессии: {self.session_token}"

    def logout(self):
        """Выход пользователя из системы"""
        if self.current_user:
            name = self.current_user.username
            self.current_user = None
            self.session_token = None
            return f"{name} вышел из системы."
        return "Нет активного пользователя."

    def get_current_user(self):
        """Возвращает текущего вошедшего пользователя"""
        if self.current_user:
            return self.current_user.get_details()
        return "Нет активного пользователя."


if __name__ == "__main__":
    auth_service = AuthenticationService()

    print("Регистрация пользователей:")
    print("-----------------------------------------------------------")
    print(auth_service.register(Customer, "ivan", "ivan@mail.com", "12345", "Москва, ул. Ленина"))
    print(auth_service.register(Admin, "admin1", "admin@mail.com", "adminpass", 1))
    print(auth_service.register(Customer, "maria", "maria@mail.com", "54321", "СПб, ул. Пушкина"))
    print("===========================================================\n")

    print("Попытка зарегистрировать существующего пользователя:")
    print("-----------------------------------------------------------")
    print(auth_service.register(Customer, "ivan", "ivan2@mail.com", "11111", "Казань"))
    print("===========================================================\n")

    print("Аутентификация:")
    print("-----------------------------------------------------------")
    print(auth_service.login("ivan", "12345"))
    print(auth_service.get_current_user())
    print("===========================================================\n")

    print("Выход:")
    print("-----------------------------------------------------------")
    print(auth_service.logout())
    print(auth_service.get_current_user())
    print("===========================================================\n")

    print("Вход админа и управление пользователями:")
    print("-----------------------------------------------------------")
    print(auth_service.login("admin1", "adminpass"))
    if isinstance(auth_service.current_user, Admin):
        print("Список всех пользователей:")
        for u in Admin.list_users():
            print(u)
        print(Admin.delete_user("maria"))
        print("После удаления:")
        for u in Admin.list_users():
            print(u)
    print("===========================================================\n")
