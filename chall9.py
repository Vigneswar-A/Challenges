from flask import Flask, request, make_response
from markupsafe import escape

app = Flask(__name__)

@app.route('/xss')
def xss():
    data = request.args.get('data', '')
    if request.headers.get('X-Sandbox-Bypass') == 'Bypass':
        resp = make_response(data)
    else:
        encoded = f"<pre>{escape(data)}</pre>"
        resp = make_response(encoded)
    return resp

@app.route('/')
def index():
    with open(__file__) as f:
        source = escape(f.read())

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Safe HTML Viewer</title>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
      <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
      <style>
        body {{
          font-family: monospace;
          background: #1e1e1e;
          color: #d4d4d4;
          padding: 2rem;
        }}
        pre {{
          white-space: pre-wrap;
          word-wrap: break-word;
          background: #2d2d2d;
          padding: 1rem;
          border-radius: 8px;
          border: 1px solid #444;
        }}
      </style>
    </head>
    <body>
      <h2>Safe HTML Preview</h2>
      <pre><code id="output" class="language-html">Loading...</code></pre>

      <script>
        const params = new URLSearchParams(window.location.search);
        const raw = params.get("html");

        if (raw !== null) {{
          fetch("/xss?data=" + encodeURIComponent(raw), {{
            headers: {{ "X-Sandbox-Bypass": "Bypass" }}
          }})
          .then(res => res.text())
          .then(html => {{
            const el = document.getElementById("output");
            el.textContent = html;
            hljs.highlightElement(el);
          }});
        }} else {{
          document.getElementById("output").textContent = "No ?html= parameter provided.";
        }}
      </script>

      <h2>Source Code (server):</h2>
      <pre><code class="language-python">{source}</code></pre>

      <script>hljs.highlightAll();</script>
    </body>
    </html>
    """
    return html, 200, {'Content-Type': 'text/html'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
