from flask import Flask, render_template_string, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# --- Supabase Connection (Fixed) ---
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
        <title>{{brand}} - Advance Booking & Fare Calculator</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body class="bg-slate-50 pb-10">
        <nav class="bg-blue-800 p-5 text-white shadow-xl sticky top-0 z-50">
            <h1 class="text-2xl font-black italic tracking-tighter">{{brand}} X</h1>
        </nav>

        <div class="p-4 max-w-md mx-auto space-y-6">
            <div class="bg-white p-6 rounded-[2.5rem] shadow-2xl border-t-8 border-blue-600">
                <h2 class="text-xl font-bold mb-6 text-slate-800 italic underline decoration-blue-200 text-center">Plan Your Journey</h2>
                
                <div class="space-y-4">
                    <input type="text" id="name" placeholder="Enter Full Name" class="w-full border-b-2 p-3 outline-none focus:border-blue-600">
                    <input type="tel" id="phone" placeholder="Mobile Number" class="w-full border-b-2 p-3 outline-none focus:border-blue-600">
                    
                    <div class="grid grid-cols-2 gap-2">
                        <input type="date" id="pDate" class="w-full border-b-2 p-3 outline-none text-xs">
                        <input type="time" id="pTime" class="w-full border-b-2 p-3 outline-none text-xs">
                    </div>

                    <div class="space-y-3">
                        <input type="text" id="pickup" placeholder="Pickup City (e.g. Jaipur)" class="w-full border-b-2 p-3 outline-none">
                        <input type="text" id="drop" placeholder="Drop City (e.g. Chandigarh)" class="w-full border-b-2 p-3 outline-none">
                        <button onclick="calculateFreeDistance()" class="w-full py-2 bg-blue-50 text-blue-600 font-bold text-[10px] uppercase rounded-lg border border-blue-200">
                            Calculate Fare & Distance
                        </button>
                    </div>

                    <div id="fareBox" class="hidden bg-slate-900 p-5 rounded-[2rem] text-white space-y-4">
                        <div class="flex justify-between items-center px-2">
                            <span id="kmDisplay" class="text-blue-400 font-black">0 KM</span>
                            <select id="vType" onchange="updateFare()" class="bg-slate-800 p-2 rounded-lg text-[10px] font-bold outline-none border-none">
                                <option value="9">Mini - ₹9/KM</option>
                                <option value="12">Sedan - ₹12/KM</option>
                                <option value="15">SUV - ₹15/KM</option>
                                <option value="20">Innova - ₹20/KM</option>
                            </select>
                        </div>
                        <div class="text-center">
                            <p class="text-[9px] text-slate-400 font-bold uppercase mb-1">Total Estimated Fare</p>
                            <h3 id="totalAmt" class="text-3xl font-black text-white">₹0</h3>
                            <p class="text-[8px] text-slate-500 mt-1">*Excluding Toll, State Tax & Parking</p>
                        </div>
                    </div>

                    <button onclick="confirmAdvanceBooking()" id="bookBtn" class="w-full bg-blue-800 text-white font-black py-5 rounded-[2rem] shadow-xl uppercase mt-4 active:scale-95 transition-all">Confirm Advance Booking</button>
                </div>
            </div>
        </div>

        <script>
            let travelKms = 0;

            async function calculateFreeDistance() {
                const pick = document.getElementById('pickup').value;
                const drop = document.getElementById('drop').value;

                if(!pick || !drop) { alert("Please enter Pickup and Drop cities!"); return; }

                try {
                    const res1 = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${pick}`);
                    const loc1 = await res1.json();
                    const res2 = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${drop}`);
                    const loc2 = await res2.json();

                    if(loc1.length > 0 && loc2.length > 0) {
                        const routeRes = await fetch(`https://router.project-osrm.org/route/v1/driving/${loc1[0].lon},${loc1[0].lat};${loc2[0].lon},${loc2[0].lat}?overview=false`);
                        const routeData = await routeRes.json();
                        
                        travelKms = Math.ceil(routeData.routes[0].distance / 1000);
                        document.getElementById('kmDisplay').innerText = travelKms + " KM";
                        document.getElementById('fareBox').classList.remove('hidden');
                        updateFare();
                    } else { alert("Location not found. Please type clear city names."); }
                } catch (e) { alert("Network Error. Try again."); }
            }

            function updateFare() {
                const rate = parseInt(document.getElementById('vType').value);
                let billableKms = travelKms < 250 ? 250 : travelKms;
                const total = rate * billableKms;
                document.getElementById('totalAmt').innerText = "₹" + total;
            }

            async function confirmAdvanceBooking() {
                const btn = document.getElementById('bookBtn');
                const data = {
                    name: document.getElementById('name').value,
                    phone: document.getElementById('phone').value,
                    pDate: document.getElementById('pDate').value,
                    pTime: document.getElementById('pTime').value,
                    pickup: document.getElementById('pickup').value,
                    drop: document.getElementById('drop').value,
                    kms: travelKms,
                    fare: document.getElementById('totalAmt').innerText
                };

                if(!data.name || !data.phone || !data.kms) { 
                    alert("Please calculate Fare and fill all details first!"); 
                    return; 
                }

                btn.innerText = "Processing..."; btn.disabled = true;

                const response = await fetch('/api/book', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });

                if(response.ok) { 
                    // Yahan aapka professional message
                    alert("✅ ADVANCE BOOKING CONFIRMED!\\n\\nRoute: " + data.pickup + " to " + data.drop + "\\nDistance: " + data.kms + " KM\\nEstimated Total: " + data.fare + "\\n\\nOur support team will contact you regarding driver assignment.");
                    location.reload();
                } else { alert("Error saving booking. Try again."); btn.innerText = "Confirm Advance Booking"; btn.disabled = false; }
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
        "vehicle_type": "KM: " + str(data['kms']) + " | Total: " + data['fare']
    }
    supabase.table("bookings").insert(db_data).execute()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
