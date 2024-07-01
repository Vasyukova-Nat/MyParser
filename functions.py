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
        
        insert_data(conn, vacancy_id, vacancy_title, company_name, vacancy_url, salary_range, vacancy_area, experience)


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
        experience VARCHAR(255)
    )
    """)
    conn.commit()
    cur.close()


def insert_data(conn, vacancy_id, vacancy_title, company_name, vacancy_url, salary_range, vacancy_area, experience):
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO vacancies (vacancy_id, vacancy_title, company_name, vacancy_url, salary_range, vacancy_area, experience)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (vacancy_id, vacancy_title, company_name, vacancy_url, salary_range, vacancy_area, experience))
    conn.commit()
    cur.close()
    

def drop_table(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS vacancies")
    conn.commit()
    cursor.close()

##############################################################################################################################   
def get_vacancies_exp(key_area_db, key_experience_db):  #Фильтр БД на опыт
    conn = connect_to_db()
    cur = conn.cursor()
    if key_area_db=='' and key_experience_db=='':
        cur.execute("SELECT * FROM vacancies") # FROM vacancies LIMIT 200
    elif key_area_db:
        if key_experience_db:
            cur.execute(f"SELECT * FROM vacancies WHERE vacancy_area = '{key_area_db}' AND experience = '{key_experience_db}'")
        else:
            cur.execute(f"SELECT * FROM vacancies WHERE vacancy_area = '{key_area_db}'")
    elif key_experience_db:
        cur.execute(f"SELECT * FROM vacancies WHERE experience = '{key_experience_db}'")

    rows = cur.fetchall()
    db_experience = []
    for row in rows:
        db_experience += [row] 
    conn.close() 
    cur.close()
    return(db_experience)
#########################################################################################
