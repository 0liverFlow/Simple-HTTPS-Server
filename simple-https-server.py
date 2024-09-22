#!/usr/bin/python

import http.server
import ssl
import argparse
import os

parser = argparse.ArgumentParser(prog="simple-https-server.py", description="A simple implementation of a HTTPS server")
parser.add_argument("-d", "--directory", help="specify directory to serve files (default is the current directory)", default=os.getcwd())
parser.add_argument("-b", "--bind", help="specify the IP address to which the server will bind (default is 0.0.0.0)", default="0.0.0.0")
parser.add_argument("-p", "--port", type=int, help="specify the http server port to listen on (default is 443)", default=443)
args = parser.parse_args()

# Change the working directory to the directory specified by the user
current_working_directory = os.getcwd()
if (args.directory != current_working_directory):
    os.chdir(args.directory)

# Define the server address and port (Port 443 is the default for HTTPS)
server_address = (args.bind, args.port)

# Create an HTTP server instance
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Creating an SSL context
context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Load the server's certificate and private key
context.load_cert_chain(certfile=f"{current_working_directory}" + "/server.pem", keyfile=f"{current_working_directory}" + "/ca-key.pem")

# Wrap the server socket with SSL
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

# Start the server
print(f"Serving directory {args.directory} on https://{args.bind}:{args.port}")
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nBye!")
    httpd.server_close()
