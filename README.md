# Organization Structure API

API для управления организационной структурой компании. Позволяет создавать подразделения, сотрудников, строить дерево подразделений с ограничением глубины, перемещать подразделения с проверкой циклов, удалять с каскадированием или переназначением сотрудников.

## Стек технологий

- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0** — ORM (асинхронный)
- **PostgreSQL** — база данных
- **Alembic** — миграции
- **Docker** — контейнеризация
- **Pytest** — тестирование
- **Loguru** — логирование

## Архитектура проекта

hitalent_org/
├── app/
│ ├── api/
│ │ └── endpoints.py
│ ├── core/
│ │ ├── config.py
│ │ ├── database.py
│ │ └── exceptions.py
│ ├── models/
│ │ ├── department.py
│ │ └── employee.py
│ ├── schemas/
│ │ ├── department.py
│ │ └── employee.py
│ ├── services/
│ │ ├── department_service.py
│ │ └── employee_service.py
│ └── main.py #
├── tests/
│ ├── conftest.py #
│ └── test_departments.py 
├── migrations/
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md


## Ключевые архитектурные решения

- **Асинхронный SQLAlchemy 2.0** — неблокирующие запросы к PostgreSQL
- **Сервисный слой** — бизнес-логика отделена от API и моделей
- **Рекурсивное построение дерева** — до глубины 5 уровней
- **Проверка циклов** — при перемещении подразделений
- **Два режима удаления** — cascade (каскад) и reassign (переназначение)
- **Валидация на уровне Pydantic-схем** — тримминг пробелов, ограничения длины
- **Миграции через Alembic** — версионирование схемы БД
- **Docker Compose** — подъём PostgreSQL + приложения одной командой

## Быстрый старт

### Требования

- Docker Desktop
- Python 3.11+ (для локальной разработки)

### Запуск через Docker

```bash
# Клонировать репозиторий
git clone https://github.com/Inferno-kN/hitalent_org.git
cd hitalent_org

# Запустить контейнеры
docker-compose up --build