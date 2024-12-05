from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
from subprocess import run
from os import environ, path

port = environ.get("PORT", 8080)
cert_file = "cert.pem"
key_file = "key.pem"

if not path.exists(cert_file) or not path.exists(key_file):
    print("Certificate or key not found. Generating new ones...")
    run([
        "openssl", "req", "-x509", "-nodes", "-days", "365",
        "-newkey", "rsa:2048",
        "-keyout", key_file,
        "-out", cert_file,
        "-subj", "/C=BR/ST=Sao Paulo/L=Sao Paulo/O=/CN=localhost"
    ], check=True)
    print(f"Generated {cert_file} and {key_file}")

httpd = HTTPServer(('0.0.0.0', int(port)), SimpleHTTPRequestHandler)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=cert_file, keyfile=key_file)

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Serving on https://localhost:{port}")
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer shutting down...")
    httpd.server_close()
