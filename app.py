import requests, random, pycountry
from datetime import datetime
from flask import Flask, render_template, request
app = Flask(__name__,template_folder='templates')

# Default root
@app.route('/', methods=['GET', 'POST'])
def index():
    weather = {}    # Weather data
    bgimage = 'background-color:#2f3640;'   # Background
    highlights = 'border-color:#00a8ff;'    # Border colours
    
    if request.method == 'POST':    # Form is submitted
        # Request weather data
        f = open("api-key.txt", "r")    # Open api key file
        # Create and send request to openweathermap.org
        r = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + request.form.get('city') + "&units=metric&appid=" + f.read()[:-1]).json()
        f.close()   # Close api key file
        
        if r['cod'] == '404' or r['cod'] == '400':  # Invalid input
            highlights = 'border-color:#e84118;'    # Invalid input border colour
            return render_template('home.html', bgimage=bgimage, weather=weather, error="Invalid Input", borderhighlight=highlights)    # Return error
        
        else:   # Valid input
            highlights = 'border-color:#4cd137;'    # Valid input border colour
            
            weather = { # Weather information, ready to be pulled into html
                'location' : r['name'] + ', ' + pycountry.countries.get(alpha_2 = r['sys']['country']).name,    # Location (city, country)
                'details' : str(r['main']['temp']) + ' °C   ' + r['weather'][0]['description'].title(),         # Basic weather conditions
                # Time of sunrise asnd sunset formatted (hrs,mins)
                'sunriseandset' : 'Sunrise ' + str(datetime.fromtimestamp(r['sys']['sunrise'] + r['timezone']).time())[0:5] + ' - ' + str(datetime.fromtimestamp(r['sys']['sunset'] + r['timezone']).time())[0:5] + ' Sunset',
                'sunrise' : str(datetime.fromtimestamp(r['sys']['sunrise'] + r['timezone']).time())[0:5],   # Time of Sunrise (hrs,mins)
                'sunset' : str(datetime.fromtimestamp(r['sys']['sunset'] + r['timezone']).time())[0:5],     # Time of Sunset (hrs,mins)
                'clouds' : str(r['clouds']['all']) + '% Cloud Coverage',    # Cloud coverage %
                'windspeed' : str(r['wind']['speed']) + ' m/s Wind Speed',  # Wind speed m/s
                'humidity' : str(r['main']['humidity']) + '% Humidity'      # Humidity %
            }

            type = int(r['weather'][0]['icon'][:-1])    # Uses openweathermaps icon feature to determine weather type
            # Assign background image
            if type == 1: bgimage = 'background-image:url(' + random.choice(["static/img/clear1.jpg", "static/img/clear2.jpg"]) + ');'
            elif type == 2: bgimage = 'background-image:url("static/img/few-clouds.jpg");'
            elif type == 3: bgimage = 'background-image:url(' + random.choice(["static/img/clouds1.jpg", "static/img/clouds2.jpg"]) + ');'
            elif type == 4: bgimage = 'background-image:url("static/img/heavy-clouds.jpg");'
            elif type <= 10: bgimage = 'background-image:url("static/img/rain.jpg");'
            elif type == 11: bgimage = 'background-image:url("static/img/storm.jpg");'
            elif type == 13: bgimage = 'background-image:url("static/img/snow.jpg");'
            elif type == 50: bgimage = 'background-image:url("static/img/mist.jpg");'
            
            if type >= 5 and type <= 10:    # If raining add rainfall to data
                weather['rainfall'] = str(r['rain']['1h']) + ' mm of Rainfall (last hour)'
            elif type == 13:    # If snowing add snowfall to data
                weather['snowfall'] = str(r['snow']['1h']) + ' mm of Snowfall (last hour)'

    # Return valid result or no city has been input yet
    return render_template('home.html', bgimage=bgimage, weather=weather, borderhighlight=highlights)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
