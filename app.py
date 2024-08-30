from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Load the JSON data
def load_data():
    try:
        with open('F-A0010-001.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: JSON file not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None

data = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather_data')
def get_weather_data():
    if not data:
        return jsonify({"error": "Data not available"}), 500

    locations = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
    
    chart_data = []
    for location in locations:
        location_name = location['locationName']
        max_temps = [float(temp['temperature']) for temp in location['weatherElements']['MaxT']['daily']]
        
        chart_data.append({
            'name': location_name,
            'data': max_temps
        })
    
    return jsonify(chart_data)

if __name__ == '__main__':
    app.run(debug=True)