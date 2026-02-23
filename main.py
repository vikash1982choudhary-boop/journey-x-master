from flask import Flask, render_template_string, request, jsonify
from supabase import create_client, Client

app = Flask(__name__)

# --- Supabase Connection Setup ---
SUPABASE_URL = "https://tqpmmqzdlttlgduykbw.supabase.co"
SUPABASE_KEY = "sb_publishable_vEJyQPNgldCwal0Syx2ApA__00e0lcK" #
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BRAND = "JOURNEY X"

@app.route('/')
def index():
    # Aapka pura design aur logic yahan HTML ke roop mein hai
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JourneyX | Premium Booking</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            .selected-tab { border: 2px solid white !important; border-radius: 9999px; background: rgba(255, 255, 255, 0.15); }
        </style>
    </head>
    <body class="bg-gray-100 flex justify-center">
        <div class="w-full max-w-md bg-white min-h-screen shadow-2xl relative pb-10">
            <div class="bg-[#1e3a8a] p-6 rounded-b-[40px] text-white shadow-xl">
                <div class="flex justify-between items-center mb-6">
                    <h1 class="text-3xl font-black italic tracking-tighter">{{brand}}</h1>
                    <div id="displayRating" class="bg-yellow-400 text-blue-900 px-3 py-1 rounded-full font-black text-sm shadow-lg">5.0 ⭐</div>
                </div>
                
                <div class="space-y-4">
                    <input id="pickupLoc" type="text" placeholder="Pickup Address" class="w-full p-4 rounded-2xl bg-white/10 border border-white/20 text-white outline-none placeholder-blue-200">
                    <input id="dropLoc" type="text" placeholder="Drop Address" class="w-full p-4 rounded-2xl bg-white/10 border border-white/20 text-white outline-none placeholder-blue-200">
                    <input id="distance" type="number" oninput="calculateFare()" placeholder="Total KM" class="w-full p-4 rounded-2xl bg-white text-blue-900 font-black text-center outline-none">
                </div>
            </div>

            <div class="p-6">
                <div class="space-y-4 mb-6">
                    <select id="carSelect" onchange="calculateFare()" class="w-full p-4 border-2 border-gray-100 rounded-2xl font-bold bg-gray-50 outline-none">
                        <option value="Mini">Mini - ₹9/KM</option>
                        <option value="Sedan">Sedan - ₹12/KM</option>
                        <option value="Ertiga">Ertiga - ₹15/KM</option>
                        <option value="Innova">Innova Crysta - ₹20/KM</option>
                        <option value="Luxury">Luxury (BMW/Audi) - ₹65/KM</option>
                    </select>
                    <input id="uName" type="text" placeholder="Full Name" class="w-full p-4 border-2 border-gray-100 rounded-2xl outline-none">
                    <input id="uPhone" type="tel" placeholder="Phone Number" class="w-full p-4 border-2 border-gray-100 rounded-2xl outline-none">
                </div>

                <div id="totalBox" class="hidden bg-blue-50 border-2 border-blue-100 p-6 rounded-3xl mb-6 text-center">
                    <p class="text-blue-800 text-xs font-bold uppercase">Estimated Total</p>
                    <h2 id="fareAmount" class="text-5xl font-black text-blue-900">₹0</h2>
                </div>

                <button onclick="submitBooking()" class="w-full bg-[#1e3a8a] text-white py-5 rounded-2xl font-black text-lg shadow-xl uppercase active:scale-95 transition-all">Book Now</button>
            </div>
        </div>

        <script>
            let userRating = 5.0; // Isse hum filter manage karenge
            const rates = { "Mini": 9, "Sedan": 12, "Ertiga": 15, "Innova": 20, "Luxury": 65 };

            window.onload = () => {
                const carSelect = document.getElementById('carSelect');
                if (userRating < 4.5) {
                    document.getElementById('displayRating').classList.replace('bg-yellow-400', 'bg-red-500');
                    for (let i=0; i<carSelect.options.length; i++) {
                        if (carSelect.options[i].value === "Luxury" || carSelect.options[i].value === "Innova") {
                            carSelect.options[i].style.display = "none";
                        }
                    }
                }
            };

            function calculateFare() {
                const dist = document.getElementById('distance').value;
                const car = document.getElementById('carSelect').value;
                if(dist > 0) {
                    const total = dist * rates[car];
                    document.getElementById('fareAmount').innerText = "₹" + Math.round(total);
                    document.getElementById('totalBox').classList.remove('hidden');
                }
            }

            async function submitBooking() {
                const bookingData = {
                    name: document.getElementById('uName').value,
                    phone: document.getElementById('uPhone').value,
                    pickup: document.getElementById('pickupLoc').value,
                    drop: document.getElementById('dropLoc').value,
                    car: document.getElementById('carSelect').value,
                    fare: document.getElementById('fareAmount').innerText
                };

                const response = await fetch('/api/book', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(bookingData)
                });

                if(response.ok) {
                    alert("✅ Booking Confirmed!");
                    location.reload();
                } else {
                    alert("❌ Error saving booking!");
                }
            }
        </script>
    </body>
    </html>
    """, brand=BRAND)

@app.route('/api/book', methods=['POST'])
def book_ride():
    try:
        data = request.json
        # Supabase Table Mapping
        db_data = {
            "customer_name": data['name'],
            "customer_phone": data['phone'],
            "pickup_location": data['pickup'],
            "drop_location": data['drop'],
            "vehicle_type": data['car'],
            "luggage_details": "Fare: " + data['fare'],
            "status": "pending"
        }
        supabase.table("bookings").insert(db_data).execute()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
