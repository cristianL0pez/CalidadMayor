FROM python:3.10.0-alpine
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./ /Proyecto_ficha

WORKDIR /Proyecto_ficha






