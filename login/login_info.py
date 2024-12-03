import platform
import os
import requests
import datetime

time_info = datetime.datetime.now()
final_time = time_info.strftime("%Y-%m-%d %H:%M:%S")


def get_ip_location():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        location = data.get('loc', 'Location not available')
        city = data.get('city', 'City not available')
        country = data.get('country', 'Country not available')
        region = data.get('region', 'Region not available')
        return f"Location: {city}, {region}, {country}\nCoordinates: {location}"
    except Exception as e:
        return("Error fetching location:", e)





def get_all_info():

    return f"{final_time}\n{get_ip_location()}\nSystem Name: {platform.system()}\nRelease: {platform.release()}\nVersion: {platform.version()}\nMachine Type: {platform.machine()}\nProcessor: {platform.processor()}\nPlatform Info: {platform.platform()}\nArchitecture: {platform.architecture()}\nUsername: {os.getlogin()}"




print(get_all_info())
