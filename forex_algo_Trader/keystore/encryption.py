####################################################################################################################################################################
##-- Script Description : Encryption File for project connections
##-- Sources            : 
##-- Created            : Sep 2020 
##-- Author             : Jason TANG
####################################################################################################################################################################
##-- Amendment History  : 
####################################################################################################################################################################


################################################################################################################
## Python Libraries
################################################################################################################
## Common Libraries
import os, sys, base64

# Cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


################################################################################################################
## Encryption Logic Initial
################################################################################################################
key_generator = b"9IJN8uhb3EDC4rfv"
salt = os.urandom(16)

kdf = PBKDF2HMAC(
    algorithm = hashes.SHA256(),
    length=32,
    salt=salt,
    iterations = 100000,
    backend = default_backend()
)

masterkey = base64.urlsafe_b64decode(kdf.derive(key_generator))
f=Fernet(masterkey)

with open(os.path.join(os.getcwd(),"key.key"), "w+") as keyfile:
    key = masterkey.decode()
    keyfile.write(key)
    keyfile.close()

with open(os.path.join(os.getcwd(),"acct_demo.encrypted"), "w+") as tokenfile:
    token = f.encrypt(b"101-004-16285502-001").decode()
    tokenfile.write(token)
    tokenfile.close()

with open(os.path.join(os.getcwd(),"token_demo.encrypted"), "w+") as tokenfile:
    token = f.encrypt(b"ab76634af1721b2f72a277a400a63ef5-1d702d9778da8a0bda76a049a31aea6e").decode()
    tokenfile.write(token)
    tokenfile.close()


################################################################################################################
## Encryption Logic - New Tokens
################################################################################################################