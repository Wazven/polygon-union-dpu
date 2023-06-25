# Sebagai Base Image Python
FROM python:3.9-slim-buster

#Set untuk working dir di dalam container
WORKDIR /app

#Copy file yang diperlukan
COPY app.py .
COPY requirements.txt .
COPY .env .

#instal requirements.txt
# RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# ENV PIP_ROOT_USER_ACTION = ignore

#Expose port untuk fastAPI
EXPOSE 8000

#Terminal run
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# Cara Dockerfile
# install docker desktop
# Build Docker
# docker build -t your-image-name .
# docker run -p 8000:8000 your-image-name


