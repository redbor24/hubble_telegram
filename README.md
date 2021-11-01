# Проект hubble_telegram
_ _ _
Программа отправляет Telegram-пользователям случайные изображения с сайта NASA 
на космическую тематику с заданной периодичностью.

Имя telegram-бота [@devman-hubble](https://t.me/spacexhubble_bot)

### Зависимости
```
requests==2.26.0
python-telegram-bot==13.7
python-decouple==3.5
```

### Переменные окружения
Переменная среды `DELIVERY_TIMEOUT` хранит периодичность отправки изображений
пользователям Telegram в секундах. Если переменная не задана, то берётся
значение 10.

## telegram_bot.py
_ _ _
При получении команды `/start` отправляет сообщение `Hi! I'm a bot 
@devman_hubble!` и публикует одну случайную астрономическую картинку дня.

При получении команды `/hello` отправляет сообщение `Hi! I'm a bot 
@devman_hubble!`.

## nasa.py
_ _ _
Содержит набор функций для скачивания: 
1. Фотографий запусков космических кораблей компании [SpaceX](https://www.spacex.com/);
2. Фотографий нашей планеты из космоса.

### Функции

#### download_image
Скачивает картинку по `url` и сохраняет её с именем `full_filename`. 
Если путь, заданный в `full_filename` не существует, то он создаётся.

+ __Параметры:__

    `url` картинки;

    `full_filename` полное имя файла;

    `params` словарь для передачи в секцию `params` get-запроса. Необязательный 
  параметр.

- __Вызов:__
```
from nasa import download_image 


download_image('https://apod.nasa.gov/apod/image/2107/LRVBPIX3M82Crop1024.jpg',
               Path(os.getcwd()) / 'testimg' / 'nasa_image.jpg')
```

#### get_launches_with_images
В общем массиве информации о запусках компании 
[SpaceX](https://www.spacex.com/) содержатся фотографии не для каждого запуска.
Функция отбирает запуски, у которых имеются ссылки на изображения и 
возвращает их список с количеством ссылок на изображения для каждого запуска.

+ __Параметры:__

    `nasa_token` - токен для работы с [NASA API](https://api.nasa.gov/), 
полученный при [регистрации](https://api.nasa.gov/#signUp)

- __Возвращает:__
    Cписок словарей `id, count`, где `id` - id запуска, `count` - 
количество изображений.

- __Вызов:__
```
from nasa import get_launches_with_images


NASA_TOKEN = decouple.config('NASA_TOKEN', '')
image_list = get_launches_with_images(NASA_TOKEN)
print(*image_list, sep='\n')
```

#### fetch_spacex_launch
Обращается к [NASA API](https://api.spacexdata.com/v4/launches/)
по `id` запуска, скачивает всё имеющиеся в ответе картинки запуска и 
сохраняет их в `save_path` под именами `spacex1.jpg`, `spacex2.jpg`, ...,
`spacexN.jpg`.

- __Параметры:__
  
    `launch_id` запуска космического корабля SpaceX. Выбирается из результата 
    выполнения функции `get_launches_with_images`;

    `save_path` абсолютный путь для сохранения картинок.


- __Возвращает:__
    Список имён файлов сохранённых изображений с полными путями


- __Вызов:__
```
from nasa import get_launches_with_images, fetch_spacex_launch 


NASA_TOKEN = decouple.config('NASA_TOKEN', '')
launch_list = get_launches_with_images(NASA_TOKEN)
image_list = fetch_spacex_launch(launch_list[0]['id'], Path(os.getcwd()) / 'spacex')
print(*image_list, sep='\n')
image_list = fetch_spacex_launch(launch_list[1]['id'], 'c:\spacex')
print(*image_list, sep='\n')
```

#### get_file_ext_from_url
Возвращает расширение имени файла из переданного `url`

- __Параметры:__
    `url`

- __Вызов:__
```
from nasa import get_file_ext_from_url 


print(get_file_ext_from_url('https://apod.nasa.gov/apod/image/2107/LRVBPIX3M82Crop1024.jpg'))
print(get_file_ext_from_url('https://google.com'))
print(get_file_ext_from_url('google.com'))
```

#### get_apod_images
Обращается к [NASA API](https://api.nasa.gov/) за указанным количеством 
астрономических картинок дня
([APOD - Astronomy Picture of the Day](https://api.nasa.gov/#apod)),
скачивает их в `save_path` под именами, взятыми из их url. 
Для ссылок, указывающих на видео, сохраняется его `thumbnail` 
под именем `apodN.jpg`

- __Параметры:__
    
    `nasa_token` - токен для работы с [NASA API](https://api.nasa.gov/), 
полученный при [регистрации](https://api.nasa.gov/#signUp);

    `save_path` - полный путь для сохранения картинок;

    `image_count` - количество картинок для получения.


- __Возвращает:__
    Список имён файлов сохранённых изображений с полными путями


- __Вызов:__
```
from nasa import get_apod_images 


image_list = get_apod_images(NASA_TOKEN, Path(os.getcwd()) / 'apod', 10)
print(*image_list, sep='\n')
```

#### get_epic_images
Обращается к [NASA API](https://api.nasa.gov/EPIC/api/natural?api_key=DEMO_KEY) 
за фотографиями нашей планеты из космоса. Ответ на один запрос содержит 
несколько ссылок на фотографии. Функция скачивает их всё и 
сохраняет их в `save_path` с именами, взятыми из их `url`.

- __Параметры:__

    `nasa_token` - токен для работы с [NASA API](https://api.nasa.gov/#epic), 
полученный при [регистрации](https://api.nasa.gov/#signUp);

    `save_path` - полный путь для сохранения картинок.


- __Возвращает:__
    Список имён файлов сохранённых изображений с полными путями


- __Пример вызова:__
```
image_list = get_epic_images(NASA_TOKEN, Path(os.getcwd()) / 'epic')
print(*image_list, sep='\n')
```
