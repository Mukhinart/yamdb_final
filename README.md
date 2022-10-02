### Проект YaMDb

**YaMDb** - сервис для сбора отзывов на произведения.

[![Django-app workflow](https://github.com/Mukhinart/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/Mukhinart/yamdb_final/actions/workflows/yamdb_workflow.yml)

Проект YaMDb собирает отзывы (**Review**) пользователей на произведения (**Titles**). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (**Category**) может быть расширен администратором.
Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (**Review**) и выставляют произведению рейтинг. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

**Развернутый проект доступен по адресу - YAMDB_FINAL(http://178.154.203.148)**

### Технологии

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

### Ссылка для установки Docker:

[Docker](https://docs.docker.com/engine/install/)

### Инструкция по развертыванию приложения:

- Склонируйте проект из репозитория:

```sh
$ git clone https://github.com/Mukhinart/yamdb_final.git
```

- Выполните вход на удаленный сервер

- Установите DOCKER на сервер:
```sh
apt install docker.io 
```

- Установитe docker-compose на сервер:
```sh
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

- Отредактируйте конфигурацию сервера NGNIX:
```sh
Локально измените файл ```..infra/nginx.conf``` - замените данные в строке server_name на IP-адрес удаленного сервера
```

- Скопируйте файлы docker-compose.yml и nginx.conf из директории ```../infra/``` на удаленный сервер:
```sh
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yaml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
- Создайте переменные окружения (указаны в файле ../infra/env.example) и добавьте их в Secrets GitHub Actions

- **Запуск docker-контейнеров:**

- Запустите приложение в контейнерах:

```sh
sudo docker-compose up -d --build
```

- Выполните миграции:

```sh
sudo docker-compose exec web python manage.py migrate
```

- Создайте суперпользователя:

```sh
sudo docker-compose exec web python manage.py createsuperuser
```

- Выполните команду для сбора статики:

```sh
sudo docker-compose exec web python manage.py collectstatic --no-input
```

### Команда для остановки приложения в контейнере:

```sh
docker-compose down -v
```

***

# Ресурсы API YaMDb

**AUTH**: аутентификация.

**TITLES**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

**CATEGORIES**: категории (типы) произведений ("Фильмы", "Книги", "Музыка").

**GENRES**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.

**REVIEWS**: отзывы на произведения. Отзыв привязан к определённому произведению.

**COMMENTS**: комментарии к отзывам. Комментарий привязан к определённому отзыву.

# Пользовательские роли

**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

**Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.

**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.

**Администратор (admin)** — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

**Администратор Django** — те же права, что и у роли Администратор.

### Алгоритм регистрации пользователей

Для добавления нового пользователя нужно отправить POST-запрос на эндпоинт:

```
POST /api/v1/auth/signup/
```

- В запросе необходимо передать поля:

1. ```username``` - имя пользователя;
2. ```email``` - почта пользователя.

Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.

Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт:

```
POST /api/v1/auth/token/
```

- В запросе необходимо передать поля:

1. ```username``` - имя пользователя;
2. ```confirmation_code``` - код подтверждения.
 
В ответ на запрос пользователю придет ```token``` (JWT-токен).
В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.

После регистрации и получения токена пользователь может заполнить поля в своём профайле путем отправки запроса на эндпоинт:

```
PATCH /api/v1/users/me/
```

### Регистрация пользователей админом

Пользователя может создать администратор — через админ-зону сайта или через запрос на специальный эндпоинт:

```
POST /api/v1/users/
```

- Письмо с кодом отправлять не нужно.

После этого пользователь должен самостоятельно отправить POST-запросы как при самостоятельной регистрации.

### Примеры использования API для неавторизованных пользователей:

Для неавторизованных пользователей работа с API доступна в режиме чтения.

```sh
При указании параметров 'limit' и 'offset' выдача работает с пагинацией.
GET /api/v1/categories/ - получить список всех категорий.
GET /api/v1/genres/ - получить список всех жанров.
GET /api/v1/titles/ - получить список всех произведений.
GET /api/titles/{title_id}/reviews/ - получение списка отзывов по id произведения.
GET /api/titles/{title_id}/reviews/{review_id}/ - получение отзыва по id для указанного произведения.
GET /api/titles/{title_id}/reviews/{review_id}/comments/ - получение списка всех комментариев к отзыву
GET /api/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ - получение комментария по id для указанного отзыва.
```

#### Пример GET-запроса:
```
GET /api/v1/titles/
```

#### Пример ответа:
- код ответа сервера: 200 OK
- тело ответа:

```sh
[
  "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "name": "Безумный Макс",
            "year": 2014,
            "rating": null,
            "description": "Максим сошел с ума",
            "genre": [],
            "category": {
                "name": "Фильм",
                "slug": "cinema"
            }
        },
    ...
]
```

#### Пример POST-запроса:
```
POST /api/v1/titles/
```

```sh
{
"name": "Управление гневом",
"year": 2000,
"description": "фильм с Адамом Сендлером",
"genre": [
"comedy"
],
"category": "movie"
}
```

Подробная документация к API с доступными методами находится по адресу ```http://178.154.203.148/redoc/```

***

### Автор

Артём Мухин
