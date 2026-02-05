FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY service/app /app/service/app
COPY artifacts /app/artifacts

ENV MODEL_PATH=/app/artifacts/iris_model.joblib
ENV PORT=8000

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
