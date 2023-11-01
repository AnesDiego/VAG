FROM python:3.11
WORKDIR /app
COPY asn1crypto /app/asn1crypto
COPY asn1crypto-1.5.1.dist-info /app/asn1crypto-1.5.1.dist-info
COPY bit /app/bit
COPY bit-0.8.0.dist-info /app/bit-0.8.0.dist-info
COPY certifi /app/certifi
COPY certifi-2023.7.22.dist-info /app/certifi-2023.7.22.dist-info
COPY cffi /app/cffi
COPY cffi-1.16.0.dist-info /app/cffi-1.16.0.dist-info
COPY charset_normalizer /app/charset_normalizer
COPY charset_normalizer-3.3.0.dist-info /app/charset_normalizer-3.3.0.dist-info
COPY coincurve /app/coincurve
COPY coincurve-18.0.0.dist-info /app/coincurve-18.0.0.dist-info
COPY idna /app/idna
COPY idna-3.4.dist-info /app/idna-3.4.dist-info
COPY pycparser /app/pycparser
COPY pycparser-2.21.dist-info /app/pycparser-2.21.dist-info
COPY requests /app/requests
COPY requests-2.31.0.dist-info /app/requests-2.31.0.dist-info
COPY tests /app/tests
COPY tqdm /app/tqdm
COPY tqdm-4.66.1.dist-info /app/tqdm-4.66.1.dist-info
COPY urllib3 /app/urllib3
COPY urllib3-2.0.6.dist-info /app/urllib3-2.0.6-dist.info
COPY lambda_function.py /app/
CMD ["python3", "lambda_function.py"]