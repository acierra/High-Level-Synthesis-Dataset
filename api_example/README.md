# api_example: поиск репозиториев с упоминанием GNWSIS
![api_reader.png]([https://github.com/acierra/High-Level-Synthesis-Dataset/blob/main/docs/Screenshot%202025-09-22%20at%2001.22.42.png](https://github.com/acierra/High-Level-Synthesis-Dataset/tree/main/screenshots#:~:text=4%20minutes%20ago-,api_reader.png,-hw_4))
В этом примере используется **GitHub Search API**, чтобы найти все публичные проекты на GitHub, где встречается `GNWSIS` или `GNWSIS.csv`.  
Таким образом можно отследить, какие репозитории используют или упоминают датасет GNWSIS.

Документация API:  
https://docs.github.com/rest/search/search#search-code

## Запуск
```bash
сгенерировать токен на git_hub (https://github.com/settings/tokens)
export GITHUB_TOKEN=ghp_XXXXXXXXXXXXXXXXXXXXXXXXX

python3 api_example/api_reader.py
