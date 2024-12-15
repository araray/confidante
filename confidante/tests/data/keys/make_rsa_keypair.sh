#!/usr/bin/env bash

openssl genrsa -out rsa_private_key.pem 2048
openssl rsa -in rsa_private_key.pem -pubout > rsa_public_key.pem
