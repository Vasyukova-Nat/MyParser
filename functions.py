import requests  #для отправки HTTP-запросов к API hh.ru.
import psycopg2  #PostgreSQL
import time

def getPage(page, keyword, key_area, key_experience, key_employment):  #page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    url = 'https://api.hh.ru/vacancies'
    params = {
        "text": keyword, # Текст фильтра. В вакансии должно быть слово, например "Аналитик"
        "area": key_area,  # ID города (1 - Москва, 2 - Санкт-Петербург) 
        "experience": key_experience, 
        "employment": key_employment,
        'page': page, # Индекс страницы поиска на HH
        "per_page": 10,  # Кол-во вакансий на 1 странице
    }  
    req = requests.get(url, params=params) # Посылаем запрос к API
    data = req.json()
    req.close()
    return data


def printVacancyInfo(data, conn):
    vacancies = data.get("items", [])
    for vacancy in vacancies:
        vacancy_id = vacancy.get("id")
        vacancy_title = vacancy.get("name")
        vacancy_url = vacancy.get("alternate_url")
        company_name = vacancy.get("employer", {}).get("name") 
        salary = vacancy['salary']  
        if salary:
            salary_range = f"{salary.get('from', 'Не указано')} - {salary.get('to', 'Не указано')}"  #можно + salary.get("currency")
        else:
            salary_range = 'Не указано'
        
        vacancy_area = vacancy.get("area")  
        if vacancy_area:
            vacancy_area = f"{vacancy_area.get('name')}"  
            
        experience = vacancy.get('experience', {}).get('name', 'Не указано')
        employment = vacancy.get('employment', {}).get('name', 'Не указано')
        
        insert_data(conn, vacancy_id, vacancy_title, company_name, vacancy_url, salary_range, vacancy_area, experience, employment)


def connect_to_db():
    # conn = psycopg2.connect(
    #     dbname="ParsingDB",
    #     user="postgres",
    #     password="postgres",
    #     host="localhost",
    #     port="5432"
    # )
    conn = psycopg2.connect(
        host="db", 
        database="ParsingDB", 
        user="postgres", 
        password="postgres"
    )
    return conn

def create_table(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        vacancy_id VARCHAR(255),
        vacancy_title VARCHAR(255),
        company_name VARCHAR(255),
        vacancy_url VARCHAR(255),
        salary_range VARCHAR(255),
        vacancy_area VARCHAR(255),
        experience VARCHAR(255),
        employment VARCHAR(255)
    )
    """)
    conn.commit()
    cur.close()


def insert_data(conn, vacancy_id, vacancy_title, company_name, vacancy_url, salary_range, vacancy_area, experience, employment):
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO vacancies (vacancy_id, vacancy_title, company_name, vacancy_url, salary_range, vacancy_area, experience, employment)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (vacancy_id, vacancy_title, company_name, vacancy_url, salary_range, vacancy_area, experience, employment))
    conn.commit()
    cur.close()
    

def drop_table(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS vacancies")
    conn.commit()
    cursor.close()

##############################################################################################################################   
def get_vacancies_exp(key_area_db, key_experience_db, key_employment_db):  #Фильтр БД на опыт
    conn = connect_to_db()
    cur = conn.cursor()
    query = f"SELECT * FROM vacancies WHERE 1=1" # FROM vacancies LIMIT 200
    if key_area_db:
        query += f" AND vacancy_area = '{key_area_db}'"
    if key_experience_db:
        query += f" AND experience = '{key_experience_db}'"
    if key_employment_db:
        query += f" AND employment = '{key_employment_db}'"

    cur.execute(query)
    rows = cur.fetchall()
    db_experience = []
    count = 0  #кол-во найденных результатов
    for row in rows:
        db_experience += [row] 
        count += 1
    conn.close() 
    cur.close()
    return(db_experience, count)
#########################################################################################
#drop_table(connect_to_db()) - искусственное обнуление таблицы