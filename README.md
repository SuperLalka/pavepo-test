<!-- PROJECT LOGO -->
<div align="center">
  <h2>pavepo-test</h2>

  <h3 align="center">README тестового задания</h3>

  <p align="center">
    Веб-приложение на FastAPI, небольшой сервис загрузки аудио-файлов от пользователей
  </p>
</div>

<a name="readme-top"></a>

<hr>

<!-- ABOUT THE PROJECT -->
## About The Project

Требования:
* Реализовать сервис по загрузке аудио-файлов от пользователей, используя FastAPI, SQLAlchemy и Docker.
* Пользователи могут давать файлам имя в самом API.
* Авторизацию пользователей реализовать через Яндекс.
* Файлы хранить локально, хранилище использовать не нужно.
* Использовать асинхронный код.

Ожидаемый результат:
1. Готовое API с возможностью авторизации через Яндекс с последующей аутентификацией к запросам через внутренние токены API.
Доступные эндпоинты:
- авторизация через яндекс
- обновление внутреннего access_token
- получение, изменение данных пользователя
- удаление пользователя от имени суперпользователя
- получение информации об аудиофайлах пользователя: название файлов и путь в локальное хранилище
2. Документация по развертыванию сервиса и БД в Docker.


### Built With

* [![FastApi][FastApi-badge]][FastApi-url]
* [![Postgres][Postgres-badge]][Postgres-url]
* [![Docker][Docker-badge]][Docker-url]


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Copy project to repository on local machine (HTTPS or SSH)
  ```sh
  git clone https://github.com/SuperLalka/pavepo-test.git
  ```
  ```sh
  git clone git@github.com:SuperLalka/pavepo-test.git
  ```

### Installation

To start the project, it is enough to build and run docker containers.
Database migration and fixture loading will be applied automatically.

1. Build & run docker containers
   ```sh
   docker-compose -f docker-compose.yml up -d --build
   ```


### Documentation

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[FastApi-badge]: https://img.shields.io/badge/fastapi-%23009688.svg?style=for-the-badge&logo=fastapi&logoColor=white
[FastApi-url]: https://fastapi.tiangolo.com/
[Postgres-badge]: https://img.shields.io/badge/postgresql-%234169E1.svg?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/
[Docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
