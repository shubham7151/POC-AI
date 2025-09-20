FROM python:3.10

WORKDIR /code

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app /code/app

CMD [ "fastapi", "run", "app/api/main.py", "--port", "80" ]