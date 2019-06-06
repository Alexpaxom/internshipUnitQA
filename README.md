# Тестовый проект для вакансии "Стажёр в юнит QA"

Программа обрабатывает три файла(с логами о тестировании) в формате json, и формирует файл с собранной информацией о всех тестах (также формате json).
Все файлы валидируются с помощью JSON Schema, schema-файлы задаются в файле с настройками settings.json.

Программа расчитана на работу через консоль. На вход подаются следующие параметры с следующими ключами
-f1 (путь к первому файлу)

-f2 (путь ко второму файлу)

-f3 (путь к третьему файлу)

-o (путь к результирующему файлу)

### Пример:
  python -f1 path_to_file/File_1 -f2 path_to_file/File_2 -f3 path_to_file/File_3 -o path_to_file/output.json
  
Для того что бы проверить программу на работоспособность, можно запустить unittests, для этого можно воспользоваться стандартной модулем python unittest
### Пример:
  python -m unittest discover tests
  
 ## Requirements
 Python 3.7
 
 Все зависимости можно установить с помощью pip
 
jsonschema

jsonschema[format]
