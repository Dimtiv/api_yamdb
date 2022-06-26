# Проект YaMDb
# Описание проекта
Проект собирает отзывы пользователей на произведения. Каждое произведение относится к определенной категории и ему может быть присвоен жанр. Пользователи могут оставлять отзыв и оценку произведению, комментировать отзывы других пользователей.

#### Доступ к проекту осуществляется на уровне ролей:
* Аноним
* Аутентифицированный пользователь
* Модератор
* Администратор

#### В проекте два приложения:
1. Riviews (бэкенд проекта)
2. API (API проекта)

### В проекте доступны Эндпойнты
| адрес                                         | медот                   | описание                                                                                                                 |
|-----------------------------------------------|-------------------------|--------------------------------------------------------------------------------------------------------------------------|
| api/v1/auth/signup/                            | POST                    | регистрация нового пользователя                                                                                 |
| api/v1/auth/signup/                          | POST                    | получение JWT-токена                                                                                                      |
| api/v1/categories/                          | GET, POST, DEL                    | получение списка всех категорий, добавление, удаление категории                                                                                                        |
| api/v1/genres/                                | GET, POST, DEL             | получение списка всех жанров, добавление, удаление жанров                                                                      |
| api/v1/titles/                                | GET, POST                    | получение списка всех произведений,    добавление нового произведения                                                                                           |
| api/v1/titles/{title_id}/                    | GET, PATCH, DEL | получение информации о произведении по id, частичное обновление, удаление                                                                            |
| api/v1/titles/{title_id}/reviews/              | GET, POST    | получение списка всех отзывов,    добавление нового отзыва                                                                                              |
| api/v1/titles/{title_id}/reviews/{review_id}/   | GET, PATCH, DEL | получение информации о отзыве на произведение по id, частичное обновление, удаление                                                                                      |
| api/v1/titles/{title_id}/reviews/{review_id}/comments/ | GET, POST               | получение списка всех комментариев к отзыву, добавление нового комментария |
| api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ | GET, PATCH, DEL | получение информации о комментарии на отзыв по id, частичное обновление, удаление                                                |
| api/v1/users/                                | GET, POST                     | получение списка всех пользователей, добавление нового пользователя                                                                     |
| api/v1/users/{username}/                               | GET, PATCH, DEL                    | получение информации о пользователе, частичное обновление, удаление                                                                          |
| api/v1/users/me/                               | GET, PATCH                    | получение данных своей учетной записи, изменение своей учетной записи                                                                          |

# Установка и запуск проекта
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Dimtiv/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

>для Linux
> 
>```
>python3 -m venv env
>```
>```
>source env/bin/activate
>```
>```
>python3 -m pip install --upgrade pip

>для Windows
> 
>```
>python -m venv venv
>```
>```
>source venv/Scripts/activate 
>```
>```
>python -m pip install --upgrade pip

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

>для Linux
>```
>python3 manage.py migrate

>для Windows
>```
>python manage.py migrate

Запустить проект:

>для Linux
>```
>python3 manage.py runserver

>для Windows
>```
>python manage.py runserver

# Примеры запросов и ответов
### Регистрация пользователя. 
>Адрес 
> >api/v1/auth/signup/ 
> 
>метод 
> >POST
> 
>запрос
> >{
"email": "string",
"username": "string"
}
> >
> ответ
> > {
"email": "string",
"username": "string"
}

### Получение JWT-токена. 
>Адрес 
> >/api/v1/auth/token/
> 
>метод 
> >POST
> 
>запрос
> >{
"username": "string",
"confirmation_code": "string"
}
> >
> ответ
> > {
"token": "string"
}

### Создание категории. 
>Адрес 
> >/api/v1/categories/
> 
>метод 
> >POST
> 
>запрос
> >{
"name": "string",
"slug": "string"
}
> >
> ответ
> > {
"name": "string",
"slug": "string"
}

### Получение списка жанров. 
>Адрес 
> >/api/v1/genres/
> 
>метод 
> >GET
> 
> ответ
> > {
"count": 0,
"next": "string",
"previous": "string",
"results": [
{
"name": "string",
"slug": "string"
}
]
}

### Добавление произведения. 
>Адрес 
> >/api/v1/titles/
> 
>метод 
> >POST
> 
>запрос
> >{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}
> >
> ответ
> > {
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
{}
],
"category": {
"name": "string",
"slug": "string"
}
}

### Частичное обновление отзыва. 
>Адрес 
> >/api/v1/titles/{title_id}/reviews/{review_id}/
> 
>метод 
> >PATCH
> 
>запрос
> >{
"text": "string",
"score": 1
}
> >
> ответ
> > {
"id": 0,
"text": "string",
"author": "string",
"score": 1,
"pub_date": "2019-08-24T14:15:22Z"
}

