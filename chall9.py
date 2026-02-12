from flask import *
from html import escape

app = Flask(__name__)

INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecurePad | Minimalist Notes</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f4f7f6;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            width: 100%;
            max-width: 400px;
        }
        h1 { font-size: 1.5rem; color: #333; margin-bottom: 1.5rem; }
        .input-group { display: flex; gap: 10px; margin-bottom: 2rem; }
        input[type="text"] {
            flex: 1;
            padding: 10px 15px;
            border: 1px solid #ddd;
            border-radius: 6px;
            outline: none;
            transition: border-color 0.2s;
        }
        input[type="text"]:focus { border-color: #007bff; }
        button {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }
        button:hover { background: #0056b3; }
        #note-label { font-size: 0.8rem; color: #888; text-transform: uppercase; letter-spacing: 1px; }
        #note {
            margin-top: 10px;
            padding: 15px;
            background: #f9f9f9;
            border-left: 4px solid #007bff;
            min-height: 50px;
            word-wrap: break-word;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>SecurePad</h1>
        <form action="/note" method="POST" class="input-group">
            <input type="text" name="note" placeholder="Write a note..." autocomplete="off">
            <button type="submit">Save</button>
        </form>
        <div id="note-label">Stored Note:</div>
        <div id="note"></div>
    </div>
    <script>
    fetch('/note').then(res => res.text()).then(text => document.getElementById('note').innerHTML = text)
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    response = make_response(INDEX_HTML)
    response.headers['Content-Security-Policy'] = (
        "default-src 'none'; "
        "connect-src 'self'; "
        "style-src 'unsafe-inline'; "
        "script-src 'sha256-8drDHKdo5gz2H/MvZTsh6wRu5Mon7/UmUix8Sje9DgA=';"
    )
    return response

note = 'Welcome to your private vault.'

@app.route('/note', methods=['POST', 'GET'])
def page():
    global note
    if request.method == 'POST':
        note = request.form.get('note')
        return redirect('/')
    if request.headers.get('referer', '').startswith('http://localtest.me:5000/'): 
        return note
    return escape(note)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
