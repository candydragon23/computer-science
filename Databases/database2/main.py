import sqlite3
import pandas as pd
from datetime import datetime
connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS Начисление")
cursor.execute("DROP TABLE IF EXISTS Лицевые_счета")
cursor.execute("DROP TABLE IF EXISTS Отдел")
cursor.execute("""CREATE TABLE IF NOT EXISTS `Лицевые_счета` (
               `Лицевой счёт` integer primary key NOT NULL UNIQUE,
               `Улица` TEXT NOT NULL,
               `Номер дома` INTEGER NOT NULL,
               `Отдел магазина` TEXT NOT NULL
               );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS `Отдел` (
               `ID отдела` integer primary key NOT NULL UNIQUE,
               `Название` TEXT NOT NULL
               );
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS `Начисление` (
               `ID операции` integer primary key NOT NULL UNIQUE,
               `Дата` TEXT NOT NULL,
               ` Лицевые счёта` INTEGER NOT NULL,
               `ID отдела` INTEGER NOT NULL,
               `Операции` TEXT NOT NULL,
               `Сумма, руб.` INTEGER NOT NULL,
               FOREIGN KEY(` Лицевые счёта`) REFERENCES `Лицевые_счета`(`Лицевой счёт`),
               FOREIGN KEY(`ID отдела`) REFERENCES `Отдел`(`ID отдела`)
               );
               """)
personal_accounts_df = pd.read_excel('data.xls', sheet_name = 'Лицевые_счета')
departments_df = pd.read_excel('data.xls', sheet_name = 'Отдел')
accruals_df = pd.read_excel('data.xls', sheet_name = 'Начисление')
accruals_df['Дата'] = pd.to_datetime(accruals_df['Дата']).dt.strftime('%Y-%m-%d')
personal_accounts_df.to_sql('Лицевые_счета', connection, index = False, if_exists = 'append')
departments_df.to_sql('Отдел', connection, index = False, if_exists = 'append')
accruals_df.to_sql('Начисление', connection, index = False, if_exists = 'append')
connection.commit()
cursor.execute("""SELECT SUM(н.`Сумма, руб.`) as Доходы 
               FROM `Начисление` н 
               JOIN `Лицевые_счета` л ON н.` Лицевые счёта` = л.`Лицевой счёт`
               JOIN `Отдел` о ON н.`ID отдела` = о.`ID отдела`
               WHERE о.`Название` = 'Производственный цех'
               AND н.`Операции` = 'Доход'
               AND л.`Отдел магазина` = 'Сантехника'
               AND л.`Улица` = 'Семеоновская'
               AND л.`Номер дома` = 27
               AND strftime('%Y', н.`Дата`) = '2021'
               """)
answer = cursor.fetchone()
print(answer[0])
connection.close()
