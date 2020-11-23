FROM python:3.8-alpine

WORKDIR /src/api

# System setup
RUN apk update
RUN apk add build-base gcc abuild binutils binutils-doc gcc-doc
RUN apk add python3-dev
RUN apk add mariadb-dev
COPY . /src
EXPOSE 5000


# Python setup
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN pip3 install pipenv
RUN pipenv install --system --deploy
RUN pip install gunicorn

COPY . /src/api

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
