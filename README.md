# Qatalogue
## Содержание
1. Введение
2. Развертывание
3. Возможности
## Введение
Проект представляет из себя простой сетевой каталог, в котором диллеры могут оставлять объявления о продаже и условиях продажи товара.
В данном случае проект - площадка для диллерства автомобилями, мотоциклами и электротранспортом.
## Развертывание и настройка
### 1. Создать и запустить виртуальное окружение
> python -m venv [название]
[название]\Scripts\activate

### 2. Установить требуемые библиотеки
> python -m pip install --upgrade pip

>pip install -r requirements.txt

### 3.  Подключить базу данных
Необходимо изменить параметры в settings.py 'DATABASES'. Я использовал PostgreSQL, поэтому при использовании другой субд следует так же
изменить движок 'ENGINE'.

### 4. Создать и выполнить миграции
Далее следует перейти в директорию с проектом:
> cd "qatalogue"

>python manage.py makemigrations

>python manage.py migrate

### 5. Заполнить базу данных объектами для примера
> python manage.py loaddata db.json

### 6. Запустить сервер
> python manage.py runserver

## Возможности
### Общие рекомендации
Для отслеживания данных о работе сервера установлена панель для дебага (django-debug-toolbar 2.0), она отображается у левой границы
окна.

В директории проекта содержатся данные для примера 'db.json'. Для загрузки объектов в базу данных:

> python manage.py loaddata db.json

Данные о курсах обмена в правом верхнем углу получаются через API KursExchange Беларусбанка, поэтому при отсутствии соединения они
будут отсутствовать.

Для использования функционала, доступного авторизованным пользователям и диллерам (django auth), можно воспользоваться следующими
данными:

Простые пользователи: SimpleMan, Rater, MisterBones, BabyYoda.

Диллеры: Getcars, Dispersion, Gooddealer, DJPJDcompany.

Пароль для всех пользователей - pas12345.

При регистрации в качестве диллера или создания диллера из обычного пользователя необходимо, для нового диллера в админ-панели
поставить флажок в свойстве 'valid'.

### Каталог продукции

![](https://github.com/Ktwru/Qatalogue/blob/master/screenshots/Products.PNG "Cars, type - coupe, drive unit: rear and foward")

На страницах cars, motorcycles и scooters выводится характеристика имеющейся в базе данных продукции, а также информация о количестве
объявлений о ее продаже и минимальная цена.

Слева отображена форма для фильтрации продукции (DRF django-filter).

### Объявления

![](https://github.com/Ktwru/Qatalogue/blob/master/screenshots/Product.PNG)

Отображается информация о продукте, а также все объявления о его продаже.

### Диллеры
На странице /dealers/ содежиться информация о подтвержденных диллерах, количество их объявлений и их рейтинг.

Все объявления диллеров во всех категориях отображаются по адресу /ads/dealers/[диллер]

Только простые пользователи могут оценивать и оставлять отзывы о диллерах, одновременно от одного пользователя 
на одного диллера может быть только одна оценка - /dealers/rate[id]:

![](https://github.com/Ktwru/Qatalogue/blob/master/screenshots/Rate.PNG)

### Поиск

![](https://github.com/Ktwru/Qatalogue/blob/master/screenshots/Search.PNG)

Поиск проводится по продукции во всех категориях.

### Добавление объявлений

![](https://github.com/Ktwru/Qatalogue/blob/master/screenshots/Adding.PNG)

К форме для добавления объявления можно перейти со страницы с выбранным продуктом или из категории с техникой, а затем уже выбрать продукт или создать новый. Добавлять как объявления, так и продукцию в каталог, могут только валидированные диллеры.
