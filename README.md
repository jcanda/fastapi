<a name="readme-top"></a>
# Fastapi API REST

Proyecto en FastAPI para la creación de una API REST para dar servicio a una App y al panel de control de la misma.

## Instalación en local

1. Clona este repositorio en tu máquina local.
2. Ejecuta `docker-compose build` para construir las imágenes de Docker.
3. Ejecuta `docker-compose up -d` para iniciar los contenedores de Docker.
4. Ejecuta `alembic upgrade head` para aplicar las migraciones de la base de datos.
5. Visita `http://localhost:8000` en tu navegador para acceder a la aplicación.

### Built With
[![FastAPI][fastapi.tiangolo.com]][fastapi-url]
[![Pydantic][pydantic.com]][pydantic-url]
[![SQLAlchemy][sqlalchemy.org]][sqlalchemy-url]
[![Uvicorn][uvicorn.org]][uvicorn-url]
[![asyncmy][asyncmy.github.io]][asyncmy-url]
[![alembic][alembic.sqlalchemy.org]][alembic-url]
[![Docker][docker.com]][docker-url]
[![Docker Compose][docker-compose.com]][docker-compose-url]
[![Database][mariadb.org]][mariadb-url]
[![PyJWT][pyjwt.org]][pyjwt-url]
[![pre-commit][pre-commit.code]][pre-commit-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Make will help you
To build , run and test and more ... use magic of make help to play with this project.
```shell
make help
```

## Documentación en local dentro del entorno
`PYTHONPATH="app:$PYTHONPATH" uvicorn main:app --reload`

## Licencia

Este proyecto está bajo una Licencia de Software Propietario. Consulta el archivo `LICENSE` para más información.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[fastapi.tiangolo.com]: https://img.shields.io/badge/FastAPI-0.114.0-009485?style=for-the-badge&logo=fastapi&logoColor=white
[fastapi-url]: https://fastapi.tiangolo.com/
[pydantic.com]: https://img.shields.io/badge/Pydantic-2.9.0-e92063?style=for-the-badge&logo=pydantic&logoColor=white
[pydantic-url]: https://docs.pydantic.dev/latest/
[sqlalchemy.org]: https://img.shields.io/badge/SQLAlchemy-2.0.34-bb0000?color=bb0000&style=for-the-badge
[sqlalchemy-url]: https://docs.sqlalchemy.org/en/20/
[uvicorn.org]: https://img.shields.io/badge/Uvicorn-0.23.2-2094f3?style=for-the-badge&logo=uvicorn&logoColor=white
[uvicorn-url]: https://www.uvicorn.org/
[asyncmy.github.io]: https://img.shields.io/badge/asyncmy-0.2.9-2e6fce?style=for-the-badge&logo=mariadb&logoColor=white
[asyncmy-url]: https://github.com/long2ice/asyncmy
[pytest.org]: https://img.shields.io/badge/pytest-6.2.5-fff?style=for-the-badge&logo=pytest&logoColor=white
[pytest-url]: https://docs.pytest.org/en/6.2.x/
[alembic.sqlalchemy.org]: https://img.shields.io/badge/alembic-1.13.2-6BA81E?style=for-the-badge&logo=alembic&logoColor=white
[alembic-url]: https://alembic.sqlalchemy.org/en/latest/
[docker.com]: https://img.shields.io/badge/Docker-2.29.2-2496ed?style=for-the-badge&logo=docker&logoColor=white
[docker-url]: https://www.docker.com/
[docker-compose.com]: https://img.shields.io/badge/Docker_Compose-1.29.2-2496ed?style=for-the-badge&logo=docker&logoColor=white
[docker-compose-url]: https://docs.docker.com/compose/
[mariadb.org]: https://img.shields.io/badge/MariaDB-11.5-336791?style=for-the-badge&logo=mariadb&logoColor=white
[mariadb-url]: https://mariadb.org/
[pyjwt.org]: https://img.shields.io/badge/PyJWT-2.9.0-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white
[pyjwt-url]: https://pyjwt.readthedocs.io/en/stable/
[pre-commit.code]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge&logo=pre-commit&logoColor=white
[pre-commit-url]: https://github.com/pre-commit/pre-commit/actions/workflows/main.yml
