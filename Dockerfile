FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
COPY requirements-serving.txt .
RUN pip install --no-cache-dir -r requirements-serving.txt
COPY serve.py model.joblib ./
USER 10001:10001
EXPOSE 8080
CMD ["python", "serve.py"]
