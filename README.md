# Проект: Благотворительный фонд поддержки котиков QRKot

QRKot — это благотворительная платформа, которая помогает собирать средства на поддержку различных инициатив, связанных с заботой о кошках. Фонд организует целевые проекты, каждый из которых имеет свою цель и требуемую сумму сбора. Пользователи могут делать пожертвования, которые распределяются между проектами по принципу FIFO.

## Стек технологий

- **Backend**: Python, FastAPI
- **База данных**: SQLite
- **Аутентификация и авторизация**: JWT

## Основные функции приложения

### Проекты

- В Фонде QRKot может быть открыто несколько целевых проектов одновременно.
- Каждый проект имеет уникальное название, описание и целевую сумму, которую необходимо собрать.
- Когда необходимая сумма набрана, проект закрывается.

### Пожертвования

- Пользователь может сделать пожертвование и оставить комментарий к нему.
- Все пожертвования нецелевые: они отправляются в общий фонд, а затем распределяются среди активных проектов.
- Пожертвования направляются в самый старый активный проект до тех пор, пока он не соберет всю необходимую сумму. Затем пожертвования перенаправляются на следующий проект.
- Если текущие открытые проекты полностью профинансированы, остаток средств ожидает открытия новых проектов.

### Пользователи

- Целевые проекты создаются администраторами платформы.
- Любой посетитель сайта может просмотреть информацию обо всех проектах, включая их статус (открытые/закрытые), необходимые и собранные суммы.
- Зарегистрированные пользователи могут делать пожертвования и отслеживать свои предыдущие взносы.

## Установка и запуск

Для запуска сервиса на вашем локальном компьютере выполните следующие шаги:

1. Скопируйте репозиторий:
```git clone https://github.com/arteick/cat_charity_fund.git```
2. Создайте виртуальное окружение и обновите систему управления пакетами pip
```py -m venv venv```
```py -m pip install -U pip```

3. Установите зависимости
```pip install -r requirements.txt```
4. Заполните файл .env -> пример .env.example
5. Создайте БД и таблицы с помощью миграций
```alembic upgrade head```
6. Запустите проект
```uvicorn app.main:app```

### Автор
[Артём Козлов](https://github.com/arteick/)
