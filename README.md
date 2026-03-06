# Coursework_03

## Описание
Проект сбора данных о компаниях и вакансиях с сайта hh.ru с загрузкой в БД.

## Установка

  poetry install

## Настройки


1. Создайте `database.ini` конфигурационный файл с вашими параметрами подключения к БД.
</br>
Пример содержания файла:
```ini
[postgresql]
host=localhost
user=postgres
password=12345
port=5432
```