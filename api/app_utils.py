import base64
import json
import time
from decouple import config
from jose.constants import ALGORITHMS
from jose.exceptions import JWKError
from jose.jwt import encode

# Function to decode base64url-encoded data
def base64url_decode(data):
    padding = b'=' * (4 - (len(data) % 4))
    data = data.replace(b'-', b'+').replace(b'_', b'/') + padding
    return base64.b64decode(data)

def create_jwt_token(user_id):
    try:
        jwt_header = {
            "alg": power_sync_private_key_json["alg"],
            "kid": power_sync_private_key_json["kid"],
        }

        jwt_payload = {
            "sub": user_id,
            "iat": time.time(),
            "iss": "http://127.0.0.1:8000/",
            "aud": power_sync_url,
            "exp": int(time.time()) + 300,  # 5 minutes expiration
        }

        token = encode(
            jwt_payload,
            power_sync_private_key_json,
            algorithm=ALGORITHMS.RS256,
            headers=jwt_header
        )

        return token

    except (JWKError, ValueError, KeyError) as e:
        raise Exception(f"Error creating JWT token: {str(e)}")

# PowerSync private key
power_sync_private_key_b64 = config('POWERSYNC_PRIVATE_KEY')

# PowerSync Url
power_sync_url = config('POWERSYNC_URL')

# PowerSync public key
power_sync_private_key_bytes = base64url_decode(power_sync_private_key_b64.encode('utf-8'))
power_sync_private_key_json = json.loads(power_sync_private_key_bytes.decode('utf-8'))