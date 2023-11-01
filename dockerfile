FROM python:3.11
WORKDIR /app
COPY lambda_function.py /app/
CMD ["python3", "lambda_function.py"]