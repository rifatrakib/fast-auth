FROM python:3.9-slim

COPY ./server /api/server
COPY ./requirements.txt /api/requirements.txt

WORKDIR /api

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "server.main:app", "--host=0.0.0.0", "--reload"]
