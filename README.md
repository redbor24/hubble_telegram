## Скрипт hubble_telegram.py
При самостоятельном вызове скрипт сохраняет посредством функции 
`download_image` с заданного url картинку в файл с заданным именем. 

### download_image
Принимает параметрами `url` картинки и полное имя файла `full_filename`. 

Скачивает картинку по `url` и сохраняет её с именем `full_filename`. 
Если путь, заданный в `full_filename` не существует, то он создаётся.