import ephem
import numpy as np
from datetime import datetime,timedelta
from astropy.time import Time
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
        moonset = observer.next_setting(moon).datetime().strftime('%Y/%m/%d %H:%M:%S')
    except ephem.AlwaysUpError:
        moonset = "Moon always up"
    except ephem.NeverUpError:
        moonset = "Moon never rises"

    # 🌙 Moon Age Calculation
    conjunction_time = ephem.previous_new_moon(observer.date)
    moon_age_days = observer.date - conjunction_time
    moon_age_hours = int(moon_age_days * 24)
    moon_age_minutes = int((moon_age_days * 24 * 60) % 60)
    moon_age_str = f"{moon_age_hours} hrs {moon_age_minutes} mins"
    conjunction_utc = ephem.Date(conjunction_time).datetime()

    return {
        "moon_altitude": moon_alt,
        "moon_azimuth": moon_az,
        "sun_altitude": sun_alt,
        "sun_azimuth": sun_az,
        "arcv": arcv,
        "arcl": arcl,
        "crescent_width": w,
        "moon_phase": moon_phase,
        "moon_illumination": illumination,
        "moon_angular_diameter": moon_ang_diam,
        "moon_distance_au": moon_dist,
        "daz": daz,
        "elongation": elongation,
        "sunset_time": sunset,
        "moonset_time": moonset,
        "moon_age": moon_age_str,
        "conj_time": conjunction_utc
    }


def calculate_q_and_visibility(moon_params):
    """Calculate q value and determine crescent visibility criteria."""
    arcv = moon_params["arcv"]  # Use altitude difference
    w = moon_params["crescent_width"] * 60  # Convert to arcseconds
    
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
    
    return {"q_value": round(q,2), "visibility_criterion": visibility}



def time_zone(time,zone):
    time = time + timedelta(hours=zone)  # Manually add UTC+5
    return time


def calculate_all_locations(locations, date_str):
    """
    Generate moon parameters for multiple locations on a given date
    and return a formatted DataFrame.
    """
    obs_date = datetime.strptime(date_str, "%d-%m-%Y")
    results = []

    for loc in locations:
        try:
            sunset_dt = get_sunset_time(loc['lat'], loc['lon'], obs_date,loc["elevation"])
            moon = get_moon_parameters(sunset_dt, loc['lat'], loc['lon'],loc["elevation"])
            visibility = calculate_q_and_visibility(moon)

            # Parse sunset and moonset to datetime
            sunset = moon["sunset_time"]
            moonset = datetime.strptime(moon["moonset_time"], "%Y/%m/%d %H:%M:%S")

            # Calculate lag time in minutes
            lag_minutes = round((moonset - sunset).total_seconds() / 60)
            moon["moon_age"] = moon["moon_age"].replace("hrs", "").replace("mins", "").strip()
            moon["moon_age"] = moon["moon_age"].replace("  ", ":")
            
            sunset = time_zone(sunset,5)        
            moon["conj_time"]= time_zone(moon["conj_time"],5)          

            results.append({
                "Station": f"{loc['Station']} ({sunset.strftime('%H:%M')})",
                "lag": lag_minutes,
                "Alt": round(moon["moon_altitude"], 2),
                "Saz": round(moon["sun_azimuth"], 2),
                "dz": round(moon["daz"], 2),
                "El": round(moon["elongation"], 2),
                "ilum": round(moon["moon_illumination"], 1),
                "cat": visibility["visibility_criterion"],
                "age": moon["moon_age"],
                "conj_time": moon["conj_time"],
                "elevation": loc['elevation']
            })
        except Exception as e:
            print(f"Error with {loc['Station']}: {e}")

    df = pd.DataFrame(results)
    df.rename(columns={
        "Station": "STATION(Sunset Time)",
        "lag": "LAG TIME(Minutes) ",
        "Alt": "MOON ALTITUDE(Degrees)",
        "Saz": "SUN_AZIMUTH(Degrees)",
        "dz": "DAZ(Degrees)",
        "El": "ELONGATION(Degrees)",
        "ilum": "ILLUMINATION(%)",
        "cat": "CRITERION",
        "age": "Moon Age",
        "conj_time": "Conjunction Time"
    }, inplace=True)

    return df




locations = [
    {"Station": "Karachi", "lat": 24.8607, "lon": 67.0011, "elevation": 10},
    {"Station": "Lahore", "lat": 31.5497, "lon": 74.3436, "elevation": 217},
    {"Station": "Islamabad", "lat": 33.6844, "lon": 73.0479, "elevation": 666},
    {"Station": "Multan", "lat": 30.1575, "lon": 71.5249, "elevation": 122},
    {"Station": "Peshawar", "lat": 34.0150, "lon": 71.5805, "elevation": 359},
    {"Station": "Quetta", "lat": 30.1798, "lon": 66.9750, "elevation": 1680},
    {"Station": "Mansehra", "lat": 34.3301, "lon": 73.1968, "elevation": 1088},
    {"Station": "Dir District", "lat": 35.2071, "lon": 71.8765, "elevation": 1120},
    {"Station": "Swabi", "lat": 34.1194, "lon": 72.4698, "elevation": 340},
    {"Station": "Cherat", "lat": 33.8178, "lon": 71.9163, "elevation": 1380},
    {"Station": "Jiwani", "lat": 25.0671, "lon": 61.8053, "elevation": 0},
    {"Station": "Gilgit", "lat": 35.9208, "lon": 74.3085, "elevation": 1500},
    {"Station": "Muzaffarabad", "lat": 34.3700, "lon": 73.4700, "elevation": 737}
]
df = calculate_all_locations(locations, "28-02-2025")


# In[286]:


def select_city(df):
    results = []
    row = df.loc[df["elevation"].idxmin()]
    return{
        "age": row['Moon Age'].split(":"),
        "dt": row["Conjunction Time"].date(),
        "tm": row["Conjunction Time"].time(),
        "city": row["STATION(Sunset Time)"].split(" ")[0]
    }

