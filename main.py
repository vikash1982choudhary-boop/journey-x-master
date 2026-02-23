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
        <title>{{brand}} - Free Live Booking</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body class="bg-slate-50 pb-10">
        <nav class="bg-blue-800 p-5 text-white shadow-xl sticky top-0 z-50">
            <h1 class="text-2xl font-black italic tracking-tighter">{{brand}} X</h1>
        </nav>

        <div class="p-4 max-w-md mx-auto space-y-6">
            <div class="bg-white p-6 rounded-[2.5rem] shadow-2xl border-t-8 border-blue-600">
                <h2 class="text-xl font-bold mb-6 text-slate-800 italic underline decoration-blue-200">Trip Fare Calculator</h2>
                
                <div class="space-y-4">
                    <input type="text" id="name" placeholder="Full Name" class="w-full border-b-2 p-3 outline-none focus:border-blue-600">
                    <input type="tel" id="phone" placeholder="Mobile Number" class="w-full border-b-2 p-3 outline-none focus:border-blue-600">
                    
                    <div class="space-y-3">
                        <div class="bg-slate-50 p-3 rounded-xl border border-dashed border-slate-300">
                            <input type="text" id="pickup" placeholder="Pickup (Ex: Delhi)" class="w-full bg-transparent p-2 outline-none text-sm">
                            <hr class="my-2">
                            <input type="text" id="drop" placeholder="Drop (Ex: Agra)" class="w-full bg-transparent p-2 outline-none text-sm">
                        </div>
                        <button onclick="calculateFreeDistance()" class="w-full text-xs font-bold text-blue-600 uppercase py-2 bg-blue-50 rounded-lg">
                            <i class="fa-solid fa-calculator mr-1"></i> Calculate Distance & Fare
                        </button>
                    </div>

                    <div id="resultBox" class="hidden bg-slate-900 p-5 rounded-[2rem] text-white space-y-3 shadow-inner">
                        <div class="flex justify-between items-center px-2">
                            <span class="text-[10px] text-slate-400 font-bold uppercase">Total Distance</span>
                            <span id="kmDisplay" class="text-lg font-black text-blue-400">0 KM</span>
                        </div>
                        
                        <select id="vType" onchange="updateFare()" class="w-full bg-slate-800 p-3 rounded-xl border-none outline-none font-bold text-white text-sm">
                            <option value="9">Mini (CNG) - ₹9/KM</option>
                            <option value="12">Sedan (P/D) - ₹12/KM</option>
                            <option value="15">SUV (Ertiga) - ₹15/KM</option>
                            <option value="20">Innova - ₹20/KM</option>
                        </select>

                        <div class="pt-3 border-t border-slate-700 text-center">
                            <p class="text-[10px] text-slate-400 font-bold uppercase">Estimated Fare</p>
                            <h3 id="totalFare" class="text-3xl font-black text-white">₹0</h3>
                        </div>
                    </div>

                    <button onclick="sendBookingToDB()" id="bookBtn" class="w-full bg-blue-600 text-white font-black py-5 rounded-[2rem] shadow-xl uppercase mt-4 active:scale-95 transition-all">Confirm Booking</button>
                </div>
            </div>
        </div>

        <script>
            let realKms = 0;

            async function calculateFreeDistance() {
                const pick = document.getElementById('pickup').value;
                const drop = document.getElementById('drop').value;

                if(!pick || !drop) { alert("Enter pickup and drop locations!"); return; }

                // Using OpenStreetMap Nominatim for Geocoding & OSRM for Routing (Free)
                try {
                    const res1 = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${pick}`);
                    const loc1 = await res1.json();
                    const res2 = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${drop}`);
                    const loc2 = await res2.json();

                    if(loc1.length > 0 && loc2.length > 0) {
                        const routeRes = await fetch(`https://router.project-osrm.org/route/v1/driving/${loc1[0].lon},${loc1[0].lat};${loc2[0].lon},${loc2[0].lat}?overview=false`);
                        const routeData = await routeRes.json();
                        
                        realKms = Math.ceil(routeData.routes[0].distance / 1000);
                        document.getElementById('kmDisplay').innerText = realKms + " KM";
                        document.getElementById('resultBox').classList.remove('hidden');
                        updateFare();
                    } else { alert("Could not find locations. Try city names."); }
                } catch (e) { alert("Error calculating route. Try again."); }
            }

            function updateFare() {
                const rate = parseInt(document.getElementById('vType').value);
                // Minimum 250 KM rule
                let billableKms = realKms < 250 ? 250 : realKms;
                const fare = rate * billableKms;
                document.getElementById('totalFare').innerText = "₹" + fare;
            }

            async function sendBookingToDB() {
                const btn = document.getElementById('bookBtn');
                const data = {
                    name: document.getElementById('name').value,
                    phone: document.getElementById('phone').value,
                    pickup: document.getElementById('pickup').value,
                    drop: document.getElementById('drop').value,
                    kms: realKms,
                    total: document.getElementById('totalFare').innerText
                };

                if(!data.name || !data.kms) { alert("Calculate fare first!"); return; }

                btn.innerText = "Saving..."; btn.disabled = true;

                const response = await fetch('/api/book', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });

                if(response.ok) { 
                    alert("✅ Booking Confirmed! Data saved in Supabase Cloud.");
                    location.reload();
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
        "pickup_location": data['pickup'],
        "drop_location": data['drop'],
        "vehicle_type": "KM: " + str(data['kms']) + " | Fare: " + data['total']
    }
    supabase.table("bookings").insert(db_data).execute()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
