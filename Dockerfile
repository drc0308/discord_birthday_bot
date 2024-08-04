FROM python:3
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir birthday_bot
COPY birthday_bot /app/birthday_bot
CMD ["python3", "birthday_bot/birthday_bot.py"]