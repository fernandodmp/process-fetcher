# Process-Fetcher

A unified web interface where users can fetch data from differents tribunals

### Requirements

- Python 3.6.5
- Django 2
- BeautifulSoup
- Selenium
- Celery
- Html5lib
- Pandas
- django_celery_results
- Chrome WebDriver
- RabbitMQ


### Install Requirements

`pip install -r requirements.txt`

O chrome Web Driver deve ser baixado e instalado manualmente conforme o site: http://chromedriver.chromium.org/downloads.

O RabbitMQ também deve ser baixado e instalado manualmente comforme o site: https://www.rabbitmq.com/download.html.

### How to use
Em um terminal na pasta do repositório inicie o Celery conforme o comando abaixo:

`celery -A challenge  worker`

Em um outro terminal utilize o comando abaixo para iniciar o servidor da interface web:

`python manage.py runserver`

Caso seja necessário, faça as migrações com:

`python manage.py migrate`
