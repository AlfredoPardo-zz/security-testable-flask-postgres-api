#!/bin/bash
gunicorn --certfile certs/api_cert.pem --keyfile certs/api_key.pem -b 0.0.0.0:5000 app:app