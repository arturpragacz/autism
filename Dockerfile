FROM python:3

ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN ./manage.py migrate
RUN ./manage.py loaddata test/fixtures/data.json

EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
