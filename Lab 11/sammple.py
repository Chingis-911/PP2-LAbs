import psycopg2
import csv
import re
from tabulate import tabulate

# Database connection function
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="suppliers",
            user="postgres",
            password="Kasablanka2006",
            port=5432,
            options='-c client_encoding=UTF8'
        )
        conn.set_client_encoding('UTF8')
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Initialize database
def initialize_database():
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS phonebook (
                user_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                surname VARCHAR(255) NOT NULL, 
                phone VARCHAR(255) NOT NULL UNIQUE
            )""")
            conn.commit()
            cur.close()
        except Exception as e:
            print(f"Initialization error: {e}")
        finally:
            conn.close()

# 1. Function that returns all records based on a pattern
def search_by_pattern(pattern):
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM phonebook 
                WHERE name ILIKE %s OR surname ILIKE %s OR phone ILIKE %s
                ORDER BY user_id
            """, (f'%{pattern}%', f'%{pattern}%', f'%{pattern}%'))
            rows = cur.fetchall()
            if rows:
                print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))
            else:
                print("No records found matching the pattern.")
        except Exception as e:
            print(f"Search error: {e}")
        finally:
            cur.close()
            conn.close()

# 2. Procedure to insert new user or update phone if exists
def upsert_user(name, phone, surname=""):
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            # Check if user exists
            cur.execute("SELECT * FROM phonebook WHERE name = %s AND surname = %s", (name, surname))
            if cur.fetchone():
                cur.execute("""
                    UPDATE phonebook SET phone = %s 
                    WHERE name = %s AND surname = %s
                """, (phone, name, surname))
                print(f"Updated phone for {name} {surname}")
            else:
                cur.execute("""
                    INSERT INTO phonebook (name, surname, phone) 
                    VALUES (%s, %s, %s)
                """, (name, surname, phone))
                print(f"Added new user {name} {surname}")
            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            print(f"Phone {phone} already exists for another user")
        except Exception as e:
            conn.rollback()
            print(f"Upsert error: {e}")
        finally:
            cur.close()
            conn.close()

# 3. Phone validation function
def is_valid_phone(phone):
    return re.match(r'^\+?\d{6,}$', phone) is not None

# 3. Procedure to insert many new users with validation
def insert_many_users(user_list):
    conn = connect_to_db()
    if not conn:
        return []
    
    incorrect_data = []
    valid_count = 0
    
    try:
        cur = conn.cursor()
        for entry in user_list:
            if len(entry) == 2:
                name, phone = entry
                surname = ""
            elif len(entry) == 3:
                name, surname, phone = entry
            else:
                incorrect_data.append(entry)
                continue
            
            if not is_valid_phone(phone):
                incorrect_data.append(entry)
                continue
            
            try:
                # Check if user exists
                cur.execute("SELECT * FROM phonebook WHERE name = %s AND surname = %s", (name, surname))
                if cur.fetchone():
                    cur.execute("""
                        UPDATE phonebook SET phone = %s 
                        WHERE name = %s AND surname = %s
                    """, (phone, name, surname))
                else:
                    cur.execute("""
                        INSERT INTO phonebook (name, surname, phone) 
                        VALUES (%s, %s, %s)
                    """, (name, surname, phone))
                valid_count += 1
            except psycopg2.IntegrityError:
                incorrect_data.append(entry)
                conn.rollback()
            except Exception as e:
                incorrect_data.append(entry)
                print(f"Error processing {entry}: {e}")
                conn.rollback()
        
        conn.commit()
        print(f"Successfully processed {valid_count} users")
        if incorrect_data:
            print("\nIncorrect data:")
            print(tabulate(incorrect_data, headers=["Name", "Surname", "Phone"], tablefmt='fancy_grid'))
    
    except Exception as e:
        print(f"Bulk insert error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    
    return incorrect_data

# 4. Function for paginated query
def query_with_pagination(limit=10, offset=0):
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM phonebook 
                ORDER BY user_id 
                LIMIT %s OFFSET %s
            """, (limit, offset))
            rows = cur.fetchall()
            
            if rows:
                print(f"Page {offset//limit + 1} ({len(rows)} records):")
                print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))
            else:
                print("No records found for this page.")
        except Exception as e:
            print(f"Pagination error: {e}")
        finally:
            cur.close()
            conn.close()

# 5. Procedure to delete by username or phone
def delete_by_identifier(identifier):
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                DELETE FROM phonebook 
                WHERE name = %s OR phone = %s 
                RETURNING *
            """, (identifier, identifier))
            deleted = cur.fetchall()
            conn.commit()
            
            if deleted:
                print(f"Deleted {len(deleted)} record(s):")
                print(tabulate(deleted, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))
            else:
                print("No records found matching the identifier.")
        except Exception as e:
            print(f"Delete error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

# Interactive menu system
def main_menu():
    initialize_database()
    
    while True:
        print("\nPhonebook Management System")
        print("1. Search by pattern")
        print("2. Add/Update user")
        print("3. Bulk import users")
        print("4. View paginated results")
        print("5. Delete user")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            pattern = input("Enter search pattern: ")
            search_by_pattern(pattern)
        
        elif choice == "2":
            name = input("Enter name: ").strip()
            surname = input("Enter surname (optional): ").strip()
            phone = input("Enter phone: ").strip()
            upsert_user(name, phone, surname if surname else "")
        
        elif choice == "3":
            print("\nBulk Import Options:")
            print("1. Enter data manually")
            print("2. Import from CSV file")
            sub_choice = input("Enter choice (1-2): ").strip()
            
            if sub_choice == "1":
                users = []
                print("\nEnter users (format: name,surname,phone or name,phone)")
                print("Type 'done' when finished")
                while True:
                    entry = input("> ").strip()
                    if entry.lower() == 'done':
                        break
                    parts = [part.strip() for part in entry.split(',')]
                    if 2 <= len(parts) <= 3:
                        users.append(tuple(parts))
                    else:
                        print("Invalid format. Use 'name,phone' or 'name,surname,phone'")
                insert_many_users(users)
            
            elif sub_choice == "2":
                filepath = input("Enter CSV file path: ").strip()
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        users = [tuple(row) for row in reader if 2 <= len(row) <= 3]
                    insert_many_users(users)
                except Exception as e:
                    print(f"File error: {e}")
        
        elif choice == "4":
            try:
                limit = int(input("Records per page (default 10): ") or 10)
                page = int(input("Page number (default 1): ") or 1)
                offset = (page - 1) * limit
                query_with_pagination(limit, offset)
            except ValueError:
                print("Please enter valid numbers")
        
        elif choice == "5":
            identifier = input("Enter name or phone to delete: ").strip()
            delete_by_identifier(identifier)
        
        elif choice == "6":
            print("Exiting program...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()