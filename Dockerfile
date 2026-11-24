FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

COPY api_cisco.py main.py ./

CMD ["python", "main.py"]