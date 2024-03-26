FROM python:3.10.13-alpine3.19

WORKDIR /usr/app

COPY . /usr/app

RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn","main:app","--host","0.0.0.0"]