from flask import Flask, render_template_string

app = Flask(__name__)

# ब्रांड डेटा
data = {
    "brand": "JOURNEY X",
    "tagline": "India's Largest Taxi Service"
}

@app.route('/')
def customer_home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <title>{{brand}} - सुरक्षित यात्रा</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body class="bg-blue-50">
        <nav class="bg-blue-800 p-4 text-white flex justify-between items-center shadow-lg">
            <h1 class="text-2xl font-bold italic tracking-wider">{{brand}} <span class="text-blue-200">X</span></h1>
            <a href="/driver" class="text-xs border border-blue-200 p-1.5 rounded-lg text-blue-100 hover:bg-blue-700">ड्राइवर पोर्टल</a>
        </nav>

        <div id="regForm" class="p-6 max-w-md mx-auto bg-white shadow-2xl mt-6 rounded-2xl border-t-4 border-blue-600">
            <h2 class="text-xl font-bold text-blue-900 mb-5">कस्टमर रजिस्ट्रेशन</h2>
            <div class="space-y-4">
                <div class="relative">
                    <input type="text" placeholder="आपका पूरा नाम" class="w-full border-2 border-blue-100 p-3 rounded-xl focus:border-blue-500 outline-none transition-all">
                </div>
                <div class="relative">
                    <input type="tel" placeholder="मोबाइल नंबर (+91)" class="w-full border-2 border-blue-100 p-3 rounded-xl focus:border-blue-500 outline-none transition-all">
                </div>
                <button onclick="showPackages()" class="w-full bg-blue-600 text-white font-bold py-4 rounded-xl shadow-lg hover:bg-blue-700 active:scale-95 transition-all">
                    आगे बढ़ें (Next)
                </button>
            </div>
        </div>

        <div id="packageSection" class="hidden p-6 max-w-md mx-auto bg-white shadow-2xl mt-6 rounded-2xl border-t-4 border-blue-400">
            <h2 class="text-lg font-bold text-blue-900 mb-4 text-center">अपनी यात्रा का प्रकार चुनें</h2>
            <div class="grid grid-cols-2 gap-3">
                <div class="border-2 border-blue-500 bg-blue-50 p-4 rounded-xl text-center cursor-pointer shadow-sm">
                    <p class="font-bold text-blue-800">Local</p>
                    <p class="text-[10px] text-blue-600 uppercase tracking-tighter">शहर के अंदर</p>
                </div>
                <div class="border-2 border-blue-100 p-4 rounded-xl text-center cursor-pointer hover:border-blue-400 transition-colors">
                    <p class="font-bold text-gray-700">Outstation</p>
                    <p class="text-[10px] text-gray-400 uppercase tracking-tighter font-semibold">शहर से बाहर</p>
                </div>
                <div class="border-2 border-blue-100 p-4 rounded-xl text-center cursor-pointer hover:border-blue-400 transition-colors">
                    <p class="font-bold text-gray-700">One Way</p>
                    <p class="text-[10px] text-gray-400 uppercase tracking-tighter font-semibold">सिर्फ एक तरफ</p>
                </div>
                <div class="border-2 border-blue-100 p-4 rounded-xl text-center cursor-pointer hover:border-blue-400 transition-colors">
                    <p class="font-bold text-gray-700">Round Trip</p>
                    <p class="text-[10px] text-gray-400 uppercase tracking-tighter font-semibold">आना-जाना</p>
                </div>
            </div>

            <div class="mt-8 space-y-5">
                <div class="border-l-4 border-blue-500 pl-3">
                    <p class="text-[10px] font-bold text-blue-500 uppercase">Pick-up Location</p>
                    <input type="text" placeholder="कहाँ से?" class="w-full p-2 border-b border-gray-200 outline-none focus:border-blue-500">
                </div>
                <div class="border-l-4 border-red-400 pl-3">
                    <p class="text-[10px] font-bold text-red-400 uppercase">Drop Location</p>
                    <input type="text" placeholder="कहाँ तक?" class="w-full p-2 border-b border-gray-200 outline-none focus:border-blue-500">
                </div>
                <button class="w-full bg-blue-800 text-white font-bold py-4 rounded-xl mt-6 shadow-xl hover:bg-blue-900 transition-all">
                    अभी बुकिंग कन्फर्म करें
                </button>
            </div>
        </div>

        <footer class="mt-12 text-center text-blue-300 text-xs pb-10">
            &copy; 2026 Journey X India - आपकी सुरक्षा, हमारी ज़िम्मेदारी।
        </footer>

        <script>
            function showPackages() {
                document.getElementById('regForm').classList.add('opacity-50');
                document.getElementById('packageSection').classList.remove('hidden');
                window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
            }
        </script>
    </body>
    </html>
    """, **data)

@app.route('/driver')
def driver_portal():
    return "<h1>Driver Registration - Coming Soon</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
