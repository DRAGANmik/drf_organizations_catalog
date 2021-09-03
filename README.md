# drf_organizations_catalog

## Справочник-телефонная книга организаций.

Справочник представляет собой API приложение(DFR) для поиска номеров телефонов и информации об организациях.

## Запуск проекта в Docker окружении 

- Запустить проект: 
    ```shell
    docker-compose up --build
     ```
- Запустить проект в автономном режиме: 
    ```shell
    docker-compose up -d --build
     ```
- Применить миграции:
   ```shell
   docker-compose exec web python manage.py migrate --noinput
   ```
- Создать суперпользователя:
  ```shell
  docker-compose exec web python manage.py createsuperuser
    ```
- Остановить проект сохранив данные в БД:
    ```shell
    docker-compose down
    ```
- Остановить проект удалив данные в БД:
    ```shell
    docker-compose down --volumes
    ```
  
## Запуск проекта локально
- Установить зависимости:
    ```shell
    pip install -r requirements.txt
    ```
- Применить миграции:
  ```shell
  python manage.py migrate --settings=testing.local
  ```
- Создать суперпользователя:
  ```shell
  python manage.py createsuperuser --settings=testing.local
  ```
- Запустить проект: 
    ```shell
    python manage.py runserver --settings=testing.local

     ```
  
## Документация: 
## - http://127.0.0.1:8000/swagger/
## - http://127.0.0.1:8000/redoc/