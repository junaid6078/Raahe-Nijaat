from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Variables to store the city and country received from the POST request
submitted_city = None
submitted_country = None

@app.route('/submit-address', methods=['POST'])
def submit_address():
    global submitted_city, submitted_country

    data = request.json
    if 'address' in data:
        address = data['address']
        # Split the address into city, state, and country
        parts = address.split(', ')
        if len(parts) == 3:
            city, state, country = parts
            submitted_city = city
            submitted_country = country
            print(f"City: {city}, State: {state}, Country: {country}")
            return jsonify({"status": "success", "message": "Address received", "city": city, "country": country}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid address format"}), 400
    else:
        return jsonify({"status": "error", "message": "No address provided"}), 400

@app.route('/get-prayer-times', methods=['GET'])
def get_prayer_times():
    global submitted_city, submitted_country

    # Default parameters with fallback to submitted city and country
    city = submitted_city if submitted_city else request.args.get('city', 'Karachi')
    country = submitted_country if submitted_country else request.args.get('country', 'Pakistan')
    method = request.args.get('method', '2')
    year = request.args.get('year', '2024')
    month = request.args.get('month', '8')
    
    print(city)
    print(country)
    print(method)
    print(year)
    print(month)
    
    # API URL
    url = f"https://api.aladhan.com/v1/calendarByCity/{year}/{month}?city={city}&country={country}&method={method}"
    
    # Fetching data from the Aladhan API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse JSON data
        return jsonify(data)     # Return JSON data to the client
    else:
        return jsonify({'error': 'Failed to fetch data from Aladhan API'}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
