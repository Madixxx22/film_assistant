# Film Assistant
**Film Assistant** - это Rest Api приложение позволяющая пользователям искать фильмы, добавлять в избранное и смотреть рекомендации.

### Возможности:
* регистрация пользователей, авторизация
* просмотр профиля и его изменения,
* сброс пароля
* Удаление всей информации об пользователе
* Поиск фильмов
* Добавление в избранное и удаление
* Рекомендации по избранному
* Просмотр истории по запросам и фильмов к ним
* Очистка истории запросов


## Оглавление
1. Сборка проекта и локальный запуск
    * Клонируем репозиторий
    * Настройка
    * Запуск
    * Открытие OpenApi(swager)
2. Запуск тестов
3. Используемый стэк


___

## Сборка проекта и локальный запуск:
### Клонируем репозиторий
Выполните в консоли

`https://github.com/Madixxx22/film_assistant`

### Настройка
Создайте .env файл в том же каталоге что и docker-compose.yaml, и добавьте следующие параметры
```
DB_USER
DB_HOST
DB_PASSWORD
DB_NAME

POSTGRES_USER
POSTGRES_DB
POSTGRES_PASSWORD

PGADMIN_DEFAULT_EMAIL
PGADMIN_DEFAULT_PASSWORD
PGADMIN_CONFIG_SERVER_MODE=

SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_WEEKS

API_KEY_IMDB
```
SECRET_KEY можно сгенерировать командай `$ openssl rand -hex 32`
API_KEY_IMDB можно получить зарегестрировавашись https://imdb-api.com/api

### Запуск
Установите docker desktop с оффициального сайта и запустите(если на windows или macos)
https://eternalhost.net/base/vps-vds/ustanovka-docker-linux (Воспользуйтесь инструкцией для Linux)

В консоле находясь в каталоге с файлом docker-compose.yaml запускаем команду
`docker-compose up` 
Если все было установлено и настроено корректно приложения запустится, кроме back end(http://127.0.0.1:8008) развернется postgresql и pgadmin(http://127.0.0.1:5050)

### Открытие OpenApi(swager)
Перейдя по ссылке http://127.0.0.1:8008/docs мы откроем автоматически сгенерированную документацию openapi swager

## Запуск тестов
Тесты можно запустить и проверить работоспособность программы при запущенных docker контейнерах
`docker-compose exec app python -m pytest app/tests`
После запустятся последовательно 18 тестов.
Обязательно запускать на пустой БД или несколько тестов будут провалены

## Используемый стэк
* **Python \ pytest**
* **FastAPI \ sqlalchemy \ pydantic \ databases \ aiohttp**
* **Postgresql \ pgadmin**
* **docker \ docker-compose**
