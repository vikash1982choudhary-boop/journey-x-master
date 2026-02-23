@app.route('/driver')
def driver_portal():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Driver Partner - {{brand}}</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body class="bg-slate-900 pb-10 text-slate-100">
        <nav class="bg-slate-800 p-5 border-b border-slate-700 flex justify-between items-center">
            <h1 class="text-xl font-black italic text-blue-400">{{brand}} DRIVER</h1>
            <div class="bg-green-500/10 px-3 py-1 rounded-full border border-green-500/20">
                <span class="text-[10px] font-bold text-green-400 uppercase">New Partner Bonus: 5.0 ⭐</span>
            </div>
        </nav>

        <div class="p-6 max-w-md mx-auto space-y-6">
            <div class="bg-slate-800 p-6 rounded-[2rem] border border-slate-700 shadow-xl">
                <h2 class="text-lg font-bold mb-4 flex items-center"><i class="fa-solid fa-id-card mr-2 text-blue-400"></i> Personal Info</h2>
                <div class="space-y-4">
                    <input type="text" placeholder="Full Name" class="w-full bg-slate-900 border border-slate-700 p-4 rounded-2xl outline-none focus:border-blue-500">
                    <input type="tel" placeholder="Mobile Number" class="w-full bg-slate-900 border border-slate-700 p-4 rounded-2xl outline-none focus:border-blue-500">
                </div>
            </div>

            <div class="bg-slate-800 p-6 rounded-[2rem] border border-slate-700 shadow-xl">
                <h2 class="text-lg font-bold mb-4 flex items-center"><i class="fa-solid fa-car mr-2 text-blue-400"></i> Vehicle & Pricing</h2>
                <div class="space-y-4">
                    <select id="vType" onchange="checkPriceLimit()" class="w-full bg-slate-900 border border-slate-700 p-4 rounded-2xl outline-none text-slate-400 font-bold">
                        <option value="Mini">Mini (Max ₹9/KM)</option>
                        <option value="Sedan">Sedan (Max ₹12/KM)</option>
                        <option value="SUV">SUV/Ertiga (Max ₹15/KM)</option>
                        <option value="Innova">Innova (Max ₹20/KM)</option>
                        <option value="Luxury">Luxury (Your Choice)</option>
                    </select>
                    
                    <div class="bg-blue-600/10 p-4 rounded-2xl border border-blue-500/20">
                        <label class="text-[10px] font-bold text-blue-400 uppercase">Set Your Rate (₹ per KM)</label>
                        <input type="number" id="dRate" oninput="checkPriceLimit()" placeholder="Enter Rate" class="w-full bg-transparent text-2xl font-black outline-none mt-1">
                        <p id="limitMsg" class="text-[9px] text-slate-500 mt-2 font-bold"></p>
                    </div>
                </div>
            </div>

            <div class="bg-slate-800 p-6 rounded-[2rem] border border-slate-700 shadow-xl">
                <h2 class="text-lg font-bold mb-4 flex items-center"><i class="fa-solid fa-route mr-2 text-blue-400"></i> Service Types</h2>
                <div class="grid grid-cols-2 gap-3">
                    <label class="p-3 border border-slate-700 rounded-xl flex items-center space-x-2 bg-slate-900/50">
                        <input type="checkbox" class="accent-blue-500"> <span class="text-xs font-bold">One Way</span>
                    </label>
                    <label class="p-3 border border-slate-700 rounded-xl flex items-center space-x-2 bg-slate-900/50">
                        <input type="checkbox" class="accent-blue-500"> <span class="text-xs font-bold">Round Trip</span>
                    </label>
                    <label class="p-3 border border-slate-700 rounded-xl flex items-center space-x-2 bg-slate-900/50">
                        <input type="checkbox" class="accent-blue-500"> <span class="text-xs font-bold">Package</span>
                    </label>
                    <label class="p-3 border border-green-500/50 bg-green-500/5 rounded-xl flex items-center space-x-2">
                        <input type="checkbox" class="accent-green-500"> <span class="text-xs font-bold text-green-400">All in One</span>
                    </label>
                </div>
            </div>

            <button id="regBtn" class="w-full bg-blue-600 text-white font-black py-5 rounded-[2rem] shadow-2xl shadow-blue-500/20 uppercase tracking-widest active:scale-95 transition-all">
                Complete Registration
            </button>
        </div>

        <script>
            function checkPriceLimit() {
                const type = document.getElementById('vType').value;
                const rate = document.getElementById('dRate').value;
                const msg = document.getElementById('limitMsg');
                const btn = document.getElementById('regBtn');
                
                let limit = 9;
                if(type === 'Sedan') limit = 12;
                if(type === 'SUV') limit = 15;
                if(type === 'Innova') limit = 20;
                if(type === 'Luxury') limit = 999;

                if(rate > limit && type !== 'Luxury') {
                    msg.innerHTML = "⚠️ Max allowed for " + type + " is ₹" + limit;
                    msg.className = "text-[9px] text-red-400 mt-2 font-bold";
                    btn.disabled = true; btn.style.opacity = "0.5";
                } else {
                    msg.innerHTML = "✅ Rate is within company limits.";
                    msg.className = "text-[9px] text-green-400 mt-2 font-bold";
                    btn.disabled = false; btn.style.opacity = "1";
                }
            }
        </script>
    </body>
    </html>
    """, brand=BRAND)
