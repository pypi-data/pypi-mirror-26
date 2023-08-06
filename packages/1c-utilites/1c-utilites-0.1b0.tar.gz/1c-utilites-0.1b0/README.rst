1C Utils
=========

**1C Utils** это набор скриптов для управления и обслуживания серверов 1С.

Репозиторий:
https://gitlab.com/onegreyonewhite/1c-utilites

Для вопросов и предложений используйте трекер задач:
https://gitlab.com/onegreyonewhite/1c-utilites/issues

Возможности
--------

На данный момент поддерживается только архивация PostgreSQL и файловых БД 1С.


Quickstart
----------

Поддерживается любая Linux-система с наличием в ней Python 2.7/3.4/3.5
и необходимых утилит обслуживания:
* pg_dump для архивации PostgreSQL баз
* tar для упаковывания файловых баз

Установка:
    .. sourcecode:: bash

      pip install 1c-utilites
      1c-utilites --help
