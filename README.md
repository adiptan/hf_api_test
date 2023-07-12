## Описание
Скрипт импортирует кандидатов из xlsx-файла в Хантфлоу. 
### Этапы работы скрипта
 - Кандидату прикрепляется файл
 - Кандидат прикрепляется к вакансии и помещается на указанный статус.
 - Добавляется комментарий.

## Установка
Выполнить последовательно следующие команды:
```
git clone https://github.com/besseneger/hf_api_test.git
cd hf_api_test
python3 -m venv my_env
source my_env/bin/activate
pip3 install -r requirements.txt
```
После установки, необходимо:
 - Переименовать файл `.env_template` -> `.env`
 - В файле `.env` необходимо поменять на актуальные значения в переменных `URL` и `TOKEN`.
 
#### Запуск скрипта
Пример запуска:
```
python main.py --db_path=data
```
Где: 
 - `--db_path` - путь к папке, в которой лежит excel-файл.
