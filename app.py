from flask import Flask, jsonify, render_template_string
import socket
import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>DevOps CI/CD Dashboard</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        body {
            background: #0f172a;
            color: #e2e8f0;
            min-height: 100vh;
        }

        .container {
            max-width: 1100px;
            margin: auto;
            padding: 30px 20px;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 15px;
        }

        h1 {
            font-size: 30px;
        }

        .subtitle {
            color: #94a3b8;
            margin-top: 6px;
        }

        .status {
            padding: 10px 18px;
            border-radius: 30px;
            background: #064e3b;
            color: #6ee7b7;
            font-weight: bold;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 18px;
        }

        .card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 15px;
            padding: 22px;
            transition: 0.2s;
        }

        .card:hover {
            transform: translateY(-4px);
            border-color: #64748b;
        }

        .icon {
            font-size: 32px;
            margin-bottom: 12px;
        }

        .card h3 {
            color: #cbd5e1;
            margin-bottom: 8px;
        }

        .value {
            font-size: 20px;
            font-weight: bold;
        }

        .green {
            color: #4ade80;
        }

        .blue {
            color: #60a5fa;
        }

        .yellow {
            color: #facc15;
        }

        .section {
            margin-top: 30px;
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 15px;
            padding: 25px;
        }

        .section h2 {
            margin-bottom: 18px;
        }

        .info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }

        .info-box {
            background: #0f172a;
            padding: 15px;
            border-radius: 10px;
        }

        .label {
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 5px;
        }

        .buttons {
            margin-top: 25px;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        button {
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            background: #2563eb;
            color: white;
        }

        button:hover {
            background: #1d4ed8;
        }

        .response {
            margin-top: 18px;
            background: #020617;
            padding: 15px;
            border-radius: 10px;
            color: #86efac;
            font-family: monospace;
            min-height: 45px;
        }

        footer {
            text-align: center;
            margin-top: 30px;
            color: #64748b;
        }
    </style>
</head>

<body>

<div class="container">

    <header>
        <div>
            <h1>🚀 DevOps CI/CD Dashboard</h1>
            <p class="subtitle">
                Flask Application Monitoring Dashboard
            </p>
        </div>

        <div class="status" id="mainStatus">
            🟢 SYSTEM UP
        </div>
    </header>


    <div class="cards">

        <div class="card">
            <div class="icon">🟢</div>
            <h3>Application</h3>
            <div class="value green" id="appStatus">
                Running
            </div>
        </div>

        <div class="card">
            <div class="icon">🐳</div>
            <h3>Docker</h3>
            <div class="value blue">
                Containerized
            </div>
        </div>

        <div class="card">
            <div class="icon">🔨</div>
            <h3>Jenkins</h3>
            <div class="value yellow">
                CI/CD Enabled
            </div>
        </div>

        <div class="card">
            <div class="icon">☁️</div>
            <h3>AWS EC2</h3>
            <div class="value blue">
                Deployment Server
            </div>
        </div>

    </div>


    <div class="section">

        <h2>📊 Application Information</h2>

        <div class="info">

            <div class="info-box">
                <div class="label">Hostname</div>
                <div id="hostname">Loading...</div>
            </div>

            <div class="info-box">
                <div class="label">Server Time</div>
                <div id="serverTime">Loading...</div>
            </div>

            <div class="info-box">
                <div class="label">Environment</div>
                <div>Production / Docker</div>
            </div>

            <div class="info-box">
                <div class="label">Application</div>
                <div>Flask DevOps App</div>
            </div>

        </div>


        <div class="buttons">

            <button onclick="checkHealth()">
                🔍 Check Health
            </button>

            <button onclick="refreshPage()">
                🔄 Refresh
            </button>

        </div>


        <div class="response" id="response">
            Click "Check Health" to test the application.
        </div>

    </div>


    <footer>
        GitHub → Jenkins → Docker Hub → AWS EC2
        <br>
        DevOps CI/CD Project
    </footer>

</div>


<script>

async function checkHealth() {

    const responseBox = document.getElementById("response");

    responseBox.innerText = "Checking application...";

    try {

        const response = await fetch("/health");

        const data = await response.json();

        responseBox.innerText =
            JSON.stringify(data, null, 2);

        document.getElementById("appStatus").innerText =
            "Running";

        document.getElementById("mainStatus").innerText =
            "🟢 SYSTEM UP";

    } catch (error) {

        responseBox.innerText =
            "Application health check failed.";

        document.getElementById("appStatus").innerText =
            "Down";

        document.getElementById("mainStatus").innerText =
            "🔴 SYSTEM DOWN";
    }
}


async function loadInfo() {

    try {

        const response = await fetch("/api/info");

        const data = await response.json();

        document.getElementById("hostname").innerText =
            data.hostname;

        document.getElementById("serverTime").innerText =
            data.time;

    } catch (error) {

        document.getElementById("hostname").innerText =
            "Unavailable";

        document.getElementById("serverTime").innerText =
            "Unavailable";
    }
}


function refreshPage() {
    location.reload();
}


loadInfo();

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    })


@app.route("/api/info")
def info():

    return jsonify({
        "hostname": socket.gethostname(),
        "time": datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )