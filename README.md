# Проект "Контроль забруднення повітря"
Цей проект розроблено для контролю за забрудненням повітря в різних містах. Додаток дозволяє користувачам вносити дані про рівень забруднення повітря та переглядати статистику забруднення за різними параметрами.

## Зміст
- [Опис](#опис)
- [Встановлення](#встановлення)
- [Використання](#використання)

## Опис
У проекті використовується Django - фреймворк для розробки веб-додатків на мові програмування Python.

### Функціональні можливості:
- **Ввід даних**: користувачі можуть вносити дані про рівень забруднення повітря в різних містах та часові проміжки.
- **Перегляд даних**: можливість переглядати дані про забруднення повітря у вигляді таблиці.
- **Створення звітів**: користувачі можуть генерувати річні, місячні та квартальні звіти зі статистикою забруднення повітря для обраного міста та забрудника.
- **Авторизація та аутентифікація користувачів**: використання системи користувачів для авторизації та аутентифікації.
- **Новини**: відображення останніх новин щодо забруднення повітря.

## Встановлення

Клонуйте репозиторій:
```sh
$ git clone https://github.com/EkaterinaPikhovkina/pollution-control-app.git
```

Запустіть сервер Django:
```sh
$ python manage.py runserver
```

## Використання
- **Ввід даних**: натисніть на посилання "Додати дані", щоб ввести дані про забруднення повітря.
- **Перегляд даних**: перейдіть на сторінку "Перегляд даних", щоб переглянути таблицю з даними про забруднення повітря.
- **Створення**: на сторінці "Звіт" ви можете вибрати тип звіту (річний, місячний, квартальний) та ввести необхідні дані для генерації звіту.
- **Авторизація та аутентифікація**: використовуйте форму авторизації для входу в систему.
- **Новини**: на сторінці "Новини" ви можете переглянути останні новини щодо забруднення повітря.