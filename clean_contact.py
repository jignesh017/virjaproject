import re

file_path = r'd:\virjaproject\enquiries\templates\enquiries\contact.html'

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Clean up messed up scripts
html = re.sub(r'<script>.*?const stateCities.*?</script>\s*{% endblock %}', '{% endblock %}', html, flags=re.DOTALL)

# 2. Re-inject clean script at the correct place
# The last {% endblock %} is usually block content.
# Since we replaced all of them with {% endblock %}, they are clean now.
# Let's find the main content div end
js_code = """
<script src="{% static 'js/cities.js' %}"></script>
<script>
document.addEventListener("DOMContentLoaded", function() {
    const stateSelect = document.getElementById("stateSelect");
    const citySelect = document.getElementById("citySelect");

    if (stateSelect && citySelect) {
        stateSelect.addEventListener("change", function() {
            const selectedState = this.value;
            // The JSON from cities.js uses the 'stateCities' variable
            const cities = typeof stateCities !== 'undefined' ? (stateCities[selectedState] || []) : [];
            
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
{% endblock %}
"""

# Replace ONLY the last {% endblock %}
parts = html.rsplit('{% endblock %}', 1)
if len(parts) == 2:
    html = parts[0] + js_code + parts[1]

# 3. Add {% load static %} line 2 if missing
if '{% load static %}' not in html:
    html = html.replace('{% extends \'base.html\' %}', '{% extends \'base.html\' %}\n{% load static %}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)
