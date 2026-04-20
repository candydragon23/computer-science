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
cursor.execute("""SELECT фамилия, имя, отчество,
               CASE WHEN средний_балл >= 4 THEN 1 ELSE 0 END as получает_стипендию
               FROM студенты
               """)
answers = cursor.fetchall()
print('Запрос 1')
print('Фамилия, Имя, Отчество, Получает_стипендию')
for answer in answers:
    фамилия, имя, отчество, получает_стипендию = answer
    print(f'{фамилия}, {имя}, {отчество}, {получает_стипендию}')
cursor.execute("""SELECT SUM(CASE WHEN н.`id_направления` = 1 THEN 1 ELSE 0 END) as прикладная_информатика,
               SUM(CASE WHEN н.`id_направления` = 2 THEN 1 ELSE 0 END) as управление_персоналом,
               SUM(CASE WHEN н.`id_направления` = 3 THEN 1 ELSE 0 END) as реклама_и_связи_с_общественностью,
               SUM(CASE WHEN н.`id_направления` = 4 THEN 1 ELSE 0 END) as сервис
               FROM `студенты` с
               JOIN `направления` н ON с.`id_направления` = н.`id_направления`
               """)
answer = cursor.fetchone()
print('Запрос 2')
прикладная_информатика, управление_персоналом, реклама_и_связи_с_общественностью, сервис = answer
print('Прикладная_информатика, Управление, Реклама, Сервис')
print(f'{прикладная_информатика}, {управление_персоналом}, {реклама_и_связи_с_общественностью}, {сервис}')
cursor.execute("""SELECT н.`название`, (SELECT AVG(с.`средний_балл`)
               FROM `студенты` с
               WHERE с.`id_направления` = н.`id_направления`) as средний_балл
               FROM `направления` н
               WHERE (SELECT AVG(с.`средний_балл`)
               FROM `студенты` с
               WHERE с.`id_направления` = н.`id_направления`) > 4
               """)
answers = cursor.fetchall()
print('Запрос 3')
print('Направление, средний_балл')
for answer in answers:
    направление, средний_балл = answer
    print(f'{направление}, {средний_балл}')
cursor.execute("""SELECT т.`название`, (SELECT AVG(с.`средний_балл`)
               FROM `студенты` с
               WHERE с.`id_уровня` = т.`id_типа`) as средний_балл
               FROM `типы_обучения` т
               WHERE (SELECT AVG(с.`средний_балл`)
               FROM `студенты` с
               WHERE с.`id_уровня` = т.`id_типа`) < 4.1""")
answers = cursor.fetchall()
print('Запрос 4')
print('Тип_обучения, средний_балл')
for answer in answers:
    уровень_обучения, средний_балл = answer
    print(f'{уровень_обучения}, {средний_балл}')
cursor.execute("""WITH worst_students as (
               SELECT фамилия, имя, средний_балл
               FROM студенты
               ORDER BY средний_балл
               LIMIT 5
               )
               SELECT *
               FROM worst_students""")
answers = cursor.fetchall()
print('Запрос 5')
print('Фамилия, имя, средний_балл')
for answer in answers:
    фамилия, имя, средний_балл = answer
    print(f'{фамилия}, {имя}, {средний_балл}')
cursor.execute("""WITH bachelor_students as(
               SELECT *
               FROM студенты
               WHERE id_уровня = 1
               ),
               top_students as (
               SELECT имя, фамилия, средний_балл
               FROM bachelor_students
               ORDER BY средний_балл DESC
               LIMIT 5
               )
               SELECT *
               FROM top_students""")
answers = cursor.fetchall()
print('Запрос 6')
print('Фамилия, имя, средний_балл')
for answer in answers:
    фамилия, имя, средний_балл = answer
    print(f'{фамилия}, {имя}, {средний_балл}')
connection.close()