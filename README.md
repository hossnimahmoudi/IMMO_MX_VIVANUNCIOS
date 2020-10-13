## How to launch a spider
 - Activate a virtualEnv Python2, if not :
 - Install NEUKOLLN.
 - Activate the virtualEnv virtualenv_py3.
 - Launch new_vivanuncios.py.
 - Extract all URLS and put them into a csv file.
 - Add the previous csv file as an input in the second spider spider_parsing.py

<hr>

## Follow this steps


- Activate the virtual_env venv_py2
```
source venv_py2/bin/activate
```


- Launch the spider in a Screen
```
scrapy crawl new_vivanuncios -o spider_urls.csv

```

- Activate the virtual_env virtualenv_py3
```
source virtualenv_py3/bin/activate
```

- Launch the spider in a Screen
```
scrapy crawl new_vivanuncios -o spider_urls.csv

```

- Execute the post_process in Jupyter Notebook
```
Vivanuncios.ipynb

```

- Drop duplicate
```
sort -u -k3,3 -t";" spider_parsing.csv > merge_file_without_dup.csv

