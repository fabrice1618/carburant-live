FROM python:3.9

RUN mkdir /data

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["python3", "-u", "backend.py"]
