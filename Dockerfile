FROM python:3.9.8-bullseye
LABEL maintainer="Joseph Abbate <josephabbateny@gmail.com>"

WORKDIR /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

run python -m flask db upgrade

ENTRYPOINT ["gunicorn", "light:APP"]
CMD ["--bind=0.0.0.0:8080"]