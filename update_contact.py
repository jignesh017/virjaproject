import re

file_path = r'd:\virjaproject\enquiries\templates\enquiries\contact.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the state block wrapper
bad_block_start = '<div class="mb-4">\n                        <label class="block text-gray-700 font-bold mb-2">State</label>\n                        <select name="state" required class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-secondary bg-white">'
good_block_start = '<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">\n                        <div>\n                            <label class="block text-gray-700 font-bold mb-2">State</label>\n                            <select id="stateSelect" name="state" required class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-secondary bg-white">'
html = html.replace(bad_block_start, good_block_start)

# Now find the end of the state select and insert city select
bad_block_end = '                        </select>\n                    </div>\n\n                    <div class="mb-6">'
good_block_end = '                        </select>\n                        </div>\n                        <div>\n                            <label class="block text-gray-700 font-bold mb-2">City</label>\n                            <select id="citySelect" name="city" required class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-secondary bg-white">\n                                <option value="" disabled selected>Select your city</option>\n                            </select>\n                        </div>\n                    </div>\n\n                    <div class="mb-6">'
html = html.replace(bad_block_end, good_block_end)

# JS code to insert before {% endblock %}
js_code = """
<script>
const stateCities = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Tirupati"],
    "Arunachal Pradesh": ["Itanagar", "Tawang", "Naharlagun", "Pasighat"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Raigarh"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Kutch"],
    "Haryana": ["Faridabad", "Gurugram", "Panipat", "Ambala", "Rohtak"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Mandi", "Solan"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Deoghar"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Mangaluru", "Belagavi"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam"],
    "Madhya Pradesh": ["Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane", "Aurangabad"],
    "Manipur": ["Imphal", "Thoubal", "Bishnupur", "Churachandpur"],
    "Meghalaya": ["Shillong", "Tura", "Nongstoin", "Jowai"],
    "Mizoram": ["Aizawl", "Lunglei", "Saiha", "Champhai"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Kota", "Bikaner", "Ajmer", "Udaipur"],
    "Sikkim": ["Gangtok", "Namchi", "Pelling", "Geyzing"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Ramagundam"],
    "Tripura": ["Agartala", "Dharmanagar", "Udaipur", "Kailashahar"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Meerut", "Noida"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rishikesh"],
    "West Bengal": ["Kolkata", "Asansol", "Siliguri", "Durgapur", "Howrah"],
    "Andaman and Nicobar Islands": ["Port Blair"],
    "Chandigarh": ["Chandigarh"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Diu", "Silvassa"],
    "Delhi": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla"],
    "Ladakh": ["Leh", "Kargil"],
    "Lakshadweep": ["Kavaratti", "Agatti"],
    "Puducherry": ["Puducherry", "Oulgaret", "Karaikal", "Yanam", "Mahe"]
};

document.addEventListener("DOMContentLoaded", function() {
    const stateSelect = document.getElementById("stateSelect");
    const citySelect = document.getElementById("citySelect");

    if (stateSelect && citySelect) {
        stateSelect.addEventListener("change", function() {
            const selectedState = this.value;
            const cities = stateCities[selectedState] || [];
            
            citySelect.innerHTML = '<option value="" disabled selected>Select your city</option>';
            cities.forEach(function(city) {
                const option = document.createElement("option");
                option.value = city;
                option.textContent = city;
                citySelect.appendChild(option);
            });
        });
        
        // initialize if state already selected (like back button)
        if (stateSelect.value) {
            stateSelect.dispatchEvent(new Event('change'));
        }
    }
});
</script>
"""

html = html.replace('{% endblock %}', js_code + '\n{% endblock %}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)
