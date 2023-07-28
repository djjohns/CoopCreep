from phew import logging, server, connect_to_wifi
from phew.template import render_template
from secret import ssid, password
from machine import ADC
import time
adc = machine.ADC(4) 

connect_to_wifi(ssid, password)
def get_ip_address():
  import network
  try:
    return network.WLAN(network.STA_IF).ifconfig()[0]
  except:
    return None
ip_address = get_ip_address()
logging.info("IP Address:", ip_address)

@server.route("/")
def index(request):
    return render_template("home.html", name="userNamePlaceholder", title="userNamePlaceholder's Chicken Coop Monitoring Service")

@server.route("/about")
def about(request):
    return render_template("about.html", name="userNamePlaceholder", title="About this Site")

@server.route("/login", ["POST",'GET'])
def login_form(request):
    print(request.method)
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':    
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        if username == "userNamePlaceholder" and password == "password":
            return render_template('template.html', content = f"Welcome back, {username}")
        else:
            return render_template('template.html', content = "Invalid username or password")
        
@server.route("/temp")
def temp_readout(request):
    ADC_voltage = adc.read_u16() * (3.3 / (65535))
    temperature_celsius = 27 - (ADC_voltage - 0.706)/0.001721
    temp_fahrenheit=32+(1.8*temperature_celsius)
    degree = chr(176) # create from known unicode point
    return render_template('template.html', content = f'Current CPU Temperature: {temp_fahrenheit}{degree} F')

# Set up onboard temperature sensor (internal temperature sensor on the RP2040)
sensor_temp = ADC(4)

# Route to display the thermometer page with temperature readout
@server.route("/thermometer")
def display_thermometer(request):
    ADC_voltage = sensor_temp.read_u16() * (3.3 / (65535))
    temperature_celsius = 27 - (ADC_voltage - 0.706)/0.001721
    temp_fahrenheit=32+(1.8*temperature_celsius)
    degree = chr(176)
    mercury_fill_div = f'{temp_fahrenheit}'
    return render_template(
        "thermometer.html",
        current_temp = mercury_fill_div,
        degree_symbol = degree
    )

@server.catchall()
def my_catchall(request):
  return "No matching route", 404

server.run()

