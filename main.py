from flask import Flask, render_template_string, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# --- Supabase Connection ---
SUPABASE_URL = "https://tqpmmqzdlttlgduykbw.supabase.co"
SUPABASE_KEY = "sb_publishable_vEJyQPNgldCwal0Syx2ApA_00e0lcK" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BRAND = "JOURNEY X"

@app.route('/')
def customer_portal():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{brand}} - Premium & Luxury Booking</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body class="bg-slate-50 pb-10">
        <nav class="bg-blue-900 p-5 text-white shadow-2xl sticky top-0 z-50">
            <div class="max-w-md mx-auto flex justify-between items-center">
                <h1 class="text-2xl font-black italic tracking-tighter">{{brand}} X</h1>
                <span class="text-[10px] bg-yellow-500 text-black px-3 py-1 rounded-full font-bold uppercase">Luxury Service</span>
            </div>
        </nav>

        <div class="p-4 max-w-md mx-auto space-y-6">
            <div id="mainCard" class="bg-white p-6 rounded-[2.5rem] shadow-2xl border-t-8 border-blue-600">
                <div class="space-y-4">
                    <input type="text" id="name" placeholder="Full Name" class="w-full border-b-2 p-3 outline-none focus:border-blue-600 font-bold">
                    <input type="tel" id="phone" placeholder="Mobile Number" class="w-full border-b-2 p-3 outline-none focus:border-blue-600 font-bold">
                    
                    <div class="grid grid-cols-2 gap-2">
                        <input type="date" id="pDate" class="w-full border-b-2 p-3 outline-none text-xs font-bold bg-slate-50 rounded-xl">
                        <input type="time" id="pTime" class="w-full border-b-2 p-3 outline-none text-xs font-bold bg-slate-50 rounded-xl">
                    </div>

                    <div class="space-y-3 bg-slate-50 p-4 rounded-3xl border border-slate-200">
                        <input type="text" id="pickup" placeholder="Pickup City" class="w-full bg-transparent border-b p-2 outline-none font-bold">
                        <input type="text" id="drop" placeholder="Drop City" class="w-full bg-transparent border-b p-2 outline-none font-bold">
                        <button onclick="calculateFare()" class="w-full py-2 bg-blue-600 text-white font-bold text-[10px] uppercase rounded-xl shadow-md mt-2">
                            <i class="fa-solid fa-crown mr-1"></i> Calculate Luxury Fare
                        </button>
                    </div>

                    <div id="fareBox" class="hidden bg-slate-900 p-5 rounded-[2rem] text-white text-center border-2 border-yellow-500">
                        <p id="kmText" class="text-yellow-400 font-black text-sm mb-2 italic">Luxury Route Detected</p>
                        
                        <select id="vType" onchange="updatePrice()" class="w-full bg-slate-800 text-white p-3 rounded-xl text-xs font-bold outline-none mb-4 border border-yellow-600">
                            <option value="9">Mini (WagonR/Swift) - ₹9/KM</option>
                            <option value="12">Sedan (Dzire/Etios) - ₹12/KM</option>
                            <option value="15">Ertiga (7 Seater) - ₹15/KM</option>
                            <option value="20">SUV (Innova/Crysta) - ₹20/KM</option>
                            <option value="50">LUXURY (BMW/Audi/Mercedes) - ₹50/KM</option>
                        </select>

                        <div class="py-2 border-t border-slate-700">
                            <p class="text-[9px] text-slate-400 font-bold uppercase mb-1">Premium Estimate</p>
                            <h3 id="totalAmt" class="text-4xl font-black text-yellow-500">₹0</h3>
                        </div>
                    </div>

                    <button onclick="confirmBooking()" id="bookBtn" class="w-full bg-blue-900 text-white font-black py-5 rounded-[2rem] shadow-xl uppercase mt-4 active:scale-95 transition-all">Book Premium Ride</button>
                </div>
            </div>

            <div id="successCard" class="hidden bg-white p-8 rounded-[2.5rem] shadow-2xl text-center border-t-8 border-green-500">
                <div class="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
                    <i class="fa-solid fa-check text-4xl"></i>
                </div>
                <h2 class="text-2xl font-black text-slate-800 mb-2">LUXURY BOOKING SAVED</h2>
                <p class="text-xs text-slate-500 mb-6 font-bold uppercase tracking-widest">Journey X Cloud Database Updated</p>
                <button onclick="location.reload()" class="w-full bg-slate-900 text-white font-bold py-4 rounded-2xl shadow-lg">New Booking</button>
            </div>
        </div>

        <script>
            let travelKM = 0;

            async function calculateFare() {
                const pick = document.getElementById('pickup').value;
                const drop = document.getElementById('drop').value;
                if(!pick || !drop) { alert("Enter both locations!"); return; }

                try {
                    const res1 = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${pick}`);
                    const loc1 = await res1.json();
                    const res2 = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${drop}`);
                    const loc2 = await res2.json();

                    if(loc1.length > 0 && loc2.length > 0) {
                        const routeRes = await fetch(`https://router.project-osrm.org/route/v1/driving/${loc1[0].lon},${loc1[0].lat};${loc2[0].lon},${loc2[0].lat}?overview=false`);
                        const routeData = await routeRes.json();
                        travelKM = Math.ceil(routeData.routes[0].distance / 1000);
                        document.getElementById('kmText').innerText = travelKM + " KM Trip";
                        document.getElementById('fareBox').classList.remove('hidden');
                        updatePrice();
                    }
                } catch(e) { alert("Network Error. Please retry."); }
            }

            function updatePrice() {
                const rate = parseInt(document.getElementById('vType').value);
                let finalKM = travelKM < 250 ? 250 : travelKM;
                document.getElementById('totalAmt').innerText = "₹" + (rate * finalKM);
            }

            async function confirmBooking() {
                const btn = document.getElementById('bookBtn');
                const data = {
                    name: document.getElementById('name').value,
                    phone: document.getElementById('phone').value,
                    pDate: document.getElementById('pDate').value,
                    pTime: document.getElementById('pTime').value,
                    pickup: document.getElementById('pickup').value,
                    drop: document.getElementById('drop').value,
                    kms: travelKM,
                    fare: document.getElementById('totalAmt').innerText,
                    vName: document.getElementById('vType').options[document.getElementById('vType').selectedIndex].text
                };

                if(!data.name || !data.kms) { alert("Calculate Fare First!"); return; }

                btn.innerText = "Processing..."; btn.disabled = true;

                const response = await fetch('/api/book', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });

                if(response.ok) { 
                    document.getElementById('mainCard').classList.add('hidden');
                    document.getElementById('successCard').classList.remove('hidden');
                    window.scrollTo(0,0);
                }
            }
        </script>
    </body>
    </html>
    """, brand=BRAND)

@app.route('/api/book', methods=['POST'])
def book_ride():
    data = request.json
    db_data = {
        "customer_name": data['name'],
        "customer_phone": data['phone'],
        "pickup_location": data['pickup'] + " (" + data['pDate'] + " " + data['pTime'] + ")",
        "drop_location": data['drop'],
        "vehicle_type": data['vName'] + " | Total: " + data['fare']
    }
    supabase.table("bookings").insert(db_data).execute()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
                                  
