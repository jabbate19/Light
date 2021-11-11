FROM python:latest
LABEL maintainer="Joseph Abbate <josephabbateny@gmail.com>"

RUN apk add tzdata && \
    cp /usr/share/zoneinfo/America/New_York /etc/localtime && \
    echo "America/New_York" > /etc/timezone && \
    apk del tzdata

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

run python -m flask db upgrade

ENTRYPOINT ["gunicorn", "light:APP"]
CMD ["--bind=0.0.0.0:8080"]