import base64
import binascii
import hashlib
from typing import Union
from Crypto.Cipher import AES

__all__ = [
    "md5",
    "b64encode",
    "b64decode",
    "decrypt",
    "encrypt",
    "DEFAULT_CRYPTO_KEY",
    "DEFAULT_CRYPTO_IV",
]
UTF8 = "utf-8"
DEFAULT_CRYPTO_KEY = 'TfvY7I358yospfWKcoviZizOShpm5hyH'  # 32
DEFAULT_CRYPTO_IV = 'abcde56789012345abcde56789012345'  # 16


def md5(content: str) -> str:
    m = hashlib.md5()
    m.update(content.encode(UTF8))
    return m.hexdigest()


def b64encode(content: str) -> str:
    return base64.b64encode(content.encode(UTF8)).decode(UTF8)


def b64decode(content: str) -> str:
    return base64.b64decode(content.encode(UTF8)).decode(UTF8)


def decrypt(
        values: Union[list, dict],
        crypt_key: str,
        crypt_iv: str,
        prefix: str = "#",
        seg_size=128) -> Union[list, dict]:
    """
    prefix: filter string needs to be decrypted. Empty for non prefix
    segment_size: Python uses 8-bit segments by default for legacy reasons.
        In order to support languages that encrypt using 128-bit segments,
        without having to use data with a length divisible by 16,
        we need to pad and truncate the values.
    """  # noqa:E501
    if not values or type(values) not in (list, dict):
        return values
    iv_bt = binascii.unhexlify(crypt_iv)
    key_bt = crypt_key.encode()
    if isinstance(values, dict):
        return {
            k: aes_decrypt(
                value_ori=val, crypt_key=key_bt, iv=iv_bt,
                prefix=prefix, seg_size=seg_size
            ) for k, val in values.items()
        }
    return [
        aes_decrypt(
            value_ori=val, crypt_key=key_bt, iv=iv_bt,
            prefix=prefix, seg_size=seg_size
        ) for val in values
    ]


def aes_decrypt(
        value_ori: str,
        crypt_key: bytes,
        iv: bytes,
        prefix: str = "#",
        block_size: int = 16,
        seg_size=128,
        mode=AES.MODE_CFB) -> str:
    """
    prefix: filter string needs to be decrypted. Empty for non prefix
    block_segments: Python uses 8-bit segments by default for legacy reasons. 
        In order to support languages that encrypt using 128-bit segments, 
        without having to use data with a length divisible by 16, 
        we need to pad and truncate the values.
    cipher need to reset
    """  # noqa:E501
    if not value_ori or not value_ori.startswith(prefix):
        return value_ori
    cipher = AES.new(crypt_key, mode, iv, segment_size=seg_size)
    value_f = value_ori.lstrip(prefix)
    # base64 padding requires length is n*4
    value = base64.b64decode(value_f + '=' * (4 - len(value_f) % 4), b'-_')
    remainder = len(value) % block_size
    padded_value = value + b'\0' * (
            block_size - remainder) if remainder else value
    # Return the decrypted string with the padding removed.
    return cipher.decrypt(padded_value)[:len(value)].decode()


def encrypt(
        values: Union[list, dict],
        crypt_key: str,
        crypt_iv: str,
        prefix: str = "#",
        seg_size=128) -> Union[list, dict]:
    """
    prefix: distinguish between encrypted and unencrypted strings
    segment_size: Python uses 8-bit segments by default for legacy reasons.
        In order to support languages that encrypt using 128-bit segments,
        without having to use data with a length divisible by 16,
        we need to pad and truncate the values.
    """  # noqa:E501
    if not values or type(values) not in (list, dict):
        return values
    iv_bt = binascii.unhexlify(crypt_iv)
    key_bt = crypt_key.encode()
    if isinstance(values, dict):
        return {
            k: aes_encrypt(
                value_ori=val, crypt_key=key_bt, iv=iv_bt,
                prefix=prefix, seg_size=seg_size
            ) for k, val in values.items()
        }
    return [
        aes_encrypt(
            value_ori=val, crypt_key=key_bt, iv=iv_bt,
            prefix=prefix, seg_size=seg_size
        ) for val in values
    ]


def aes_encrypt(
        value_ori: str,
        crypt_key: bytes,
        iv: bytes,
        prefix: str = "#",
        block_size: int = 16,
        seg_size=128,
        mode=AES.MODE_CFB) -> str:
    """
    prefix: distinguish between encrypted and unencrypted strings
    block_size = AES.block_size  # 16
    """  # noqa:E501
    if not value_ori or value_ori.startswith(prefix):
        return value_ori
    cipher = AES.new(crypt_key, mode, iv, segment_size=seg_size)
    value = value_ori.encode()
    remainder = len(value) % block_size
    padded_value = value + b'\0' * (
            block_size - remainder) if remainder else value
    value = cipher.encrypt(padded_value)[:len(value)]
    return prefix + base64.b64encode(value, b'-_').decode()
