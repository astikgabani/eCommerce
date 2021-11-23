FROM python:3.8

WORKDIR /ecom-api-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./package .

CMD [ "python", "wsgi.py" ]
