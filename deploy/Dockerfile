FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get -y install libpq-dev gcc

RUN mkdir /dicom_router
WORKDIR /dicom_router

COPY requirements.txt /dicom_router
RUN pip3 install -r requirements.txt
ADD ./dicom_router /dicom_router/

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py superuser --user admin --email naserfuni@gmail.com --password admin && python manage.py collectstatic --noinput && python app.py && gunicorn dicom_router.wsgi:application --bind 0.0.0.0:8080 --timeout 600"]
