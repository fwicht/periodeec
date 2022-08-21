FROM python:3.11-rc-bullseye

RUN apt-get update && apt-get upgrade -y

WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt

CMD python3 "app.py"