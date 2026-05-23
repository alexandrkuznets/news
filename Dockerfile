FROM python:3.12-slim

WORKDIR /app/

RUN pip install --upgrade pip

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

