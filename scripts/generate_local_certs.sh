#!/bin/bash
# Description: This script sets up a local development environment by generating self-signed SSL certificates.

# Generate Self-Signed SSL Certificates for Development
echo "Creating certificate directories..."
mkdir -p ./.certs/live/localhost
mkdir -p ./.certs/archive/localhost
mkdir -p ./.certs/keys

echo "Generating self-signed certificate for localhost..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ./.certs/live/localhost/privkey.pem \
  -out ./.certs/live/localhost/fullchain.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"

echo "Certificate generation complete!"
echo "Private key: ./.certs/live/localhost/privkey.pem"
echo "Certificate: ./.certs/live/localhost/fullchain.pem"
echo ""