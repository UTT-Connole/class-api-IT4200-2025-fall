FROM python:3.11

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8000
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]