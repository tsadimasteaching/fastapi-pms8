FROM python:3.10.13-alpine3.19

RUN apk update && apk add gcc  libc-dev

WORKDIR /usr/data

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN addgroup -S appuser && adduser -S appuser -G appuser  --home /usr/data

ENV PATH=$PATH:/usr/data/.local/bin

COPY ./requirements.txt .

COPY . /usr/data

RUN pip install -r requirements.txt

RUN chown -R appuser:appuser /usr/data

USER appuser:appuser

EXPOSE 8000/tcp
CMD ["uvicorn","main:app","--host", "0.0.0.0", "--port", "8000"]