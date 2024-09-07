from flask import Flask, render_template, request, jsonify
import requests
from functions import connect_to_db, drop_table, create_table, getPage, printVacancyInfo, insert_data, get_vacancies_exp
import time

app = Flask(__name__)

@app.route('/')
def index():
    keyword = request.args.get('keyword', '') #извлекаем keyword из GET-запроса. Если отсутствует, то значение по умолчанию - пустая строка.
    if not keyword:
        return render_template('index.html')  
    key_pages_number = (request.args.get('key_pages_number', ''))
    if key_pages_number == '':
        key_pages_number = 1
    key_pages_number = int(key_pages_number)

    key_area = request.args.get('key_area', '')
    if not key_area:
        key_area = None
    key_experience = request.args.get('key_experience', '')
    if not key_experience:
        key_experience = None
    key_employment = request.args.get('key_employment', '')
    if not key_employment:
        key_employment = None
        
    conn = connect_to_db()  
    drop_table(conn)  
    create_table(conn)  

    for page in range(0, key_pages_number): 
        data = getPage(page=page, keyword=keyword, key_area=key_area, key_experience=key_experience, key_employment=key_employment) # Получаем данные 
        printVacancyInfo(data, conn)  #Сохраняем их в базу
        if (data['pages'] - page) <= 1:  # Проверка на последнюю страницу, если вакансий меньше 2000
            break
        time.sleep(0.25) # Необязательная задержка, чтобы не нагружать сервисы hh.
    
    conn.close()  # Закрываем соединение с базой данных

    result = 'Парсинг завершён. Результаты отображены на второй странице.'
    return render_template('index.html', result=result)

@app.route('/results')
def results():
    key_area_db = request.args.get('key_area_db', '')
    key_experience_db = request.args.get('key_experience_db', '')
    key_employment_db = request.args.get('key_employment_db', '')
    
    filterr = get_vacancies_exp(key_area_db=key_area_db, key_experience_db=key_experience_db, key_employment_db=key_employment_db)[0]
    
    count = str(get_vacancies_exp(key_area_db=key_area_db, key_experience_db=key_experience_db, key_employment_db=key_employment_db)[1])
    if key_area_db=='' and key_experience_db=='' and key_employment_db=='':
        count = 'Всего найдено вакансий: ' + count 
    else:
        count = 'По Вашему запросу найдено вакансий: ' + count 
    return render_template('results.html', filterr=filterr, count=count)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')




