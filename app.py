from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'  # Path to the database
app.config['SQLALCHEMY_ECHO'] = True  # Echoes SQL for debugging
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# WeatherData model
class WeatherData(db.Model):
    print("test")
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # Storing date as a string
    time = db.Column(db.String(8), nullable=False)  # Storing time as a string
    timezone_offset = db.Column(db.String(6), nullable=False)
    coordinates = db.Column(db.String(50), nullable=False)
    water_temp = db.Column(db.Float, nullable=False)
    air_temp = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    wind_direction = db.Column(db.String(3), nullable=False)
    precipitation = db.Column(db.Float, nullable=True)
    haze = db.Column(db.Boolean, nullable=True)
    notes = db.Column(db.Text, nullable=True)

# Endpoint to add weather data
@app.route('/weather/add/', methods=['POST'])
def add_weather():
    print("test")
    data = request.get_json()
    try:
        new_weather = WeatherData(
            date=data['date'],
            time=data['time'],
            timezone_offset=data['timezone_offset'],
            coordinates=data['coordinates'],
            water_temp=data['water_temp'],
            air_temp=data['air_temp'],
            humidity=data['humidity'],
            wind_speed=data['wind_speed'],
            wind_direction=data['wind_direction'],
            precipitation=data.get('precipitation'),
            haze=data.get('haze', False),  # Default haze to False if not provided
            notes=data.get('notes'),
        )
        db.session.add(new_weather)
        db.session.commit()
        return jsonify({"message": "Weather data added successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Endpoint to retrieve weather data
@app.route('/weather', methods=['GET'])
def get_weather():
    print("test")
    weather_data = WeatherData.query.all()
    grouped_weather = {}
    for weather in weather_data:
        date_key = weather.date
        if date_key not in grouped_weather:
            grouped_weather[date_key] = []
        grouped_weather[date_key].append({
            "time": weather.time,
            "timezone_offset": weather.timezone_offset,
            "coordinates": weather.coordinates,
            "water_temp": weather.water_temp,
            "air_temp": weather.air_temp,
            "humidity": weather.humidity,
            "wind_speed": weather.wind_speed,
            "wind_direction": weather.wind_direction,
            "precipitation": weather.precipitation,
            "haze": weather.haze,
            "notes": weather.notes,
        })
    response = {
        "metadata": {
            "total_entries": len(weather_data),
            "dates_included": list(grouped_weather.keys()),
        },
        "data": grouped_weather,
    }
    return jsonify(response), 200



