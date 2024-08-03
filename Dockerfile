FROM python:3
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY birthday_bot.py birthday_bot.py
CMD ["python3", "birthday_bot.py"]