# kms_encrypter

Encrypt/Decrypt using AWS KMS

## Install

    $ pip install kms_encrypter

## Usage

    from kms_encrypter import KMSEncrypter
    encrypter = KMSEncrypter('YOUR_AWS_KMS_ID')
    msg = 'hello , world'
    encrypted_msg = encrypter.encrypt(msg) 
    assert encrypter.decrypt(encrypted_msg) == msg 












