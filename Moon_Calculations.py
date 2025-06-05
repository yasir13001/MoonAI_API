import ephem
import numpy as np
from datetime import datetime,timedelta
import pandas as pd
import math

def get_sunset_time(lat, lon, date,elevation=0,pressure=1013.25, horizon='0', epoch='2000'):
    """Calculate the sunset time for a given location and date."""
    if hasattr(date, 'datetime'):
        date = date.datetime  # Convert Astropy Time to datetime if needed
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.elev = elevation
    observer.horizon = horizon
    observer.date = ephem.Date(date.date())  # Convert datetime to ephem.Date

    sun = ephem.Sun()
    try:
        sunset_time = observer.next_setting(sun).datetime()
        return sunset_time
    except ephem.AlwaysUpError:
        return "Sun always up"
    except ephem.NeverUpError:
        return "Sun never rises"

def illum(a):#converting elongation to illumination
           val = 50*(1-math.cos(math.radians(a)))
           val = round(val, 1)
           return val

def calculate_q_and_visibility(arcv,width):
    """Calculate q value and determine crescent visibility criteria."""
    w = width * 60  # Convert to arcseconds
    
    q = (arcv - (11.8371 - 6.3226 * w + 0.7319 * w**2 - 0.1018 * w**3)) / 10
    
    if q > 0.216:
        visibility = "A"
    elif 0.216 >= q > -0.014:
        visibility = "B"
    elif -0.014 >= q > -0.160:
        visibility = "C"
    elif -0.160 >= q > -0.232:
        visibility = "D"
    elif -0.232 >= q > -0.293:
        visibility = "E"
    else:
        visibility = "F"
    
    return (round(q,2),visibility)



def time_zone(time,zone):
    time = time + timedelta(hours=zone)  # Manually add UTC+5
    return time

def get_moon_parameters(obs_date, lat, lon, elevation=0, pressure=1013.25, horizon='0', epoch='2000',):
    """Calculate Moon and Sun parameters using PyEphem."""
    
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.elev = elevation
    observer.pressure = pressure
    observer.horizon = horizon
    observer.epoch = epoch
    observer.date = obs_date

    moon = ephem.Moon()
    sun = ephem.Sun()

    moon.compute(observer)
    sun.compute(observer)

    # Convert values from radians to degrees
    moon_phase = moon.phase
    moon_alt = np.degrees(float(moon.alt))
    moon_az = np.degrees(float(moon.az))
    sun_alt = np.degrees(float(sun.alt))
    sun_az = np.degrees(float(sun.az))

    arcv = moon_alt - sun_alt
    moon_illum = moon_phase
    moon_ang_diam = moon.size / 60.0
    moon_dist = moon.earth_distance
#     elongation = np.degrees(ephem.separation(moon, sun))
    # Geocentric elongation using g_ra/g_dec
    elongation = np.degrees(ephem.separation(
        (moon.g_ra, moon.g_dec), (sun.g_ra, sun.g_dec)
    ))
    illumination = illum(elongation)
    daz = sun_az - moon_az    
    arcl = elongation
    parallax = np.arcsin(6378.1 / (moon_dist * 149597870.7))
    sd = 0.27245 * np.sin(parallax)
    sd_prime = sd * (1 + np.sin(np.radians(moon_alt)) * np.sin(parallax))
    w = sd_prime * (1 - np.cos(np.radians(arcl)))
    sunset = obs_date

    try:
        moonset = observer.next_setting(moon).datetime()
    except ephem.AlwaysUpError:
        moonset = "Moon always up"
    except ephem.NeverUpError:
        moonset = "Moon never rises"

    q_value, visibility_criterion = calculate_q_and_visibility(arcv,w)

    # 🌙 Moon Age Calculation
    conjunction_time = ephem.previous_new_moon(observer.date)
    moon_age_days = observer.date - conjunction_time
    moon_age_hours = int(moon_age_days * 24)
    moon_age_minutes = int((moon_age_days * 24 * 60) % 60)
    moon_age_str = f"{moon_age_hours} hrs {moon_age_minutes} mins"
    conjunction_utc = ephem.Date(conjunction_time).datetime()

    def rnd (value):
        return round(value,4)

    data = {
        "date":obs_date.date(),
        "location":
        {
            "latitude":lat,
            "longitude": lon,
            "elevation": elevation,
            "horizon": horizon,
            "epoch": epoch
        },
       "moon":{
            "conj_time": conjunction_utc.time(),
            "moon_altitude": rnd(moon_alt),
            "moon_azimuth": rnd(moon_az),
            "arcv": rnd(arcv),
            "arcl": rnd(arcl),
            "crescent_width": rnd(w),
            "moon_phase": rnd(moon_phase),
            "moon_illumination": rnd(illumination),
            "moon_angular_diameter": rnd(moon_ang_diam),
            "moon_distance_au": rnd(moon_dist),
            "elongation": rnd(elongation),
            "moonset_time": moonset.time(),
            "moon_age": moon_age_str,
            "q_value": rnd(q_value),
            "visibility_criterion": visibility_criterion
       },
       "sun": {
            "sun_altitude": rnd(sun_alt),
            "sun_azimuth": rnd(sun_az),
             "sunset_time": sunset.time(),
             "daz": rnd(daz),
       }
    }
    return data

 


