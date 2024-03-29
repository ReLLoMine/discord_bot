# Проект Discord Bot

### Описание:
- В боте реализованы функции:
    - Автоматическое создание каналов по необходимости и удаление в случае отсутствия пользователей на канале
    - Выдача ссылки на изображение аватарки выбранного пользователя
    - Механизм конфигурации бота для каждого сервера по-отделтности
    - Управление ботом через DM и консоль
    - Планируется добавить: выдачу ролей по запросу

### Технологический стек:
- python 3.8
- discord.py

### Инструкция по настройке проекта:
1. Склонировать проект
2. Открыть проект в PyCharm с наcтройками по умолчанию
3. Создать виртуальное окружение (через settings -> project Discord Bot -> project interpreter)
4. Открыть терминал в PyCharm
5. **Убедиться, что виртуальное окружение активировано**.
6. Обновить pip:
    ```bash
    pip install --upgrade pip
    ```
7. Установить в виртуальное окружение необходимые пакеты: 
    ```bash
    pip install -r requirements.txt
    ```
8. Создать конфигурацию запуска в PyCharm (файл `main.py`)
