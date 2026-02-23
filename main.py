from flask import Flask, render_template_string, request

app = Flask(__name__)

# ऑल इंडिया हब्स और डेटाबेस (नमूना)
data = {
    "brand": "JOURNEY X",
    "tagline": "India's Largest Taxi Service",
    "states": ["Haryana", "Rajasthan", "Delhi-NCR", "Uttar Pradesh", "Punjab"],
    "hubs": {
        "Haryana": ["Gurugram", "Rohtak", "Faridabad"],
        "Rajasthan": ["Jaipur", "Ajmer", "Jodhpur"],
        "Delhi-NCR": ["New Delhi", "Noida", "Ghaziabad"]
    }
}

# 1. कस्टमर होमपेज (Customer Web Page)
@app.route('/')
def customer_home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <title>{{brand}} - Book Now</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body class="bg-gray-100">
        <nav class="bg-black p-4 text-white text-center">
            <h1 class="text-3xl font-bold italic">{{brand}} <span class="text-yellow-400">X</span></h1>
            <p class="text-xs">{{tagline}}</p>
        </nav>
        
        <div class="p-6 max-w-md mx-auto bg-white shadow-xl rounded-b-xl mt-4">
            <h2 class="text-xl font-bold mb-4 text-center">अपनी यात्रा बुक करें (All India)</h2>
            <div class="space-y-4">
                <input type="text" placeholder="Pick-up Location" class="w-full border p-3 rounded-lg focus:ring-2 focus:ring-yellow-400">
                <input type="text" placeholder="Drop Location" class="w-full border p-3 rounded-lg focus:ring-2 focus:ring-yellow-400">
                
                <select class="w-full border p-3 rounded-lg">
                    <option>Select State (राज्य चुनें)</option>
                    {% for state in states %}
                    <option>{{state}}</option>
                    {% endfor %}
                </select>
                
                <button class="w-full bg-black text-white font-bold py-4 rounded-lg hover:bg-gray-800 transition">
                    चेक किराया (Check Fare)
                </button>
            </div>
            
            <div class="mt-6 text-center">
                <p class="text-gray-500 text-sm">ड्राइवर हैं? <a href="/driver" class="text-blue-600 font-bold underline">यहाँ लॉगिन करें</a></p>
            </div>
        </div>
        
        <footer class="mt-10 text-center text-gray-400 text-sm italic">
            &copy; 2026 Journey X India - सुरक्षित सफ़र, सही किराया।
        </footer>
    </body>
    </html>
    """, **data)

# 2. ड्राइवर पोर्टल (Driver Login Page)
@app.route('/driver')
def driver_portal():
    return "<h1>Driver App Coming Soon...</h1><p>यहाँ ड्राइवर अपना फेस वेरिफिकेशन और कागज़ात अपलोड करेंगे।</p>"

# 3. गुप्त एडमिन पैनल (Hidden Admin Panel)
@app.route('/admin-secret-vikash')
def admin_panel():
    return "<h1>Master Admin Dashboard</h1><p>विकास भाई, यहाँ से आप हरियाणा, गुड़गांव और पूरे भारत का हिसाब देखेंगे।</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
