FROM python:3.10

WORKDIR /app/chatbot

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app/chatbot

CMD ["uvicorn", "src.main:app", "--port", "8000"]