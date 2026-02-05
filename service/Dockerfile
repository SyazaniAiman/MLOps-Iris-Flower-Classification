FROM python:3.11

WORKDIR /app

COPY service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY service/app/ /app/
COPY artifacts/ /app/artifacts/

ENV MODEL_PATH=/app/artifacts/iris_model.joblib
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
