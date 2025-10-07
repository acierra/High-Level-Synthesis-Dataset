# parse_example: парсинг таблицы FPGA dev boards

Источник данных:  
[List of FPGA dev boards by vendor](https://www.fpgadeveloper.com/list-of-fpga-dev-boards-by-vendor/)

На странице опубликованы таблицы с разработческими платами FPGA разных производителей.


## Запуск
```bash
conda install lxml -n my_env
python3 parse_example/data_parser.py
