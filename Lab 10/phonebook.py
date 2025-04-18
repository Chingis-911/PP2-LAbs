import psycopg2
import csv
from config import load_config

def create_tables():
    """Создание таблицы phonebook в базе данных"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50),
            phone VARCHAR(20) NOT NULL UNIQUE,
            email VARCHAR(100),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        """,
    )
    
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
        print("Таблица phonebook успешно создана")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def insert_from_csv(filename):
    """Добавление данных из CSV файла"""
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # Пропускаем заголовок
                    for row in reader:
                        cur.execute(
                            """INSERT INTO phonebook (first_name, last_name, phone, email)
                            VALUES (%s, %s, %s, %s)""",
                            row
                        )
                print(f"Данные из файла {filename} успешно добавлены")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def insert_from_console():
    """Добавление данных через консоль"""
    print("\nДобавление нового контакта:")
    first_name = input("Имя: ")
    last_name = input("Фамилия (необязательно): ")
    phone = input("Телефон: ")
    email = input("Email (необязательно): ")
    
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO phonebook (first_name, last_name, phone, email)
                    VALUES (%s, %s, %s, %s)""",
                    (first_name, last_name, phone, email)
                )
                print("Контакт успешно добавлен")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def update_contact():
    """Обновление данных контакта"""
    print("\nОбновление контакта")
    phone = input("Введите телефон контакта для обновления: ")
    
    print("Что вы хотите изменить?")
    print("1. Имя")
    print("2. Фамилию")
    print("3. Телефон")
    print("4. Email")
    choice = input("Выберите пункт (1-4): ")
    
    if choice == '1':
        field = 'first_name'
        new_value = input("Введите новое имя: ")
    elif choice == '2':
        field = 'last_name'
        new_value = input("Введите новую фамилию: ")
    elif choice == '3':
        field = 'phone'
        new_value = input("Введите новый телефон: ")
    elif choice == '4':
        field = 'email'
        new_value = input("Введите новый email: ")
    else:
        print("Неверный выбор")
        return
    
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""UPDATE phonebook 
                    SET {field} = %s
                    WHERE phone = %s""",
                    (new_value, phone)
                )
                if cur.rowcount == 0:
                    print("Контакт с таким телефоном не найден")
                else:
                    print("Контакт успешно обновлен")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def query_contacts():
    """Поиск контактов"""
    print("\nПоиск контактов по:")
    print("1. Имени")
    print("2. Фамилии")
    print("3. Телефону")
    print("4. Email")
    print("5. Показать все контакты")
    choice = input("Выберите пункт (1-5): ")
    
    if choice == '1':
        field = 'first_name'
        value = input("Введите имя для поиска: ")
    elif choice == '2':
        field = 'last_name'
        value = input("Введите фамилию для поиска: ")
    elif choice == '3':
        field = 'phone'
        value = input("Введите телефон для поиска: ")
    elif choice == '4':
        field = 'email'
        value = input("Введите email для поиска: ")
    elif choice == '5':
        field = None
    else:
        print("Неверный выбор")
        return
    
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if field:
                    cur.execute(
                        f"""SELECT id, first_name, last_name, phone, email 
                        FROM phonebook 
                        WHERE {field} = %s
                        ORDER BY first_name""",
                        (value,)
                    )
                else:
                    cur.execute(
                        """SELECT id, first_name, last_name, phone, email 
                        FROM phonebook 
                        ORDER BY first_name"""
                    )
                
                rows = cur.fetchall()
                
                if not rows:
                    print("Контакты не найдены")
                else:
                    print("\nНайденные контакты:")
                    for row in rows:
                        print(f"ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Телефон: {row[3]}, Email: {row[4]}")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def delete_contact():
    """Удаление контакта"""
    print("\nУдаление контакта по:")
    print("1. Имени")
    print("2. Телефону")
    choice = input("Выберите пункт (1-2): ")
    
    if choice == '1':
        field = 'first_name'
        value = input("Введите имя контакта для удаления: ")
    elif choice == '2':
        field = 'phone'
        value = input("Введите телефон контакта для удаления: ")
    else:
        print("Неверный выбор")
        return
    
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""DELETE FROM phonebook 
                    WHERE {field} = %s""",
                    (value,)
                )
                if cur.rowcount == 0:
                    print("Контакты не найдены")
                else:
                    print(f"Удалено {cur.rowcount} контактов")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def main_menu():
    """Главное меню"""
    while True:
        print("\nТелефонная книга - Главное меню")
        print("1. Создать таблицу phonebook")
        print("2. Добавить контакты из CSV файла")
        print("3. Добавить контакт вручную")
        print("4. Обновить контакт")
        print("5. Найти контакты")
        print("6. Удалить контакт")
        print("7. Выход")
        
        choice = input("Выберите действие (1-7): ")
        
        if choice == '1':
            create_tables()
        elif choice == '2':
            filename = input("Введите имя CSV файла (например: contacts.csv): ")
            insert_from_csv(filename)
        elif choice == '3':
            insert_from_console()
        elif choice == '4':
            update_contact()
        elif choice == '5':
            query_contacts()
        elif choice == '6':
            delete_contact()
        elif choice == '7':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор, попробуйте снова")

if __name__ == '__main__':
    main_menu()