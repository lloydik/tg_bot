FROM python
WORKDIR /app
COPY . .
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y build-essential libpq-dev postgresql postgresql-contrib openssh-client iputils-ping
RUN pip3 install -r requirements.txt
CMD sleep 10 && python main.py
