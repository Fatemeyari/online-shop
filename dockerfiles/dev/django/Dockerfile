FROM python:3.12-slim

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .


RUN pip install --upgrade pip && \
    pip install -r requirements.txt
    
COPY core/ .

CMD ["python3","main.py"]