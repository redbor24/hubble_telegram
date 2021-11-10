# Проект hubble_telegram

Скрипт отправляет в Telegram-канал картинку на космическую тематику с 
заданной периодичностью.

Имя telegram-бота [@devman-hubble](https://t.me/spacexhubble_bot)

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков 
[dvmn.org](http://dvmn.org).

### Зависимости
```
requests==2.26.0
python-telegram-bot==13.7
python-decouple==3.5
```
### Установка
Python должен быть установлен. Затем используйте pip для установки зависимостей
(или pip3, если есть конфликт с Python2):
```
pip install -r requirements.txt
```
или
```
pip3 install -r requirements.txt
```

### Переменные окружения

  - `DELIVERY_TIMEOUT=<value>` - периодичность отправки картинок в Telegram-канал в 
секундах. Если переменная не задана, то берётся значение 86400 (одни сутки)


### Файл `.env` 

  - `NASA_TOKEN=<value>` - токен для работы с [NASA API](https://api.nasa.gov/), 
полученный при [регистрации](https://api.nasa.gov/#signUp);

  - `TELEGRAM_TOKEN=<value>` - токен для работы с Telegram-API
([получение токена](https://t.me/botfather));

  - `TELEGRAM_CHANNEL_NAME=<value>` - имя Telegram-канала для отправки картинок.

  - `IMAGES_PATH` - абсолютный или относительный (от места запуска скрипта) 
путь для сохранения картинок.

### Запуск

```
python hubble_telegram.py
```

## Модули

### config.py
Содержит объявление глобальных переменных, необходимых для работы скрипта
 (см. `.env`-файл):

  - `NASA_TOKEN` - токен для работы с NASA API;

  - `TELEGRAM_TOKEN` - токен для работы с Telegram;

  - `DELIVERY_TIMEOUT` - периодичность отправки картинок в Telegram-канал;

  - `TELEGRAM_CHANNEL_NAME` - имя Telegram-канала;

  - `IMAGES_PATH` - путь для сохранения картинок.

### hubble_telegram.py

Отправляет в заданный Telegram-канал одну картинку из папки с заданной 
периодичностью.

- __Пример использования:__
```
from config import IMAGES_PATH, TELEGRAM_CHANNEL_NAME, TELEGRAM_TOKEN, \
    DELIVERY_TIMEOUT

send_images_to_telegram_channel(TELEGRAM_TOKEN, IMAGES_PATH,
                                TELEGRAM_CHANNEL_NAME, DELIVERY_TIMEOUT)
```
### space_images.py

Содержит функции для скачивания:
1. Фотографий запусков космических кораблей компании 
[SpaceX](https://www.spacex.com/);
2. Фотографий нашей планеты из космоса;
3. Астрономических картинок дня.

#### Функции

###### download_spacex_images
Скачивает все доступные фотографии запусков космических аппаратов компании 
[SpaceX](https://www.spacex.com/).

- __Параметры:__
  
    `images_path` - полный путь для сохранения картинок.


- __Вызов:__
```
from config import IMAGES_PATH


download_spacex_images(IMAGES_PATH)
```

###### download_apod_images
Обращается к [NASA API](https://api.nasa.gov/) за указанным количеством 
астрономических картинок дня
([APOD - Astronomy Picture of the Day](https://api.nasa.gov/#apod)),
скачивает их в `save_path` под именами, взятыми из их url. 
Для ссылок, указывающих на видео, сохраняется его `thumbnail` 
под именем `apodN.jpg`

- __Параметры:__
    
  - `nasa_token` - токен для работы с [NASA API](https://api.nasa.gov/), 
полученный при [регистрации](https://api.nasa.gov/#signUp);

  - `images_path` - полный путь для сохранения картинок;

  - `image_count` - количество картинок для получения.


- __Вызов:__
```
from config import NASA_TOKEN, IMAGES_PATH


download_apod_images(NASA_TOKEN, IMAGES_PATH)
```

###### download_epic_images
Обращается к [NASA API](https://api.nasa.gov/EPIC/api/natural?api_key=DEMO_KEY) 
за фотографиями нашей планеты из космоса. Ответ на один запрос содержит 
несколько ссылок на фотографии. Функция скачивает их все и 
сохраняет в `save_path` с именами из их `url`.

- __Параметры:__

  - `nasa_token` - токен для работы с [NASA API](https://api.nasa.gov/#epic), 
полученный при [регистрации](https://api.nasa.gov/#signUp);

  - `images_path` - полный путь для сохранения картинок.


- __Пример вызова:__
```
from config import NASA_TOKEN, IMAGES_PATH


download_epic_images(NASA_TOKEN, IMAGES_PATH)
```