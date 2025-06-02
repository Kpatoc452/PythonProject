# Marketplace
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Асинхронность](https://img.shields.io/badge/-Асинхронность-464646?style=flat-square&logo=Асинхронность)](https://en.wikipedia.org/wiki/Asynchrony_(computer_programming))
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat-square&logo=JWT)](https://jwt.io/introduction)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Minio](https://img.shields.io/badge/-Minio-464646?style=flat-square&logo=Minio)](https://min.io/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat-square&logo=Alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat-square&logo=SQLAlchemy)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?style=flat-square&logo=uvicorn)](https://www.uvicorn.org/)
[![JavaScript](https://img.shields.io/badge/-JavaScript-464646?style=flat-square&logo=JavaScript)]()
[![HTML5](https://img.shields.io/badge/-HTML5-464646?style=flat-square&logo=HTML5)]()
[![CSS](https://img.shields.io/badge/-css-464646?style=flat-square&logo=css)]()
[![CatBoost](https://img.shields.io/badge/-CatBoost-464646?style=flat-square&logo=CatBoost)](https://catboost.ai/)
[![Poetry](https://img.shields.io/badge/-Poetry-464646?style=flat-square&logo=Poetry)](https://python-poetry.org/)


## Описание

Репозиторий IT-проекта "Marketplace" на Python

### Состав команды 

Ефименко Михаил - Backend, Frontend, DevOps

Мишин Дмитрий Михайлович - Backend

Стрекаловский Глеб Антонович - ML

### Стек технологий

- Языки программирования: Python 3.12.7, JavaScript
- Создание WEB-интерфейса: HTML5, CSS
- WEB-фреймворк: Fastapi
- Изолирование окружения: Docker
- Работа с зависимостями: Poetry
- База данных: PostgreSQL
- Работа с базой данных: SQLAlchemy, Alembic
- Объектное хранилище: Minio
- Создание ML-модели: CatBoost

### Реалезованный функционал 

- Хранение денных в PostgreSQL
- Хранение объектов в Minio
- Хранение чувствительный данных в env-файлеч
- Автоматическое создание миграций на старте приложения
- Регистрация, верификация пользователей
- Аунтефикация пользователей с помощью JWT
- Создание товаров для аунтифецированных пользователей, удаление, обновление, получение списка своих товаров, получение списка рекомендованных товаров с помощью рекомендательной системы
- Получение списка всех категорий
- Создание, обновление, удаление категорий только для суперюзера
- Покупка товара
- Логирование просмотров товаров для рекомендательной системы
- Создание суперюзера программно / на старте приложения
- ML модель для рекомендательной системы
- WEB-интерфейс
