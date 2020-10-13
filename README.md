## How to launch a spider
 - Create a virtualEnv Python2.
 - Install NEUKOLLN.
 - Launch new_vivanuncios.py.
 - Extract all URLS and put them into a csv file.
 - Add the previous csv file as an input in the second spider spider_parsing.py

<hr>

## Follow this steps


- Activate the virtual_env venv_py2
```
source venv_py2/bin/activate
```


- Launch each spider in different Screen
```
scrapy crawl new_vivanuncios -o spider_urls.csv
scrapy crawl spider_parsing -o spider_parsing.csv

```

- Execute the post_process in Jupyter Notebook
```
Vivanuncios.ipynb

```

- Drop duplicate
```
sort -u -k3,3 -t";" spider_parsing.csv > merge_file_without_dup.csv

