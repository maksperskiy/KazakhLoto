FROM python:3.9

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app

RUN sed -i -e 's/localhost/postgres/; s/15432/5432/' config.py
CMD python /app/app.py