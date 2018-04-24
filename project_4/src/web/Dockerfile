FROM continuumio/miniconda3

COPY ./app /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD python app.py
