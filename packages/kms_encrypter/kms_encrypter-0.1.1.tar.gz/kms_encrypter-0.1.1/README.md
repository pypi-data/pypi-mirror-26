# kms_encrypter

Encrypt using AWS KMS

## Install

    $ cd kms_encrypter
    $ python3.6 -m venv venv
    $ pip install -r requirements.txt

## Getting Started


Create AWS KMS Key at <a href="https://aws.amazon.com/jp/iam/" target="_blank">this</a>.

Next, replace AWS_KMS_ID  with created it at main.py.

    AWS_KMS_ID = '<AWS_KMS_ID>'

That's all. You can get encrypted text by run command and enter question.

    $ cd kms_encrypter
    $ source venv/bin/activate
    $ python main.py
    
    Type text to encrypt 
    > abc
    
    === ENCRYPTED TEXT ===
    'ENCRYPTED_TEXT'
    === DECRYPTED TEXT === 
    'abc'













