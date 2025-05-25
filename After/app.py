from flask import Flask, request, jsonify
import os
import subprocess
import ast
import ipaddress
import shutil

app = Flask(__name__)

# Load password from environment variable
PASSWORD = os.environ.get("APP_PASSWORD")

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    if not name.isalnum():
        return jsonify({"error": "Invalid name"}), 400
    return f"Hello, {name}!"

# Command injection vulnerability
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    try:
        ipaddress.ip_address(ip)  # Validate IP address
    except ValueError:
        return jsonify({"error": "Invalid IP address"}), 400
    
    # Find the full path to the ping command
    ping_path = shutil.which('ping')
    if not ping_path:
        return jsonify({"error": "Ping command not found"}), 500    

    try:
        result = subprocess.check_output([ping_path, '-c', '1', ip], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Ping failed: {e.output}"}), 500

# Insecure use of eval
@app.route('/calculate')
def calculate():
    expression = request.args.get('expr')
    try:
        result = ast.literal_eval(expression)
        return str(result)
    except (ValueError, SyntaxError):
        return jsonify({"error": "Invalid expression"}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
