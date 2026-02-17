import subprocess
import atexit
import textwrap
import requests
from flask import Flask, request
import secrets

access_token = secrets.token_hex(16)
app = Flask(__name__)

PUBLIC_COMMANDS = ["greet"]
HASH = "00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff"

# ================= PHP FILES =================

ADMIN_PHP = f"""
<?php
session_start();
$raw = file_get_contents("php://input");
$data = json_decode($raw, true);

if (!isset($_REQUEST['token']) || $_REQUEST['token'] !== "{access_token}") {{
    echo "<h2>Invalid token</h2>";
    exit;
}}

if ($_REQUEST['cmd'] == 'greet') {{
    echo "<h1>Hello, World!</h1>";
    return;
}}

if (!isset($_SESSION["role"]) || $_SESSION["role"] != 'admin'){{
    header("location: /login.php");
}}

if ($_REQUEST['cmd'] == 'flag' && $data['cmd'] == 'flag') {{
    echo "flag{{4ct10n_f14g_c0mp13t3d_5uc3ssfu11y}}";
}}
else {{
    echo "<h1>404 Not Found</h1>";
}}
?>
"""

LOGIN_PHP = f"""
<?php
session_start();
$CORRECT_HASH = "{HASH}";

if (!isset($_REQUEST['token']) || $_REQUEST['token'] !== "{access_token}") {{
    echo "<h2>Invalid token</h2>";
    exit;
}}

if ($_SERVER["REQUEST_METHOD"] === "POST") {{
    $user = $_POST["username"] ?? "";
    $pass = $_POST["password"] ?? "";
    $hash = hash("sha256", $pass);

    if ($user === "admin" && $hash === $CORRECT_HASH) {{
        $_SESSION["role"] = "admin";
        echo "<h2>Logged in as admin</h2>";
        exit;
    }} else {{
        echo "<h2>Invalid credentials</h2>";    
        exit;
    }}
}}
?>

<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
<h2>Admin Login</h2>
<form method="POST">
    <input name="username" placeholder="username"><br><br>
    <input name="password" type="password" placeholder="password"><br><br>
    <button type="submit">Login</button>
</form>
</body>
</html>
"""

with open("admin.php", "w") as f:
    f.write(textwrap.dedent(ADMIN_PHP))

with open("login.php", "w") as f:
    f.write(textwrap.dedent(LOGIN_PHP))

# ================= START PHP =================

php_proc = subprocess.Popen(["php", "-S", "127.0.0.1:3000"])
atexit.register(php_proc.terminate)

# ================= UI =================

@app.route("/")
def ui():
    return """<!DOCTYPE html>
<html>
<head>
<title>WAF Proxy Challenge</title>
<style>
body {
  font-family: system-ui, sans-serif;
  background: #0f1220;
  color: #e5e7eb;
}

.box {
  background: #171a2b;
  border: 1px solid #2a2f45;
  border-radius: 8px;
  padding: 20px;
  width: 520px;
}

input, button {
  background: #0f1220;
  color: #e5e7eb;
  border: 1px solid #2a2f45;
  border-radius: 6px;
  padding: 6px 10px;
}

button {
  cursor: pointer;
}

button:hover {
  background: #1f2340;
}
</style>
</head>
<body>

<h1>WAF Proxy</h1>

<div class="box">
<form id="f">
Proxy URL:<br><br>
<input id="url" size="60" value="/admin.php?cmd=greet"><br><br>
<button>Open</button>
</form>
</div>

<script>
document.getElementById("f").onsubmit = e => {
  e.preventDefault();
  const url = document.getElementById("url").value;
  // navigate instead of fetch
  window.location.href = url;
};
</script>

</body>
</html>
"""


# ================= PROXY =================

@app.route("/<path>", methods=["GET", "POST"])
def proxy(path):
    if request.remote_addr != "133.7.13.37" and request.args.get("cmd") and request.args.get("cmd") not in PUBLIC_COMMANDS:
        return "Access Denied", 400

    json = request.get_json(silent=True)
    if json and "flag" in repr(json):
        return "Don't even think about it!", 400

    if request.method == "GET":
        resp = requests.get(
            request.url.replace(":5000", ":3000"),
            allow_redirects=False,
            params={"token": access_token}
        )
    else:
        resp = requests.post(
            request.url.replace(":5000", ":3000"),
            json=json,
            params={"token": access_token},
            allow_redirects=False
        )

    if resp.headers.get("Location"):
        return (
            resp.content,
            resp.status_code,
            {"Location": resp.headers.get("Location")}
        )
    else:
        return (
            resp.content,
            resp.status_code
        )


app.run("0.0.0.0", port=5000)
