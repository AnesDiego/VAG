FROM python:3.11
WORKDIR /vag
COPY lambda_function.py /vag/
CMD ["python3", "lambda_function.py"]