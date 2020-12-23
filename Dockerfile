FROM python:3.7.2-slim

RUN mkdir /code
COPY app.py /code/
COPY requirements.txt /code/

RUN pip install -r /code/requirements.txt

CMD ["python","/code/requirements.txt"]
