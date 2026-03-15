FROM python:3.13.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "interfaces.api.routes.transactions:app", "--host", "0.0.0.0", "--port", "8000"]