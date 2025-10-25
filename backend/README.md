# PixErase Backend

Бекенд часть сервиса OSINT по обработке данных. 

## Принцип реализации

В проекте используется архитектурный подход `Clean Architecture`, `EDA`. 

## Зависимости

В проекте используются следующие зависимости, которые представлены в [`pyproject.toml`]

## Деплой

> [!IMPORTANT]
> Убедитесь, что на вашем ПК или сервере установлен `Docker` и `Docker compose`.

### Локальная разработка

> [!IMPORTANT]
> Для запуска и взаимодействия используется [`just`](https://github.com/casey/just). 
> В дальнейшем в мануале будут использоваться команды с помощью `just`.  

#### Инициализация переменных окружения

Для начала создайте `.env` файл, скопировав значения из `.env.dist`.

> [!IMPORTANT]
> При запуске приложения без `Docker` следует все хосты поменять на `localhost`.

#### Инициализация `Python` проекта

Создайте `.venv`, выбрав `Python 3.12`. 
После этого вам нужно будет установить `uv` в данное виртуальное окружение, использовав команду: 

```bash
pip install uv
```

Теперь установим библиотеки и фреймворки, которые используются в проекте с помощью команды: 

```bash
uv install
```

#### Запуск инфраструктурных зависимостей

Для запуска `RabbitMQ`, `PostgreSQL`, `MinIO`, `Redis` используется команда: 

```bash
just up-dev
```

> [!IMPORTANT]
> Ожидается, что `.env` был удачно создан заранее. 

#### Запуск `scheduler`

Для запуска `worker` используем команду, которая представлена ниже: 

```bash
taskiq worker --ack-type when_saved pix_erase.worker:create_worker_taskiq_app -fsd -tp pix_erase.infrastructure.scheduler.tasks
```

Теперь запускаем сам `scheduler` в отдельном процессе: 

```bash
taskiq scheduler pix_erase.scheduler:create_scheduler_taskiq_app -fsd -tp pix_erase.infrastructure.scheduler.tasks
```

> [!IMPORTANT]
> Ожидается, что `.env` был удачно создан заранее. 
> Ожидается, что инфраструктурные зависимости уже были запущены. 

#### Запуск миграций

```bash
alembic upgrade head
```

#### Запуск `api`

Для запуска `api` используем команду, которая представлена ниже: 

```bash
uvicorn --factory src.pix_erase.web:create_fastapi_app --port 8080
```

> [!IMPORTANT]
> Ожидается, что `.env` был удачно создан заранее. 
> Ожидается, что инфраструктурные зависимости уже были запущены. 
> Ожидается, что `worker` был запущен заранее.

> [!NOTE]
> `Swagger` будет доступен на http://localhost:8080

Учетная запись супер админа: 

> email: `admin@pixerase.com`
> password: `admin12345`

