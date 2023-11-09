import bit
import random
import json
import threading

MAX_INT = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140
MAX_TRIES = 10000000000000

def check_prefix(prefix, address):
    return address.startswith(prefix)

def generate_vanity_address(prefix, result):
    if len(prefix) > 15:
        result.append({
            'statusCode': 400,
            'body': json.dumps({
                'error': "The prefix cannot exceed 15 characters."
            })
        })
        return

    for _ in range(MAX_TRIES):
        private_key_bytes = random.randint(1, MAX_INT).to_bytes(32, byteorder='big')
        private_key = bit.PrivateKey(bit.format.bytes_to_wif(private_key_bytes))
        address = private_key.address

        if check_prefix(prefix, address):
            result.append({
                'statusCode': 200,
                'body': json.dumps({
                    'prefix': prefix,
                    'private_key': private_key.to_wif(),
                    'address': address
                })
            })
            return
    result.append({
        'statusCode': 404,
        'body': json.dumps({
            'error': "No matching address found within the maximum number of tries."
        })
    })

def lambda_handler(event, context):
    prefix = event['prefix']
    result = []
    
    generate_vanity_address(prefix, result)
    
    return result[0] if result else None

# Ler o conteúdo do arquivo JSON diretamente
content = sys.stdin.read()

# Converter o conteúdo do arquivo JSON em um objeto Python
event = json.loads(content)

# Passar o evento para a função lambda_handler e imprimir o resultado
result = lambda_handler(event, None)
print(result)
