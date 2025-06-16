FROM python:3.8-slim-buster

RUN apt update -y && apt install awscli -y
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

COPY src/ /app/src/
COPY app.py /app/

RUN mkdir -p /app/artifacts/training/
COPY artifacts/training/model.h5 /app/artifacts/training/model.h5

RUN ls -la /app/artifacts/training/

EXPOSE 8080

CMD ["python3", "app.py"]