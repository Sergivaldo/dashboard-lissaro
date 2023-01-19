import base64

import rsa


def generate_keys():
    return rsa.newkeys(1024)


def encrypt(message, key):
    ciphertext = rsa.encrypt(message.encode('ascii'), key)
    ciphertextB64 = base64.b64encode(ciphertext).decode('utf8')
    return ciphertextB64


def decrypt(ciphertext, key):
    try:
        decrypted = base64.b64decode(ciphertext)
        return rsa.decrypt(decrypted, key).decode('ascii')
    except Exception:
        return False


def save_private_key(private_key):
    return private_key.save_pkcs1().decode('utf-8')


def save_public_key(public_key):
    return public_key.save_pkcs1().decode('utf-8')


def get_private_key(private_key):
    return rsa.PrivateKey.load_pkcs1(private_key.encode('utf8'))


def get_public_key(public_key):
    return rsa.PublicKey.load_pkcs1(public_key.encode('utf8'))
