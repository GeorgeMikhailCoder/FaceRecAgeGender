# FaceRecAgeGender
 Web server to accept different people to base  

# Описание:
## Задача
Микросервис предназначен для выборочного добавления в базу людей и оценки их пола и возраста при отсутствии такой информации. Задачей микросервиса является не допустить добавление людей, фото которых уже есть в базе. Для этого в базе дополнительно хранится закодированная информация о лицах. 

## База данных
Поля базы данных (в синтаксисе SQL):  
id - автозаполняемый идентификатор, (целое число, первичный ключ)  
fio - имя/ФИО человека (строка)  
age - возраст человека (целое число)  
gender - пол человека (один символ, М/F)  
imgPath - полный путь до места хранения картинки от корневой папки системы (строка)  
binImg - уникальный код лица на картинке (бинарные данные)  

Добавленные картинки хранятся в папке media/facesImages/facesImages, полный путь и название файла содержится в imgPath

## Интерфейс
Главная страница микросервиса выводит информацию об объектах из БД, даёт возможности добавить или удалить информацию об отдельном человеке. (8000 - порт по умолчанию)  
http://ip_adress:8000/

Микросервис поддерживает два способа добавления нового человека:
- через сайт http://ip_adress:8000/add_person
- через post-запрос http://ip_adress:8000/hook/

## Принцип работы
При попытке добавления, картинка добавляемого человека сохраняется во временном хранилище, кодируется, сравнивается с уже имющимися в базе данных и в случае отсутсвия такого же человека добавляется в базу.
При отсутствии информации о поле и возрасте человека будет произведена оценка. При высокой вероятности определения оценка заносится в базу.
(Значения неизвестных полей будет: fio - "unknown", age - 0, gender - '?')

Функция добавления возвращает также id человека в базе. Данные можно посмотреть в консоли сервера, отправить post запросом на указанный адрес или увидеть в самой БД на главной странице

## Установка  
Для работы требуются модули python:  
- django
- MySQLdb (для установки MySQL-python или mysqlclient(новее))
- face_recognition
- shutil
- pickle
- age-and-gender
- libpng
- libjpeg
- x11
- libpthread

Модуль можно установить консольной командой pip install имя_модуля

Модули face_recognition (связанный с ним dlib), MySQLdb плохо устанавляваются под Windows, рекомендуется использовать linux-подобные системы или воспользоваться виртуальными машинами/wsl

После установки сервер можно запустить из директории FaceRecProject/FaceRecProfect командой:
python manage.py runserver

## Настройка
Для запуска необходимо настроить переменные окружения:
- DB_NAME - название БД
- DB_USER - имя пользователя БД
- DB_PASSWORD - пароль пользователя БД
- DB_HOST - ip удалённой БД (или localhost)
- DB_PORT - port удалённой БД
- PATH_IMAGES - путь для сохранения картинок для БД
- KOEF_FACE_COMPARATION - коэффициент распознавания, насколько большую разницу между лицами можно считать одним лицом  
0.99 - разные люди воспринимаются как один  
0.01 - один человек воспринимается как разные  
по умолчанию 0.6  
 - PREDICT_ACCURACY - показывает вероятность, выше которой предсказание пола/возраста считается достоверным (вносится в базу) в процентах  
по умолчанию 50  

После запуска по умолчанию работает на порте 8000, можно настроить. Также следует добавить выделенный для работы сервера ip в переменную ALLOWED_HOSTS в файле settings.py. 
