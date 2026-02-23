from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <body style="font-family: Arial; background: #000; color: #fff; text-align: center; padding-top: 50px;">
        <h1 style="font-size: 50px;">JOURNEY <span style="color: #FFD700;">X</span></h1>
        <p style="font-style: italic; font-size: 20px; color: #ccc;">India's Largest Taxi Service</p>
        <hr style="width: 50%; margin: 20px auto; border-color: #333;">
        <div style="background: #111; display: inline-block; padding: 20px; border-radius: 10px;">
            <p>Admin Control: 🟢 Online</p>
            <p>City Hubs: Gurugram, Jaipur, Delhi-NCR</p>
            <p>Commission Logic: 8% Wallet Lock Enabled</p>
        </div>
    </body>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
  
