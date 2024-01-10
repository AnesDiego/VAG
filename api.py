Python 3.11.7 (tags/v3.11.7:fa7a6f2, Dec  4 2023, 19:24:49) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> Python
... from fastapi import FastAPI
... from pydantic import BaseModel, constr
... from typing import Optional
... import bit
... import random
... import json
... 
... MAX_INT = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140
... MAX_TRIES = 10000000000000
... 
... app = FastAPI()
... 
... class Prefix(BaseModel):
...     prefix: constr(min_length=1, max_length=15)
... 
... class Address(BaseModel):
...     prefix: str
...     private_key: str
...     address: str
... 
... class Error(BaseModel):
...     error: str
... 
... @app.get("/generate", response_model=Optional[Address, Error])
... async def generate_address(prefix: Prefix):
...     for _ in range(MAX_TRIES):
...         private_key_bytes = random.randint(1, MAX_INT).to_bytes(32, byteorder='big')
...         private_key = bit.PrivateKey(bit.format.bytes_to_wif(private_key_bytes))
...         address = private_key.address
... 
...         if address.startswith(prefix.prefix):
...             return Address(
...                 prefix=prefix.prefix,
...                 private_key=private_key.to_wif(),
...                 address=address
...             )
...     return Error(
...         error="No matching address found within the maximum number of tries."
...     )
