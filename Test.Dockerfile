FROM python:3
WORKDIR /app
COPY requirements.txt requirements.txt
COPY conftest.py conftest.py
COPY test_secret_token.txt secret_token.txt
COPY .coveragerc .coveragerc
RUN pip3 install -r requirements.txt
RUN mkdir birthday_bot
COPY birthday_bot /app/birthday_bot
RUN mkdir test
COPY test test/
CMD ["pytest", "test", "-W ignore::DeprecationWarning", "--junit-xml=/app/results.xml", "--cov=/app/birthday_bot/", "--cov-report", "term-missing", "--cov-config=/app/.coveragerc"]