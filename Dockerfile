FROM python:3.9.8-bullseye
LABEL maintainer="Joseph Abbate <josephabbateny@gmail.com>"

WORKDIR /app/
COPY requirements.txt /app/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/

run python -m flask db upgrade; exit 0

ENTRYPOINT ["gunicorn", "light:APP"]
CMD ["--bind=0.0.0.0:8080"]