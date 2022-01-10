import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = 'jjjsokal@gmail.com'  # feel free to enter :)
MY_PASSWORD = 'Dwight123!'  # feel free to enter :)
RECEIVER = 'jakub.sokalski@yahoo.com'

# Warsaw, Ursynow
MY_LAT = 52.163704
MY_LONG = 21.023471

def is_iss_overhead():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()

    data = response.json()
    longitude = float(data['iss_position']['longitude'])
    latitude = float(data['iss_position']['latitude'])
    iss_position = (longitude, latitude)

    if MY_LAT - 5 <= latitude <= MY_LAT + 5 and MY_LONG - 5 <= longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted': 0
    }
    response = requests.get('https://api.sunrise-sunset.org/json', params = parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data['results']['sunrise']
    sunrise = int(sunrise.split('T')[1].split(':')[0])
    sunset = data['results']['sunset']
    sunset = int(sunset.split('T')[1].split(':')[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(username = MY_EMAIL, password = MY_PASSWORD)
            connection.sendmail(from_addr = MY_EMAIL, to_addrs = RECEIVER,
                                msg = f'Subject: ISS Overhead!\n\nLook up! ISS is '
                                      f'above you!')
