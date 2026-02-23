from flask import Flask, render_template_string

app = Flask(__name__)

BRAND = "JOURNEY X"
SUPPORT = "+91 88888 88888"

@app.route('/')
def customer_portal():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{brand}} - सुरक्षित यात्रा</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body class="bg-slate-50 pb-10">
        <nav class="bg-blue-800 p-4 text-white flex justify-between items-center shadow-lg sticky top-0 z-50">
            <h1 class="text-2xl font-black italic italic">{{brand}} X</h1>
            <a href="tel:{{phone}}" class="text-xs bg-white/20 px-3 py-1 rounded-full font-bold">Help Line</a>
        </nav>

        <div id="step1" class="p-6 max-w-md mx-auto bg-white shadow-2xl mt-6 rounded-[2rem] border-t-8 border-blue-600">
            <h2 class="text-xl font-bold mb-6 text-blue-900"><i class="fa-solid fa-user-circle mr-2"></i> कस्टमर लॉगिन</h2>
            <div class="space-y-4">
                <input type="text" id="cName" placeholder="आपका पूरा नाम" class="w-full bg-slate-50 border-2 p-4 rounded-2xl outline-none focus:border-blue-600">
                <input type="tel" id="cPhone" placeholder="मोबाइल नंबर" class="w-full bg-slate-50 border-2 p-4 rounded-2xl outline-none focus:border-blue-600">
                <button onclick="checkLogin()" class="w-full bg-blue-600 text-white font-black py-4 rounded-2xl shadow-xl">Next</button>
            </div>
        </div>

        <div id="step2" class="hidden p-6 max-w-md mx-auto bg-white shadow-2xl mt-6 rounded-[2rem] border-t-8 border-red-500">
            <h2 class="text-lg font-bold text-red-600 mb-4 italic">⚠️ ज़रूरी शर्तें (Terms)</h2>
            <div class="bg-red-50 p-4 rounded-2xl text-xs space-y-3 mb-6 border border-red-100 font-bold text-slate-700">
                <p>✅ 250 KM प्रति दिन का किराया अनिवार्य है।</p>
                <p>✅ टोल, पार्किंग और स्टेट टैक्स (Hot Status) एक्स्ट्रा होगा।</p>
                <p>✅ नाइट चार्ज और भत्ता गाड़ी के अनुसार लागू होगा।</p>
            </div>
            <div class="flex gap-4">
                <button onclick="location.reload()" class="flex-1 bg-slate-100 py-4 rounded-2xl font-bold">Reject</button>
                <button onclick="goToBooking()" class="flex-1 bg-red-600 text-white font-bold py-4 rounded-2xl shadow-lg">Accept</button>
            </div>
        </div>

        <div id="step3" class="hidden p-6 max-w-md mx-auto bg-white shadow-2xl mt-6 rounded-[2rem] border-t-8 border-blue-400">
            <h2 class="text-lg font-bold mb-4 text-center">गाड़ी चुनें</h2>
            <div class="grid grid-cols-2 gap-3 mb-6">
                <div onclick="set('Mini', 9, 200, 250)" class="card border-2 p-3 rounded-2xl text-center cursor-pointer bg-slate-50">
                    <p class="font-bold">Mini</p><p class="text-blue-600 text-xs">₹9/KM</p>
                </div>
                <div onclick="set('Sedan', 12, 200, 250)" class="card border-2 p-3 rounded-2xl text-center cursor-pointer bg-slate-50">
                    <p class="font-bold">Sedan</p><p class="text-blue-600 text-xs">₹12/KM</p>
                </div>
                <div onclick="set('SUV', 15, 250, 300)" class="card border-2 p-3 rounded-2xl text-center cursor-pointer bg-slate-50">
                    <p class="font-bold">Ertiga</p><p class="text-blue-600 text-xs">₹15/KM</p>
                </div>
                <div onclick="set('Innova', 20, 300, 400)" class="card border-2 p-3 rounded-2xl text-center cursor-pointer bg-slate-50">
                    <p class="font-bold">Innova</p><p class="text-blue-600 text-xs">₹20/KM</p>
                </div>
                <div onclick="set('Luxury', 'Driver Set', 'Driver Set', 'Driver Set')" class="col-span-2 border-2 border-yellow-500 bg-yellow-50 p-3 rounded-2xl text-center shadow-md">
                    <p class="font-black text-yellow-800 italic uppercase">Luxury Segment ✨</p>
                    <p class="text-[10px] text-yellow-700">Dynamic Driver Rates</p>
                </div>
            </div>

            <div id="info" class="hidden bg-slate-900 p-4 rounded-2xl text-white mb-6">
                <p id="t" class="text-xs font-bold text-blue-400 uppercase mb-2"></p>
                <div class="flex justify-between text-[10px] font-bold">
                    <span>नाइट: <span id="n"></span></span>
                    <span>भत्ता: <span id="a"></span></span>
                </div>
            </div>

            <div class="space-y-4">
                <input type="text" placeholder="Pick-up location" class="w-full border-b-2 p-2 outline-none">
                <input type="text" placeholder="Drop location" class="w-full border-b-2 p-2 outline-none">
                <button onclick="finish()" class="w-full bg-blue-800 text-white font-black py-4 rounded-2xl mt-4">Confirm Booking</button>
            </div>
        </div>

        <script>
            function checkLogin() { if(document.getElementById('cName').value) { document.getElementById('step1').classList.add('hidden'); document.getElementById('step2').classList.remove('hidden'); } }
            function goToBooking() { document.getElementById('step2').classList.add('hidden'); document.getElementById('step3').classList.remove('hidden'); }
            function set(car, rate, n, a) {
                document.getElementById('info').classList.remove('hidden');
                document.getElementById('t').innerText = car + " के नियम:";
                document.getElementById('n').innerText = (typeof n === 'number') ? "₹" + n : n;
                document.getElementById('a').innerText = (typeof a === 'number') ? "₹" + a : a;
            }
            function finish() { alert("बुकिंग कन्फर्म! हम आपसे जल्द संपर्क करेंगे।"); }
        </script>
    </body>
    </html>
    """, brand=BRAND, phone=SUPPORT)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
