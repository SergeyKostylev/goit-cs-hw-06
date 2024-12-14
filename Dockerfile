FROM python:3.12-slim

WORKDIR /app

COPY ./app /app

EXPOSE 3000
EXPOSE 5099

RUN pip install --no-cache-dir -r requirements.txt

# ws running
CMD ["python", "main.py"]