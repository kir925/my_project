FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./main.py /app/main.py
COPY ./data_downloader /app/data_downloader

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
