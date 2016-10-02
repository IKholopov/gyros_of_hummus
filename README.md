# gyros_of_hummus
Деплоймент осуществляется через [docker](https://www.docker.com/). Нафига? Чтобы упростить процесс доставки на сервер и унифицировать среду тестирования. Суть в том, что при работе через контейнер происходит запуск в конкретизированной среде - с явной версией библиотек и пр. 

Установка docker'а происходит следующим образом. 

  Для Max: https://docs.docker.com/docker-for-mac/ 
  
  Для Linux: 
  
    docker-engine: https://docs.docker.com/engine/installation/linux/
    
    docker-compose: pip install docker-compose
    
Подгатовка к работе.
  1. Клонируем репозиторий.
  2. В корневой папке репозиотрия запускаем docker-compose build 
  3. Пьём кофе
  4. Как закончит - docker-compose up -d
  
##Основной workflow:
  При запуске 
  
    docker-compose up -d
  
  будет запущен nginx на 80 порте. Все изменения в код будут подтягиваться автоматически.
  Если надо выполнить что-то с помощью manage.py (если оставим django), то делаем это зайдя в сессию с помощью 
      docker-compose run web /bin/bash
