<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JourneyX | Premium Taxi Booking</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    
    <style>
        .selected-tab {
            border: 2px solid white !important;
            border-radius: 9999px;
            background: rgba(255, 255, 255, 0.15);
        }
        input[type="date"]::-webkit-calendar-picker-indicator,
        input[type="time"]::-webkit-calendar-picker-indicator {
            filter: invert(1);
            cursor: pointer;
        }
    </style>

    <script>
        // --- Supabase Setup ---
        const SUPABASE_URL = "https://tqpmmqzdlttlgduykbw.supabase.co";
        const SUPABASE_KEY = "sb_publishable_vEJyQPNgldCwal0Syx2ApA__00e0lcK"; 
        const _supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

        let currentTripType = 'one-way';
        const rates = { "Mini": 9, "Sedan": 12, "Ertiga": 15, "Innova": 20, "Luxury": 65 };

        window.setTripType = (type, btn) => {
            currentTripType = type;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('selected-tab'));
            btn.classList.add('selected-tab');
            calculateFare();
        }

        window.calculateFare = () => {
            const dist = parseFloat(document.getElementById('distance').value) || 0;
            const car = document.getElementById('carSelect').value;
            const name = document.getElementById('uName').value;
            const phone = document.getElementById('uPhone').value;
            const pickup = document.getElementById('pickupLoc').value;
            const drop = document.getElementById('dropLoc').value;

            if(dist > 0 && car && name && phone && pickup && drop) {
                let effDist = (currentTripType === 'package' && dist < 250) ? 250 : dist;
                let total = effDist * rates[car];
                if (total < 1000) total = 1000;

                document.getElementById('fareAmount').innerText = "₹" + Math.round(total);
                document.getElementById('totalBox').classList.remove('hidden');
            } else {
                document.getElementById('totalBox').classList.add('hidden');
            }
        }

        window.showCustomAlert = (msg) => {
            document.getElementById('alertMessage').innerText = msg;
            document.getElementById('customAlert').classList.remove('hidden');
        };

        window.confirmBooking = () => {
            const date = document.getElementById('bookingDate').value;
            const time = document.getElementById('bookingTime').value;
            const name = document.getElementById('uName').value;
            if(!name || !date || !time) {
                showCustomAlert("Kripya saari jankari aur Time chunein!");
                return;
            }
            document.getElementById('agreementPopup').classList.remove('hidden');
        }

        window.finalSubmit = async function() {
            document.getElementById('agreementPopup').classList.add('hidden');
            
            const bookingData = {
                customer_name: document.getElementById('uName').value,
                customer_phone: document.getElementById('uPhone').value,
                pickup_location: document.getElementById('pickupLoc').value,
                drop_location: document.getElementById('dropLoc').value,
                vehicle_type: `${document.getElementById('carSelect').value} (${currentTripType})`,
                fuel_type: "Dist: " + document.getElementById('distance').value + " KM",
                luggage_details: "Fare: " + document.getElementById('fareAmount').innerText + " | Date: " + document.getElementById('bookingDate').value + " " + document.getElementById('bookingTime').value,
                status: 'pending'
            };

            try {
                // Supabase Insertion
                const { error } = await _supabase.from('bookings').insert([bookingData]);
                if (error) throw error;

                // Telegram Notification
                const botToken = "7954151806:AAHy2Q3nePpv_CqA9ymfhEmg33B229ORClI";
                const chatId = "5670868884";
                const msg = `👑 *Luxury Booking Alert!*%0A👤: ${bookingData.customer_name}%0A📱: ${bookingData.customer_phone}%0A🚗: ${bookingData.vehicle_type}%0A💰: ${bookingData.luggage_details}`;
                
                await fetch(`https://api.telegram.org/bot${botToken}/sendMessage?chat_id=${chatId}&text=${msg}&parse_mode=Markdown`);
                
                showCustomAlert("✅ Booking Safal Rahi! Hum aapse sampark karenge.");
                setTimeout(() => location.reload(), 3000);
            } catch (e) { 
                showCustomAlert("Error: Data save nahi ho saka!"); 
            }
        }
    </script>
</head>
<body class="bg-gray-50 flex justify-center">

    <div class="w-full max-w-md bg-white min-h-screen shadow-2xl relative pb-10 font-sans">
        
        <div class="bg-[#1e3a8a] p-6 rounded-b-[40px] text-white shadow-xl">
            <h1 class="text-3xl font-black italic mb-6 tracking-tighter">JourneyX</h1>
            
            <div class="flex bg-blue-900/60 p-2 rounded-2xl text-[11px] font-bold mb-6 space-x-1 text-center border border-white/10">
                <button onclick="setTripType('one-way', this)" class="tab-btn flex-1 py-2 selected-tab transition-all">One Way</button>
                <button onclick="setTripType('round-trip', this)" class="tab-btn flex-1 py-2 transition-all">Round Trip</button>
                <button onclick="setTripType('package', this)" class="tab-btn flex-1 py-2 transition-all">Package</button>
            </div>

            <div class="space-y-4">
                <input id="pickupLoc" oninput="calculateFare()" type="text" placeholder="Pickup Address" class="w-full p-4 rounded-2xl bg-white/10 border border-white/20 text-white outline-none placeholder-blue-200">
                <input id="dropLoc" oninput="calculateFare()" type="text" placeholder="Drop Address" class="w-full p-4 rounded-2xl bg-white/10 border border-white/20 text-white outline-none placeholder-blue-200">
                
                <div class="flex space-x-2">
                    <div class="flex-1">
                        <label class="text-[10px] uppercase font-bold text-blue-200 mb-1 block">📅 Journey Date</label>
                        <input id="bookingDate" type="date" class="w-full p-3 rounded-xl bg-white/10 border border-white/20 text-white outline-none text-sm">
                    </div>
                    <div class="flex-1">
                        <label class="text-[10px] uppercase font-bold text-blue-200 mb-1 block">⏰ Pickup Time</label>
                        <input id="bookingTime" type="time" class="w-full p-3 rounded-xl bg-white/10 border border-white/20 text-white outline-none text-sm">
                    </div>
                </div>

                <input id="distance" type="number" oninput="calculateFare()" placeholder="कुल किलोमीटर (Total KM)" class="w-full p-4 rounded-2xl bg-white text-blue-900 font-black text-center outline-none shadow-lg">
            </div>
        </div>

        <div class="p-6">
            <div class="space-y-4 mb-6">
                <div>
                    <label class="text-[10px] font-bold text-gray-400 uppercase ml-1">Select Car</label>
                    <select id="carSelect" onchange="calculateFare()" class="w-full p-4 border-2 border-gray-100 rounded-2xl font-bold bg-gray-50 outline-none">
                        <option value="Mini">Mini (Alto, Swift & Similar) - ₹9/KM</option>
                        <option value="Sedan">Sedan (Dzire, Etios & Similar) - ₹12/KM</option>
                        <option value="Ertiga">SUV (Ertiga, Carens & Similar) - ₹15/KM</option>
                        <option value="Innova">Premium (Innova Crysta) - ₹20/KM</option>
                        <option value="Luxury">Luxury (BMW, Audi, Mercedes) - ₹65/KM</option>
                    </select>
                </div>
                <input id="uName" oninput="calculateFare()" type="text" placeholder="Full Name" class="w-full p-4 border-2 border-gray-100 rounded-2xl outline-none">
                <input id="uPhone" oninput="calculateFare()" type="tel" placeholder="Phone Number" class="w-full p-4 border-2 border-gray-100 rounded-2xl outline-none">
            </div>

            <div id="totalBox" class="hidden bg-blue-50 border-2 border-blue-100 p-6 rounded-3xl mb-6 text-center shadow-inner">
                <p class="text-blue-800 text-xs font-bold uppercase tracking-widest">Estimated Total Fare</p>
                <h2 id="fareAmount" class="text-5xl font-black text-blue-900">₹0</h2>
                <p class="text-[10px] text-gray-400 mt-2">*Toll, Tax & Parking Extra.</p>
            </div>

            <button onclick="confirmBooking()" class="w-full bg-[#1e3a8a] text-white py-5 rounded-2xl font-black text-lg shadow-xl uppercase tracking-widest active:scale-95 transition-all">Book Now</button>
        </div>

        <div id="agreementPopup" class="hidden fixed inset-0 bg-black/80 flex items-center justify-center p-6 z-[100]">
            <div class="bg-red-600 text-white p-8 rounded-[40px] text-center shadow-2xl max-w-xs border-4 border-white/20">
                <h2 class="text-2xl font-bold mb-4 uppercase italic">Zaroori Information!</h2>
                <p class="text-sm mb-6 leading-relaxed">क्या आप **State Tax, Toll Tax और Parking** अलग से देने के लिए तैयार हैं?</p>
                <button onclick="finalSubmit()" class="w-full bg-white text-red-600 py-4 rounded-xl font-black mb-3 shadow-lg uppercase">हाँ, मैं तैयार हूँ</button>
                <button onclick="document.getElementById('agreementPopup').classList.add('hidden')" class="text-xs uppercase font-bold opacity-70">Cancel</button>
            </div>
        </div>

        <div id="customAlert" class="hidden fixed inset-0 bg-black/50 flex items-center justify-center z-[200] p-6 text-center">
            <div class="bg-white rounded-3xl p-8 max-w-xs w-full shadow-2xl border-t-8 border-blue-900">
                <p id="alertMessage" class="text-gray-800 font-bold mb-6 text-lg"></p>
                <button onclick="document.getElementById('customAlert').classList.add('hidden')" class="w-full bg-[#1e3a8a] text-white py-3 rounded-xl font-bold">OK</button>
            </div>
        </div>
    </div>
</body>
</html>
