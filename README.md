# MyParser
Платформа парсинга данных о соискателях и вакансиях с платформы hh.ru.

## Описание
Веб-приложение для парсинга вакансий с HeadHunter.ru с сохранением результатов в базу данных и возможностью фильтрации. Взаимодействует с API HH.RU (https://api.hh.ru/) с помощью токена. Для удобства пользования реализован веб-интерфейс с помощью фреймворка Flask. Вся система упакована в Docker-контейнеры.

![screenshot of sample](https://sun9-25.userapi.com/impg/qQe1fngHRzsvk0hbWkK9WYEQ4sqqx3Su9HFCoA/__hTPvUEYM0.jpg?size=1280x629&quality=95&sign=85be1b8ef65b277290b40501657be244&type=album)

## Стек
- Backend: Python, Flask, requests, psycopg2, PostgreSQL
- Frontend: HTML, CSS, Bootstrap
- Общее: Docker, Docker Compose
- API: HeadHunter API (https://api.hh.ru/)

## Функционал системы
- Формирование запроса для сбора данных по ключевому слову
- Настройка количества страниц для парсинга (до 200 страниц, 2000 вакансий)
- Автоматическое сохранение информации о вакансиях в БД PostgreSQL (ID, название, компания, ссылка, зарплата, город, опыт, занятость)
- Вывод аналитики по параметрам: количество вакансий по фильтрам
- Фильтрация сохранённых вакансий по городу, опыту работы, типу занятости
- Отображение всех вакансий из БД при пустых фильтрах
- Контейнеризация и оркестрация через Docker Compose
- Веб-интерфейс с тремя страницами (парсинг, результаты, контакты)

## Быстрый старт (режим разработки)
1) Клонирование репозитория:
```
git clone https://github.com/Vasyukova-Nat/MyParser.git -b master
```
2) Запуск через Docker Compose:
```
cd MyParser
docker-compose up --build
```
3) После запуска веб-приложение станет доступно по адресу http://127.0.0.1:5000

## Структура проекта
```
MyParser/
├── static/ # Статические файлы
│ └── css/
│ ├── main.css # Стили первой страницы (парсинг)
│ └── results.css # Стили второй страницы (результаты)
│
├── templates/ # Шаблоны HTML
│ ├── contacts.html # Страница контактов
│ ├── index.html # Главная страница (парсинг)
│ └── results.html # Страница результатов (фильтрация БД)
│
├── app.py # Главный файл приложения Flask
├── functions.py # Backend-логика (парсинг API, работа с БД)
├── docker-compose.yml # Оркестрация двух сервисов (flask_app и db)
├── Dockerfile # Сборка образа Flask-приложения
└── requirements.txt
```

## Инструкция пользователя
Сайт состоит из трёх страниц: парсинга, вывода содержимого БД и контактов.

На первой странице находятся 2 поля для взаимодействия: 
- Ключевое слово, по которому нужно искать вакансии. Допустим ввод на английском и русском языках.
- Количество страниц, которое пользователь хотел бы собрать (на одной странице 10 вакансий).

![screenshot of sample](https://sun9-53.userapi.com/impg/oJRpGFP6ZI8d3VY03sQAQCzBUDsycWjfaGED2Q/puvX8ZnjiIk.jpg?size=1280x627&quality=95&sign=f0db9cf438291585ae89b37c4b2567c2&type=album)

![screenshot of sample](https://sun9-41.userapi.com/impg/wWLXKntLl2barzF5-fXKl-jWwMbL7z8U6g9zwg/OpN8UyjLA8A.jpg?size=1280x636&quality=95&sign=c5af8dbe3cdfcc3a87a0e41f1ae2590d&type=album)

На второй странице пользователь может заполнить фильтры: Город, Опыт работы, Занятость.

![screenshot of sample](https://sun9-8.userapi.com/impg/UKreQHqr-o2x3sI5mwiZRXWm7RSDifqg4kWFsw/9_LfwkC_JPU.jpg?size=1280x631&quality=95&sign=83a863f6b049212b122190257f91547a&type=album)  

![screenshot of sample](https://sun9-46.userapi.com/impg/D0KAUO4kNdsi_0lBehlUK7XusnlXQjaquGRZVg/BUExwTv6Zv0.jpg?size=463x614&quality=95&sign=2e3392b492566b59c2652674ec54bda8&type=album)  
![screenshot of sample](https://sun1-98.userapi.com/impg/NSNQXh8AJzmByMbTl3EiyaPk5AJiTmKFBAGcOw/TISelgQOfRE.jpg?size=326x254&quality=95&sign=e0d07bf62040079c591fa59dc12d93c7&type=album)  
![screenshot of sample](https://sun9-58.userapi.com/impg/dCgpK8ki2-rPb4f79YepqcDYsw1ARFv4vZIuSQ/y9yBW9zrV0M.jpg?size=376x277&quality=95&sign=1c8ba54d8a9fd24e3917bed84dfb2221&type=album)  

![screenshot of sample](https://sun1-94.userapi.com/impg/GGwG1BgCKAUipoAZsV9LXt-hOUmiaw4xlZeMow/ew_ZLdr7YqM.jpg?size=1280x637&quality=95&sign=75d1070e04334026974154ca5dafb261&type=album)  

На странице "Контакты" указана подробная информация о разработчике.  
![screenshot of sample](https://sun9-2.userapi.com/impg/bp3CgcQSAR5M5LCV1KItjCoIeNMA5mMfliWZRg/FZ2SKjQibck.jpg?size=1280x630&quality=95&sign=28b0ae59d1a263dd91e6e79fa9469232&type=album)  


