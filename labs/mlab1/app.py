from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('CREATE TABLE users (username TEXT, password TEXT)')
    c.execute("INSERT INTO users VALUES ('admin', 'super_secret_p4ssw0rd')")
    c.execute("INSERT INTO users VALUES ('guest', 'guest')")
    # The flag is stored here
    c.execute('CREATE TABLE flags (flag TEXT)')
    c.execute("INSERT INTO flags VALUES ('flag{sql_1nj3ct10n_m4st3r}')")
    conn.commit()
    return conn

conn = init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # VULNERABLE SQL QUERY
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        
        try:
            c = conn.cursor()
            c.execute(query)
            user = c.fetchone()
            
            if user:
                if user[0] == 'admin':
                    # If they log in as admin, give them the flag
                    c.execute('SELECT flag FROM flags')
                    flag = c.fetchone()[0]
                    return f"<h1>Welcome Admin!</h1><p>Your flag is: {flag}</p>"
                else:
                    return f"<h1>Welcome {user[0]}!</h1>"
            else:
                return "<h1>Invalid credentials</h1>"
        except Exception as e:
            return f"<h1>Database Error: {e}</h1>"
            
    return '''
        <h1>Login to access the secret panel</h1>
        <form method="POST">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
