import sqlite3
connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS `job_titles` (
               `id_job_title` integer primary key NOT NULL UNIQUE,
                `name` TEXT NOT NULL);
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS `employees` (
               `id` integer primary key NOT NULL UNIQUE,
                `surname` TEXT NOT NULL,
                `name` TEXT NOT NULL,
                `phone_number` TEXT NOT NULL,
                `id_job_title` INTEGER NOT NULL,
                FOREIGN KEY(`id_job_title`) REFERENCES `job_titles`(`id_job_title`)
               );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS `clients` (
               `client_id` integer primary key NOT NULL UNIQUE,
               `organization` TEXT NOT NULL,
               `phone_number` TEXT NOT NULL
               );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS `orders` (
                `order_id` integer primary key NOT NULL UNIQUE,
                `client_id` INTEGER NOT NULL,
                `id` INTEGER NOT NULL,
                `sum` INTEGER NOT NULL,
                `date` TEXT NOT NULL,
                `result_mark` TEXT NOT NULL,
                FOREIGN KEY(`id`) REFERENCES `employees`(`id`),
                FOREIGN KEY(`client_id`) REFERENCES `clients`(`client_id`)
               );
               """)
job_titles_data = [(1, 'Менеджер'), (2, 'Разработчик'), (3, 'Аналитик'), (4, 'Дизайнер')]
cursor.executemany("INSERT OR IGNORE INTO `job_titles` (`id_job_title`, `name`) VALUES (?, ?)", job_titles_data)
employees_data = [(1, 'Иванов', 'Иван', '+89456753401', 2), (2, 'Петров', 'Петр', '+85463754910', 1), (3, 'Сидорова', 'Мария', '+85631059437', 3), (4, 'Козлов', 'Алексей', '+85743821950', 2), (5, 'Васильева', 'Ольга', '+89561490206', 4)]
cursor.executemany("INSERT OR IGNORE INTO `employees` (`id`, `surname`, `name`, `phone_number`, `id_job_title`) VALUES (?, ?, ?, ?, ?)", employees_data)
clients_data = [(1, 'Коробка', '+89147652355'), (2, 'Коробка', '+89146753438'), (3, 'Слата', '+89156935681'), (4, 'Слата', '+81159081558'), (5, 'Пятерочка', '+89450574554'), (6, 'Пятерочка', '+85467432332')]
cursor.executemany("INSERT OR IGNORE INTO `clients` (`client_id`, `organization`, `phone_number`) VALUES (?, ?, ?)", clients_data)
orders_data = [(1, 1, 3, 58432, '14.02.2026', 'Да'), (2, 3, 4, 65834, '25.01.2026', 'Да'), (3, 1, 5, 75439, '17.03.2026', 'Нет'), (4, 2, 5, 100133, '10.03.2026', 'Да'), (5, 5, 1, 94203, '13.02.2026', 'Нет'), (6, 3, 1, 103455, '11.03.2026', 'Нет')]
cursor.executemany("INSERT OR IGNORE INTO `orders` (`order_id`, `client_id`, `id`, `sum`, `date`, `result_mark`) VALUES (?, ?, ?, ?, ?, ?)", orders_data)
connection.commit()
cursor.execute("""SELECT surname, name
               FROM employees
               """)
answers = cursor.fetchall()
print("Запрос 1")
print("Фамилия имя")
for answer in answers:
    print(*answer)
cursor.execute("""SELECT organization, phone_number
               FROM clients
               """)
answers = cursor.fetchall()
print("Запрос 2")
print("Организация телефон")
for answer in answers:
    print(*answer)
cursor.execute("""SELECT sum, result_mark
               FROM orders
               """)
answers = cursor.fetchall()
print("Запрос 3")
print("Сумма статус")
for answer in answers:
    print(*answer)
cursor.execute("""SELECT date, result_mark
               FROM orders
               """)
answers = cursor.fetchall()
print("Запрос 4")
print("Дата статус")
for answer in answers:
    print(*answer)
cursor.execute("""SELECT surname, phone_number
               FROM employees
               """)
answers = cursor.fetchall()
print("Запрос 5")
print("Фамилия телефон")
for answer in answers:
    print(*answer)
cursor.execute("""SELECT SUM(sum)
               FROM orders
               """)
answer = cursor.fetchone()
print("Запрос 6")
print("Общая выручка")
print(*answer)
cursor.execute("""SELECT AVG(sum)
               FROM orders
               """)
answer = cursor.fetchone()
print("Запрос 7")
print("Средняя выручка")
print(*answer)
cursor.execute("""SELECT MAX(sum)
               FROM orders
               """)
answer = cursor.fetchone()
print("Запрос 8")
print("Максимальная выручка с клиента")
print(*answer)
cursor.execute("""SELECT e.surname, e.name
               FROM employees e 
               JOIN job_titles j ON e.id_job_title = j.id_job_title 
               WHERE j.name == 'Разработчик'
               """)
answers = cursor.fetchall()
print("Запрос 9")
print("Фамилия имя")
for answer in answers:
    print(*answer)
cursor.execute("""SELECT c.organization, c.phone_number
               FROM clients c
               JOIN orders o ON c.client_id = o.client_id
               WHERE o.result_mark = 'Да'
               """)
answers = cursor.fetchall()
print("Запрос 10")
print("Организация телефон")
for answer in answers:
    print(*answer)
cursor.execute("""SELECT organization, phone_number
               FROM clients
               WHERE organization = 'Слата'
               """)
answers = cursor.fetchall()
print("Запрос 11")
print("Организация телефон")
for answer in answers:
    print(*answer)
connection.close()
