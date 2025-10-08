# Dockerfile for FastAPI app
FROM python:3.11-slim
RUN  apt-get update
RUN apt-get install -y build-essential
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt  --trusted-host pypi.org --trusted-host files.pythonhosted.org
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
