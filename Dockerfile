FROM python:3.11
WORKDIR /app
COPY asn1crypto /asn1crypto
COPY asn1crypto-1.5.1.dist-info /asn1crypto-1.5.1.dist-info
COPY bit /bit
COPY bit-0.8.0.dist-info /bit-0.8.0.dist-info
COPY certifi /certifi
COPY certifi-2023.7.22.dist-info /certifi-2023.7.22.dist-info
COPY cffi /cffi
COPY cffi-1.16.0.dist-info /cffi-1.16.0.dist-info
COPY charset_normalizer /charset_normalizer
COPY charset_normalizer-3.3.0.dist-info /charset_normalizer-3.3.0.dist-info
COPY coincurve /coincurve
COPY coincurve-18.0.0.dist-info /coincurve-18.0.0.dist-info
COPY idna /idna
COPY idna-3.4.dist-info /idna-3.4.dist-info
COPY pycparser /pycparser
COPY pycparser-2.21.dist-info /pycparser-2.21.dist-info
COPY requests /requests
COPY requests-2.31.0.dist-info /requests-2.31.0.dist-info
COPY tests /tests
COPY tqdm /tqdm
COPY tqdm-4.66.1.dist-info /tqdm-4.66.1.dist-info
COPY urllib3 /urllib3
COPY urllib3-2.0.6.dist-info /urllib3-2.0.6.dist-info
COPY _cffi_backend.cpython-311-x86_64-linux-gnu.so /
COPY lambda_function.py /app/
RUN chmod +x /app/lambda_function.py
EXPOSE 8080
CMD ["python3", "/app/lambda_function.py"]