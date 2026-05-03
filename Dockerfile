FROM python:3.11-slim
WORKDIR /usr/src/assignMe_discordBot
COPY . .
RUN apt update && apt install python3-dev pkg-config python3-pip default-libmysqlclient-dev build-essential -y
RUN pip3 install mysqlclient requests discord.py
CMD ["sh", "-c", "python3 main.py"]