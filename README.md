## Скрипт hubble_telegram.py
При самостоятельном вызове скрипт для заданного `id` запуска посредством 
функции `fetch_spacex_last_launch` скачивает все картинки запуска и 
сохраняет их в подпапку `\images` в папке запуска скрипта. 

### download_image
Принимает параметрами `url` картинки и полное имя файла `full_filename`. 

Скачивает картинку по `url` и сохраняет её с именем `full_filename`. 
Если путь, заданный в `full_filename` не существует, то он создаётся.

### fetch_spacex_last_launch
Принимает параметрами `id` запуска и полный путь к папке для сохранения 
картинок.

Обращается к [api.spacexdata.com](https://api.spacexdata.com/v4/launches/)
по `id_launch` запуска, скачивает всё картинки указанного запуска и 
сохраняет их в `save_path` под именами `spacex1.jpg`, `spacex2.jpg`, ...,
`spacexN.jpg`.