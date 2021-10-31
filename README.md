# Проект hubble_telegram
_ _ _
### Зависимости
```
requests==2.26.0
python-telegram-bot==13.7
python-decouple==3.5
```
## telegram_bot.py
_ _ _
Код Телеграм-бота
_ _ _
## nasa.py
Содержит набор функций для скачивания фотографий: 
1. Запусков космических кораблей компании [SpaceX](https://www.spacex.com/);
2. Нашей планеты из космоса 
[NASA API](https://api.nasa.gov/EPIC/api/natural?api_key=DEMO_KEY).

### Функции
_ _ _
#### download_image
Параметры:
1. `url` картинки;
2. `full_filename` полное имя файла;
3. `params` словарь для передачи в секцию `params` get-запроса. Необязательный 
параметр.

Скачивает картинку по `url` и сохраняет её с именем `full_filename`. 
Если путь, заданный в `full_filename` не существует, то он создаётся.

*Пример вызова:*
```
download_image('https://apod.nasa.gov/apod/image/2107/LRVBPIX3M82Crop1024.jpg',
               Path(os.getcwd()) / 'testimg' / 'nasa_image.jpg')
```
_ _ _
#### get_launches_with_images
Параметры:
1. `nasa_token` - токен для работы с [NASA API](https://api.nasa.gov/), 
полученный при [регистрации](https://api.nasa.gov/#signUp)

Не каждый запуск космического корабля компании 
[SpaceX](https://www.spacex.com/) содержит фотографии. Функция
отбирает запуски, у которых имеются ссылки на фотоматериалы и 
возвращает их список с количеством ссылок на фотографии для каждого запуска.

*Пример вызова:*
```
NASA_TOKEN = decouple.config('NASA_TOKEN', '')
list = get_launches_with_images(NASA_TOKEN)
print(*list, sep='\n')
```
_ _ _
#### fetch_spacex_launch
Параметры:
1. `launch_id` запуска космического корабля SpaceX. Выбирается из результата 
выполнения функции `get_launches_with_images`;
2. `save_path` абсолютный путь для сохранения картинок.

Обращается к [NASA API](https://api.spacexdata.com/v4/launches/)
по `id` запуска, скачивает всё имеющиеся в ответе картинки запуска и 
сохраняет их в `save_path` под именами `spacex1.jpg`, `spacex2.jpg`, ...,
`spacexN.jpg`.

*Пример вызова:*
```
NASA_TOKEN = decouple.config('NASA_TOKEN', '')
list = get_launches_with_images(NASA_TOKEN)
fetch_spacex_launch(list[0]['id'], Path(os.getcwd()) / 'testimg')
```
_ _ _
#### get_file_ext_from_url
Параметры:
1. `url`

Возвращает расширение имени файла из переданного `url`

*Пример вызова:*
```
print(get_file_ext_from_url('https://apod.nasa.gov/apod/image/2107/LRVBPIX3M82Crop1024.jpg'))
print(get_file_ext_from_url('https://google.com'))
print(get_file_ext_from_url('google.com'))
```
_ _ _
#### get_apod_images
Параметры:
1. `nasa_token` - токен для работы с [NASA API](https://api.nasa.gov/), 
полученный при [регистрации](https://api.nasa.gov/#signUp);
2. `save_path` - полный путь для сохранения картинок;
3. `image_count` - количество картинок для получения.

Обращается к [NASA API](https://api.nasa.gov/) за указанным количеством 
астрономических картинок дня
([APOD - Astronomy Picture of the Day](https://api.nasa.gov/#apod)),
скачивает их всё и сохраняет их в `save_path` под именами, взятыми из их url. 
Для ссылок, указывающих на видео, сохраняется его `thumbnail` 
под именем `spacexN.jpg`

*Пример вызова:*
```
get_apod_images(NASA_TOKEN, Path(os.getcwd()) / 'apod', 10)
```
_ _ _
#### get_epic_images
Параметры:
1. `nasa_token` - токен для работы с [NASA API](https://api.nasa.gov/#epic), 
полученный при [регистрации](https://api.nasa.gov/#signUp);
2. `save_path` - полный путь для сохранения картинок.

Обращается к [NASA API](https://api.nasa.gov/EPIC/api/natural?api_key=DEMO_KEY) 
за фотографиями нашей планеты из космоса. Ответ на один запрос содержит 
несколько ссылок на фотографии. Функция скачивает их всё и 
сохраняет их в `save_path` с именами, взятыми из их `url`.

*Пример вызова:*
```
get_epic_images(NASA_TOKEN, Path(os.getcwd()) / 'epic')
```
