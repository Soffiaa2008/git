import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    # Функция create_db() создает базу данных users.db и инициализирует схему
    create_db()
    yield
    # Очистка после выполнения тестов
    os.remove('users.db')

def test_create_db(setup_database):
    """Тест создания базы данных и таблицы пользователей."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Проверяем, существует ли таблица users
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_add_user_with_existing_username(setup_database):
    """Тест добавления пользователя с существующим логином."""
    add_user('testuser', 'testuser@example.com', 'password123')
    result = add_user('testuser', 'another@example.com', 'newpassword')
    assert not result, "Не должно быть добавлено два пользователя с одинаковым логином."

def test_authenticate_user(setup_database):
    """Тест успешной аутентификации пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    assert authenticate_user('testuser', 'password123')

def test_authenticate_nonexistent_user(setup_database):
    """Тест аутентификации несуществующего пользователя."""
    assert not authenticate_user('unknownuser', 'unknownpassword')

def test_authenticate_user_with_incorrect_password(setup_database):
    """Тест аутентификации пользователя с неправильным паролем."""
    add_user('testuser', 'testuser@example.com', 'password123')
    assert not authenticate_user('testuser', 'wrongpassword')

def test_display_users(setup_database):
    """Тест отображения списка пользователей."""
    add_user('testuser1', 'testuser1@example.com', 'password123')
    add_user('testuser2', 'testuser2@example.com', 'password456')
    expected_output = [
        ('testuser1', 'testuser1@example.com'),
        ('testuser2', 'testuser2@example.com')
    ]
