from flask import Flask, render_template_string, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# --- Supabase Connection (Directly set for you) ---
SUPABASE_URL = "https://tqpmmqzdlttlgduykbw.supabase.co"
# Aapki Publishable Key jo aapne photo mein dikhayi thi
SUPABASE_KEY = "sb_publishable_vEJyQPNgldCwal0Syx2ApA_00e0lcK" 

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BRAND = "JOURNEY X"
SUPPORT = "+91 88888 88888"

@app.route('/')
def customer_portal():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <title>{{brand}} - Best India Tour & One Way Taxi</title>
        <meta name="description" content="Book affordable One Way Taxi, India Tour Packages, and Luxury Cars like BMW/Audi.">
        <meta name="keywords" content="One Way Taxi, India Tour, Luxury Car, BMW Taxi, Tourist Package, CNG Taxi">

        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body class="bg-slate-50 pb-10">
        <nav class="bg-blue-800 p-5 text-white shadow-2xl sticky top-0 z-50">
            <div class="max-w-md mx-auto flex justify-between items-center">
                <h1 class="text-2xl font-black italic italic tracking-tighter">{{brand}} X</h1>
                <div class="text-right"><p class="text-[10px] font-bold uppercase">Rating: 5.0 ⭐</p></div>
            </div>
        </nav>

        <div class="p-6 max-w-md mx-auto space-y-6">
            <div id="bookingForm" class="bg-white p-6 rounded-[2.5rem] shadow-2xl border-t-8 border-blue-600">
                <h2 class="text-xl font-bold mb-6 text-slate-800"><i class="fa-solid fa-map-location-dot mr-2 text-blue-600"></i>Book Your Ride</h2>
                
                <div class="space-y-4">
                    <input type="text" id="name" placeholder="Full Name" class="w-full border-b-2 p-3 outline-none focus:border-blue-600">
                    <input type="tel" id="phone" placeholder="Mobile Number" class="w-full border-b-2 p-3 outline-none focus:border-blue-600">
                    <input type="text" id="pickup" placeholder="Pick-up City" class="w-full border-b-2 p-3 outline-none focus:border-blue-600">
                    <input type="text" id="drop" placeholder="Drop City (All India)" class="w-full border-b-2 p-3 outline-none focus:border-blue-600">
                    
                    <select id="vType" class="w-full bg-slate-50 p-4 rounded-2xl border-none outline-none font-bold text-slate-700">
                        <option value="Mini-CNG">Mini (CNG) - ₹9/KM</option>
                        <option value="Sedan-Petrol">Sedan (Petrol) - ₹12/KM</option>
                        <option value="SUV-Diesel">SUV (Ertiga) - ₹15/KM</option>
                        <option value="Luxury">Luxury (BMW/Audi)</option>
                    </select>

                    <p class="text-[9px] text-red-500 font-bold italic">* 250KM Min. Running | No Roof Carrier</p>

                    <button onclick="sendBooking()" id="btn" class="w-full bg-blue-600 text-white font-black py-5 rounded-[2rem] shadow-xl uppercase mt-4 active:scale-95 transition-all">Confirm Booking</button>
                </div>
            </div>
        </div>

        <script>
            async function sendBooking() {
                const btn = document.getElementById('btn');
                const data = {
                    name: document.getElementById('name').value,
                    phone: document.getElementById('phone').value,
                    pickup: document.getElementById('pickup').value,
                    drop: document.getElementById('drop').value,
                    vehicle: document.getElementById('vType').value
                };

                if(!data.name || !data.phone || !data.pickup || !data.drop) { 
                    alert("Please fill all details correctly!"); return; 
                }

                btn.innerText = "Processing..."; btn.disabled = true;

                try {
                    const response = await fetch('/api/book', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(data)
                    });

                    if(response.ok) { 
                        alert("✅ Success! Your booking is saved in Journey X Database.");
                        location.reload();
                    } else { alert("❌ Server Error. Please try again."); }
                } catch (e) { alert("❌ Connection Error."); }
                finally { btn.innerText = "Confirm Booking"; btn.disabled = false; }
            }
        </script>
    </body>
    </html>
    """, brand=BRAND)

@app.route('/api/book', methods=['POST'])
def book_ride():
    try:
        data = request.json
        db_data = {
            "customer_name": data['name'],
            "customer_phone": data['phone'],
            "pickup_location": data['pickup'],
            "drop_location": data['drop'],
            "vehicle_type": data['vehicle']
        }
        # Direct insert into Supabase
        supabase.table("bookings").insert(db_data).execute()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
