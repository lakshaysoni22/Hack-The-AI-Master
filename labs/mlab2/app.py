import os
from flask import Flask, request

app = Flask(__name__)

# The secret flag
FLAG = "TECHCORP{cmd_injection_win}"

@app.route('/')
def index():
    return '''
    <h1>Network Diagnostic Tool</h1>
    <p>Enter an IP address to ping:</p>
    <form action="/ping" method="get">
        <input type="text" name="ip" placeholder="8.8.8.8">
        <input type="submit" value="Ping">
    </form>
    '''

@app.route('/ping')
def ping():
    ip = request.args.get('ip', '')
    if not ip:
        return "Please provide an IP address."
    
    # VULNERABLE: Direct command injection
    result = os.popen(f"ping -c 1 {ip}").read()
    
    return f"<pre>{result}</pre><br><a href='/'>Back</a>"

if __name__ == '__main__':
    # Write flag to a file on startup so it can be read via injection
    with open('/flag.txt', 'w') as f:
        f.write(FLAG)
    
    app.run(host='0.0.0.0', port=80)
