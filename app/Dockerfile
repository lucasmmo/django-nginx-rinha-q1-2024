FROM python

EXPOSE 8000

WORKDIR /app

RUN apt update && apt upgrade -y

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache
