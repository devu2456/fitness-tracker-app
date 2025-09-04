FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install coverage

COPY src/ src/
COPY tests/ tests/

CMD ["python", "src/app.py"]