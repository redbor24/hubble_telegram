## hubble_telegram.py
### Функции
#### download_image
Принимает параметрами `url` картинки и полное имя файла `full_filename`. 

Скачивает картинку по `url` и сохраняет её с именем `full_filename`. 
Если путь, заданный в `full_filename` не существует, то он создаётся.

#### fetch_spacex_last_launch
Принимает параметрами `id` запуска и полный путь к папке для сохранения 
картинок.

Обращается к [api.spacexdata.com](https://api.spacexdata.com/v4/launches/)
по id запуска `id_launch`, скачивает всё картинки указанного запуска и 
сохраняет их в `save_path` под именами `spacex1.jpg`, `spacex2.jpg`, ...,
`spacexN.jpg`.

#### get_file_ext_from_url
Принимает параметром `url`
Возвращает расширение имени файла из переданного `url`

#### get_apod_images
Принимает параметрами 
1. `nasa_token` - токен для работы с [NASA API](https://api.nasa.gov/), 
полученный при [регистрации](https://api.nasa.gov/#signUp)
2. `save_path` - полный путь для сохранения картинок
3. `image_count` - количество картинок для получения

Обращается к [NASA API](https://api.nasa.gov/v4/apod) за указанным количеством
астрономических картинок дня, скачивает их всё и 
сохраняет их в `save_path` под именами, взятыми из их url. Для ссылок, 
указывающих на видео, сохраняется его thumbnail под именем `spacexN.jpg`
