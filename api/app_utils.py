import base64
import json
import time
import os
from decouple import config
from jose.constants import ALGORITHMS
from jose.exceptions import JWKError
from jose.jwt import encode
from jose import jwk
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import random
import string

# Function to decode base64url-encoded data


def base64url_decode(data):
    padding = b'=' * (4 - (len(data) % 4))
    data = data.replace(b'-', b'+').replace(b'_', b'/') + padding
    return base64.b64decode(data)

# Function to generate a new RSA key pair and return in JWK format


def generate_key_pair():
    alg = 'RS256'
    kid = 'powersync-' + \
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    private_key_jwk = jwk.construct(
        private_key_pem, algorithm=ALGORITHMS.RS256).to_dict()
    private_key_jwk.update({'alg': alg, 'kid': kid})

    public_key_jwk = jwk.construct(
        public_key_pem, algorithm=ALGORITHMS.RS256).to_dict()
    public_key_jwk.update({'alg': alg, 'kid': kid})

    private_base64 = base64.urlsafe_b64encode(json.dumps(
        private_key_jwk).encode('utf-8')).decode('utf-8')
    public_base64 = base64.urlsafe_b64encode(json.dumps(
        public_key_jwk).encode('utf-8')).decode('utf-8')

    return private_base64, public_base64
# Function to ensure keys are available

# Function to ensure keys are available


def ensure_keys():
    global power_sync_private_key_json, power_sync_public_key_json

    power_sync_private_key_b64 = config('POWERSYNC_PRIVATE_KEY', default=None)
    power_sync_public_key_b64 = config('POWERSYNC_PUBLIC_KEY', default=None)

    if not power_sync_private_key_b64 or not power_sync_public_key_b64 or not power_sync_private_key_b64.strip() or not power_sync_public_key_b64.strip():
        print('Private key has not been supplied in the environment. A temporary key pair will be generated.')
        private_key_base64, public_key_base64 = generate_key_pair()
        power_sync_private_key_b64 = private_key_base64
        power_sync_public_key_b64 = public_key_base64

        # Save the keys to environment variables (only for this session, won't persist across restarts)
        os.environ['POWERSYNC_PRIVATE_KEY'] = power_sync_private_key_b64
        os.environ['POWERSYNC_PUBLIC_KEY'] = power_sync_public_key_b64

    power_sync_private_key_bytes = base64url_decode(
        power_sync_private_key_b64.encode('utf-8'))
    power_sync_private_key_json = json.loads(
        power_sync_private_key_bytes.decode('utf-8'))

    power_sync_public_key_bytes = base64url_decode(
        power_sync_public_key_b64.encode('utf-8'))
    power_sync_public_key_json = json.loads(
        power_sync_public_key_bytes.decode('utf-8'))


# Ensure keys are available
ensure_keys()

# PowerSync URL
power_sync_url = config('POWERSYNC_URL')


def create_jwt_token(user_id):
    try:
        jwt_header = {
            "alg": power_sync_private_key_json["alg"],
            "kid": power_sync_private_key_json["kid"],
        }

        jwt_payload = {
            "sub": user_id,
            "iat": time.time(),
            "iss": "https://d9ae-2601-282-1800-d970-7da1-854e-b9a7-98d.ngrok-free.app",
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
