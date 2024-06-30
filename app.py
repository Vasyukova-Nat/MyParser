import requests  #для отправки HTTP-запросов к API hh.ru.
import psycopg2  #PostgreSQL
import time

def getPage(page, keyword):  #page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    url = 'https://api.hh.ru/vacancies'
    params = {
        "text": keyword, # Текст фильтра. В вакансии должно быть слово, например "Аналитик"
        "area": None,  # ID города (1 - Москва, 2 - Санкт-Петербург) 
        'page': page, # Индекс страницы поиска на HH
        "per_page": 10,  # Кол-во вакансий на 1 странице
    }  

    req = requests.get(url, params=params) # Посылаем запрос к API
    data = req.json()
    req.close()
    #print('GET PAGEEEEEEEEEEEEEEEEEEEEEEE 2')
    return data


def printVacancyInfo(data, conn):
    vacancies = data.get("items", [])
    for vacancy in vacancies:
        vacancy_id = vacancy.get("id")
        vacancy_title = vacancy.get("name")
        vacancy_url = vacancy.get("alternate_url")
        company_name = vacancy.get("employer", {}).get("name")  # company = vacancy['employer']['name']
        salary = vacancy['salary']  #vacancy_salary = vacancy.get("salary")
        if salary:
            salary_range = f"{salary.get('from', 'Не указано')} - {salary.get('to', 'Не указано')}"  #можно + salary.get("currency")
        else:
            salary_range = 'Не указано'
        
        vacancy_area = vacancy.get("area")  
        if vacancy_area:
            vacancy_area = f"{vacancy_area.get('name')}"  
            
        experience = vacancy.get('experience', {}).get('name', 'Не указано')
        
        #print(f"ID: {vacancy_id}\nTitle: {vacancy_title}\nКомпания: {company_name}\nURL: {vacancy_url}\nЗарплата: {salary_range}\nГород: {vacancy_area}\nОпыт: {experience}\n")
        insert_data(conn, vacancy_id, vacancy_title, vacancy_url, company_name, salary_range, vacancy_area, experience)


def connect_to_db():
    conn = psycopg2.connect(
        dbname="ParsingDB",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    #print('CONNECT TO DBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
    return conn

def create_table(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        vacancy_id VARCHAR(255),
        vacancy_title VARCHAR(255),
        vacancy_url VARCHAR(255),
        company_name VARCHAR(255),
        salary_range VARCHAR(255),
        vacancy_area VARCHAR(255),
        experience VARCHAR(255)
    )
    """)
    conn.commit()
    cur.close()


def insert_data(conn, vacancy_id, vacancy_title, vacancy_url, company_name, salary_range, vacancy_area, experience):
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO vacancies (vacancy_id, vacancy_title, vacancy_url, company_name, salary_range, vacancy_area, experience)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (vacancy_id, vacancy_title, vacancy_url, company_name, salary_range, vacancy_area, experience))
    conn.commit()
    cur.close()
    
        
# Функция для удаления таблицы vacancies
def drop_table(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS vacancies")

    conn.commit()
    cursor.close()

##############################################################################################################################   

def get_vacancies_exp(key_experience_db):  #Фильтр БД на опыт
    conn = connect_to_db()
    cur = conn.cursor()
    if key_experience_db=='':
        cur.execute("SELECT * FROM vacancies LIMIT 10")
    else:
        cur.execute(f"SELECT * FROM vacancies WHERE experience = '{key_experience_db}'")
    rows = cur.fetchall()
    db_experience = ''
    for row in rows:
        db_experience += str(row) + '\n'
    conn.close()  #Закрытие соединения с БД
    cur.close()
    #print('GET exppppppppppppppppppppp', db_experience, 'O')
    return(db_experience)
#########################################################################################

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Предполагаем, что пользователь уже ввел значение keyword и оно сохранено в сессии
    keyword = request.args.get('keyword', '')
    if not keyword:
        return render_template('index.html')  # Перенаправляем пользователя на страницу ввода, если keyword пустое
    
    # Вызываем функцию парсера с переданным значением keyword
    #data = getPage(page=0, keyword=keyword)
    # Преобразуем результат в JSON и возвращаем его пользователю
    #return jsonify(data)

    #Мое
    conn = connect_to_db()  #Добавила строчку позже и сама, может не работать
    drop_table(conn)  #УДАЛЯЕМ ТАБЛИЦУ
    create_table(conn)  # Создаем таблицу, если ее нет

    data = getPage(page=0, keyword=keyword) # Получаем данные и сохраняем их в базу
    printVacancyInfo(data, conn)
    conn.close()  # Закрываем соединение с базой данных

    result = 'Парсинг запущен'
    return render_template('index.html', result=result)

@app.route('/results')
def results():
    key_experience_db = request.args.get('key_experience_db', '')
    # if not key_experience_db:
    #     return render_template('results.html')

    filterr = str(get_vacancies_exp(key_experience_db=key_experience_db))
    print('FILT', key_experience_db, filterr)
    return render_template('results.html', filterr=filterr)


if __name__ == '__main__':
    app.run(debug=True)




