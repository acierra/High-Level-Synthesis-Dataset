# api_example: поиск репозиториев с упоминанием GNWSIS

В этом примере используется **GitHub Search API**, чтобы найти все публичные проекты на GitHub, где встречается `GNWSIS` или `GNWSIS.csv`.  
Таким образом можно отследить, какие репозитории используют или упоминают датасет GNWSIS.

Документация API:  
https://docs.github.com/rest/search/search#search-code

## Запуск
```bash
сгенерировать токен на git_hub (https://github.com/settings/tokens)
export GITHUB_TOKEN=ghp_XXXXXXXXXXXXXXXXXXXXXXXXX

python3 api_example/api_reader.py
