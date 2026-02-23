from flask import Flask, render_template_string

app = Flask(__name__)

BRAND = "JOURNEY X"
SUPPORT = "+91 88888 88888"

@app.route('/')
def customer_portal():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <title>{{brand}} - No.1 India Tour, One-Way Taxi & Luxury Car Rental</title>
        <meta name="description" content="Book affordable One Way Taxi, India Tour Packages, and Luxury Cars like BMW/Audi. Best Tourist Cab service with Luggage verified vehicles.">
        <meta name="keywords" content="One Way Taxi, India Tour, Luxury Car Rental, BMW Taxi, Tourist Package, Round Trip Cab, Best Taxi Service India, Outstation Taxi, CNG Taxi, Petrol Cab">
        
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            .car-card.active { border-color: #1e40af; background-color: #eff6ff; transform: scale(1.02); }
            body { font-family: 'Inter', sans-serif; }
        </style>
    </head>
    <body class="bg-slate-50 pb-10">

        <nav class="bg-blue-800 p-5 text-white shadow-2xl sticky top-0 z-50">
            <div class="max-w-md mx-auto flex justify-between items-center">
                <div>
                    <h1 class="text-2xl font-black italic tracking-tighter">{{brand}} <span class="text-blue-300">X</span></h1>
                    <p class="text-[8px] uppercase tracking-[3px] text-blue-200 font-bold">Premium Tourism Network</p>
                </div>
                <div class="text-right">
                    <p class="text-[10px] font-black">Initial Rating</p>
                    <div class="text-yellow-400 text-xs">
                        <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>
                    </div>
                </div>
            </div>
        </nav>

        <div class="p-4 max-w-md mx-auto space-y-6">
            
            <div id="loginStep" class="bg-white p-6 rounded-[2rem] shadow-xl border-t-8 border-blue-600">
                <h2 class="text-lg font-bold mb-4"><i class="fa-solid fa-circle-user text-blue-600 mr-2"></i>Customer Login</h2>
                <div class="space-y-4">
                    <input type="text" id="custName" placeholder="Enter Full Name" class="w-full bg-slate-50 border-2 p-4 rounded-2xl outline-none focus:border-blue-600">
                    <input type="tel" id="custPhone" placeholder="Enter Mobile Number" class="w-full bg-slate-50 border-2 p-4 rounded-2xl outline-none focus:border-blue-600">
                    <button onclick="nextStep('termsStep')" class="w-full bg-blue-600 text-white font-black py-4 rounded-2xl shadow-lg">Proceed to Terms</button>
                </div>
            </div>

            <div id="termsStep" class="hidden bg-white p-6 rounded-[2rem] shadow-xl border-t-8 border-red-500">
                <h2 class="text-lg font-bold text-red-600 mb-4 italic"><i class="fa-solid fa-file-shield mr-2"></i>Security & Terms</h2>
                <div class="bg-red-50 p-4 rounded-2xl text-[11px] space-y-3 mb-6 border border-red-100 font-bold text-slate-700">
                    <p>✅ Min. Running: 250 KM/Day mandatory.</p>
                    <p>✅ Toll, Parking & State Tax (Hot Status): Extra.</p>
                    <p>✅ Night Charge & Driver Allowance: Based on vehicle selection.</p>
                    <p>✅ No Roof Carrier: Luggage must fit in boot space.</p>
                </div>
                <div class="flex gap-4">
                    <button onclick="location.reload()" class="flex-1 bg-slate-100 py-4 rounded-2xl font-bold text-slate-500">Reject</button>
                    <button onclick="nextStep('bookingStep')" class="flex-1 bg-red-600 text-white font-bold py-4 rounded-2xl shadow-lg">Accept</button>
                </div>
            </div>

            <div id="bookingStep" class="hidden space-y-4">
                
                <div class="bg-white p-6 rounded-[2rem] shadow-xl">
                    <h3 class="text-sm font-black mb-4 uppercase text-slate-400">Select Vehicle (Fuel Verified)</h3>
                    <div class="grid grid-cols-2 gap-3 mb-6">
                        <div onclick="selectCar(this, 'Mini', 9, 200, 250, 'CNG')" class="car-card border-2 p-3 rounded-2xl text-center bg-slate-50 cursor-pointer transition-all">
                            <p class="font-bold text-sm">Mini (CNG)</p><p class="text-blue-600 font-bold text-xs">₹9/KM</p>
                        </div>
                        <div onclick="selectCar(this, 'Sedan', 12, 200, 250, 'Petrol/Diesel')" class="car-card border-2 p-3 rounded-2xl text-center bg-slate-50 cursor-pointer transition-all">
                            <p class="font-bold text-sm">Sedan (P/D)</p><p class="text-blue-600 font-bold text-xs">₹12/KM</p>
                        </div>
                        <div onclick="selectCar(this, 'SUV', 15, 250, 300, 'Petrol/Diesel')" class="car-card border-2 p-3 rounded-2xl text-center bg-slate-50 cursor-pointer transition-all">
                            <p class="font-bold text-sm">Ertiga (SUV)</p><p class="text-blue-600 font-bold text-xs">₹15/KM</p>
                        </div>
                        <div onclick="selectCar(this, 'Luxury', 'Driver Set', 'Driver Set', 'Driver Set', 'Premium')" class="car-card border-2 border-yellow-500 p-3 rounded-2xl text-center bg-yellow-50 cursor-pointer transition-all shadow-md col-span-1">
                            <p class="font-bold text-sm">Luxury</p><p class="text-yellow-700 font-bold text-xs">BMW/Audi</p>
                        </div>
                    </div>

                    <div id="detailsBox" class="hidden bg-slate-900 p-4 rounded-2xl text-white mb-6">
                        <div class="flex justify-between text-[10px] uppercase font-black text-blue-400 mb-2">
                            <span>Night: <span id="nightVal" class="text-white"></span></span>
                            <span>Allow: <span id="allowVal" class="text-white"></span></span>
                        </div>
                        <p id="fuelVal" class="text-[9px] italic text-slate-400 font-bold"></p>
                    </div>

                    <div class="bg-blue-50 p-4 rounded-2xl border border-blue-100 mb-6">
                        <p class="text-[10px] font-black uppercase text-blue-800 mb-3 italic"><i class="fa-solid fa-suitcase mr-1"></i>Luggage (No Carrier)</p>
                        <div class="grid grid-cols-2 gap-3">
                            <select id="lBag" class="bg-white p-2 rounded-lg text-xs font-bold outline-none border">
                                <option>0 Large Suitcase</option><option>1 Large Suitcase</option><option>2 Large Suitcases</option>
                            </select>
                            <select id="sBag" class="bg-white p-2 rounded-lg text-xs font-bold outline-none border">
                                <option>1 Small Bag</option><option>2 Small Bags</option><option>3+ Small Bags</option>
                            </select>
                        </div>
                    </div>

                    <div class="space-y-3">
                        <input type="text" placeholder="Pick-up City" class="w-full border-b p-3 outline-none focus:border-blue-600 text-sm">
                        <input type="text" placeholder="Drop City (All India)" class="w-full border-b p-3 outline-none focus:border-blue-600 text-sm">
                        <button onclick="finish()" class="w-full bg-slate-900 text-white font-black py-5 rounded-[2rem] shadow-2xl mt-4 uppercase tracking-widest">Confirm Booking</button>
                    </div>
                </div>
            </div>
        </div>

        <script>
            function nextStep(stepId) {
                if(stepId === 'termsStep' && (!document.getElementById('custName').value || !document.getElementById('custPhone').value)) {
                    alert("Please enter Name and Phone!"); return;
                }
                document.querySelectorAll('.p-4 > div').forEach(div => div.classList.add('hidden'));
                document.getElementById(stepId).classList.remove('hidden');
                window.scrollTo(0,0);
            }

            function selectCar(el, car, rate, night, allow, fuel) {
                document.querySelectorAll('.car-card').forEach(c => c.classList.remove('active'));
                el.classList.add('active');
                document.getElementById('detailsBox').classList.remove('hidden');
                document.getElementById('nightVal').innerText = "₹"+night;
                document.getElementById('allowVal').innerText = "₹"+allow;
                document.getElementById('fuelVal').innerText = "Fuel Type: " + fuel + " (Space Verified)";
            }

            function finish() {
                alert("BOOKING SENT! \\nOur team will contact you within 5 minutes for driver details.");
            }
        </script>
    </body>
    </html>
    """, brand=BRAND, phone=SUPPORT)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
