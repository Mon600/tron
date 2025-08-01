# Настройка проекта FastAPI

Этот проект представляет собой приложение FastAPI, которое взаимодействует с базой данных и API блокчейна Tron (TRX).


## Начало работы

Выполните следующие шаги для настройки и запуска проекта локально.

### Предварительные требования

* Python 3.9+
* pip (рекомендуется для управления зависимостями)

### 1. Клонирование репозитория

```bash
git clone https://github.com/Mon600/tron
cd <каталог-вашего-проекта>
```

### 2. Настройка переменных окружения
Создайте файл .env в корневом каталоге проекта и добавьте следующие переменные окружения:

```
DB_USER=имя_пользователя_вашей_базы_данных
DB_PASSWORD=пароль_вашей_базы_данных
DB_HOST=хост_вашей_базы_данных
DB_PORT=порт_вашей_базы_данных
DB_NAME=имя_вашей_базы_данных
API_KEY=ваш_api_ключ_tron
```

Замените значения-заполнители вашими фактическими учетными данными базы данных и API-ключом Tron.

### 3. Установка зависимостей

```
pip install -r requirements.txt
```

Зависимости перечислены в requirements.txt и включают: alembic==1.16.4, fastapi==0.115.12, SQLAlchemy==2.0.39, python-dotenv==1.0.1 и uvicorn==0.34.0, среди прочих.

### 4. Миграции базы данных
   
Этот проект использует Alembic для миграций базы данных.

Сначала убедитесь, что ваша база данных запущена и доступна с учетными данными, указанными в файле .env.

Чтобы применить миграции, выполните:

```
alembic upgrade head
```

Если вам нужно создать новую миграцию, вы можете использовать:


```
alembic revision --autogenerate -m "Описание вашей миграции"
```

### 5. Запуск приложения
После установки зависимостей и применения миграций вы можете запустить приложение FastAPI:

```
python main.py
```
Приложение будет работать по умолчанию на http://127.0.0.1:8000.

### 6. Конечные точки API
API предоставляет следующие конечные точки:

`POST` `/get-info:` Получить информацию об адресе Tron.

Тело запроса: `{"address": "TRON_ADDRESS_HERE"}`

Ответ: `InfoSchema (адрес, баланс, пропускная способность, энергия)`

`GET` `/get-history`: Получить список исторических записей.

Параметр запроса (необязательно): records (целое число, по умолчанию: 10) - количество записей для получения.

Ответ: `list[HistorySchema] (id, адрес, дата)`

###7. Тестирование
Для запуска тестов используйте pytest:
```
pytest
```
