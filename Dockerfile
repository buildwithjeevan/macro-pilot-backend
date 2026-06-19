# Placeholder Dockerfile for MacroPilot backend
# Multi-stage build will be implemented in later phases.
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src /app/src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
