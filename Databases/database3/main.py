import sqlite3
connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS `уровень_обучения`")
cursor.execute("DROP TABLE IF EXISTS `направления`")
cursor.execute("DROP TABLE IF EXISTS `типы_обучения`")
cursor.execute("DROP TABLE IF EXISTS `студенты`")
cursor.execute("""CREATE TABLE IF NOT EXISTS `уровень_обучения` (
               `id_уровня` integer primary key NOT NULL UNIQUE,
               `название` TEXT NOT NULL
               );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS `направления` (
               `id_направления` integer primary key NOT NULL UNIQUE,
               `название` TEXT NOT NULL
               );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS `типы_обучения` (
               `id_типа` integer primary key NOT NULL UNIQUE,
               `название` TEXT NOT NULL
               );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS `студенты` (
               `id_студента` integer primary key NOT NULL UNIQUE,
               `id_уровня` INTEGER NOT NULL,
               `id_направления` INTEGER NOT NULL,
               `id_типа_обучения` INTEGER NOT NULL,
               `фамилия` TEXT NOT NULL,
               `имя` TEXT NOT NULL,
               `отчество` TEXT NOT NULL,
               `средний_балл` INTEGER NOT NULL,
               FOREIGN KEY (`id_уровня`) REFERENCES `уровень_обучения`(`id_уровня`),
               FOREIGN KEY (`id_направления`) REFERENCES `направления`(`id_направления`),
               FOREIGN KEY (`id_типа_обучения`) REFERENCES `типы_обучения`(`id_типа`)
               );
               """)
data = open('data.txt', 'r', encoding = 'utf-8')
new_table = True
levels_df = []
majors_df = []
types_df = []
students_df = []
lines = data.readlines()
for line in lines:
    line = line[:-1]
    if new_table:
        current_table = line
        new_table = False
    elif line == 'table':
        new_table = True
    elif current_table == 'уровень_обучения':
        levels_df.append(line.split(','))
    elif current_table == 'направления':
        majors_df.append(line.split(','))
    elif current_table == 'типы_обучения':
        types_df.append(line.split(','))
    elif current_table == 'студенты':
        students_df.append(line.split(','))
cursor.executemany("INSERT OR IGNORE INTO `уровень_обучения` (`id_уровня`, `название`) VALUES (?, ?)", levels_df)
cursor.executemany("INSERT OR IGNORE INTO `направления` (`id_направления`, `название`) VALUES (?, ?)", majors_df)
cursor.executemany("INSERT OR IGNORE INTO `типы_обучения` (`id_типа`, `название`) VALUES (?, ?)", types_df)
cursor.executemany("INSERT OR IGNORE INTO `студенты` (`id_студента`, `id_уровня`, `id_направления`, `id_типа_обучения`, `фамилия`, `имя`, `отчество`, `средний_балл`) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", students_df)
cursor.execute("""SELECT COUNT(с.`id_студента`)
               FROM `студенты` с
               """)
answer = cursor.fetchone()
print('Запрос 1')
print(f'Количество студентов: {answer[0]}')
cursor.execute("""SELECT н.`название`, COUNT(`id_студента`)
               FROM `студенты` с
               JOIN `направления` н ON с.`id_направления` = н.`id_направления`
               GROUP BY н.`id_направления`
               """)
answer = cursor.fetchall()
print('Запрос 2')
print(answer)
cursor.execute("""SELECT т.`название`, COUNT(`id_студента`)
               FROM `студенты` с
               JOIN `типы_обучения` т ON с.`id_типа_обучения` = т.`id_типа`
               GROUP BY т.`id_типа`
               """)
answer = cursor.fetchall()
print('Запрос 3')
print(answer)
cursor.execute("""SELECT MAX(`средний_балл`), MIN(`средний_балл`), AVG(`средний_балл`)
               FROM `студенты` с
               """)
answer = cursor.fetchone()
print('Запрос 4')
print(f'Максимальный балл: {answer[0]}, Минимальный балл: {answer[1]}, Средний балл: {answer[2]}')
cursor.execute("""SELECT у.`название`, т.`название`, н.`название`, AVG(с.`средний_балл`)
               FROM `студенты` с
               JOIN `уровень_обучения` у ON с.`id_уровня` = у.`id_уровня`
               JOIN `типы_обучения` т ON с.`id_типа_обучения` = т.`id_типа`
               JOIN `направления` н ON с.`id_направления` = н.`id_направления`
               GROUP BY у.`id_уровня`, т.`id_типа`, н.`id_направления`
               """)
answer = cursor.fetchall()
print('Запрос 5')
print(answer)
cursor.execute("""SELECT с.`фамилия`, с.`имя`, с.`отчество`, с.`средний_балл`
               FROM `студенты` с
               JOIN `направления` н ON с.`id_направления` = н.`id_направления`
               JOIN `типы_обучения` т ON с.`id_типа_обучения` = т.`id_типа`
               WHERE н.`название` = 'Прикладная информатика'
               AND т.`название` = 'Очный'
               ORDER BY с.`средний_балл` DESC
               LIMIT 5
               """)
answer = cursor.fetchall()
print('Запрос 6')
print(answer)
cursor.execute("""SELECT с.`фамилия`, с.`имя`, с.`отчество`
               FROM `студенты` с
               CROSS JOIN `студенты` с2
               WHERE с.`фамилия` = с2.`фамилия`
               AND с.`id_студента` < с2.`id_студента`
               """)
answer = cursor.fetchall()
print('Запрос 7')
print(answer)
cursor.execute("""SELECT с.`фамилия`, с.`имя`, с.`отчество`
               FROM `студенты` с
               CROSS JOIN `студенты` с2
               WHERE с.`фамилия` = с2.`фамилия`
               AND с.`имя` = с2.`имя`
               AND с.`отчество` = с2.`отчество`
               AND с.`id_студента` < с2.`id_студента`
               """)
cursor.fetchall()
print('Запрос 8')
print(answer)
connection.close()