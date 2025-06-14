# 🌙 MoonAI API (FastAPI)

This is a FastAPI-based web service that provides astronomical data for the **moon and sun**, including visibility, phase, altitude, azimuth, and more based on a given location, date, and timezone.

---

## 📦 Features

- Calculate **sunset time** based on geographic coordinates
- Retrieve **moon parameters** like:
  - Altitude, azimuth
  - Illumination
  - Angular diameter
  - Elongation, Illumination,crescent width
- Determine **visibility** using Q and ARCV/ARCL models
- Timezone-aware input support
- Built for Python **3.6.13**

---

## 🚀 Getting Started

### ✅ Requirements

- Python 3.6.13 (recommend using `virtualenv`)
- pip

### 📥 Installation

1. **Clone the repository** (or download the source):

   ```bash
   git clone https://github.com/yasir13001/MoonAI_API.git
   cd to/project folder
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8080
   ```

---

## 🛰️ API Usage

### Endpoint

```
POST https://moonai-api.onrender.com/moon_data
```

### Request Body (JSON)

```json
{
  "city": "Karachi"
  "lat": 24.8607,
  "lon": 67.0011,
  "elevation": 10,
  "date": "06-05-2025",
  "timezone": "Asia/Karachi"
}
```

| Field       | Type   | Description                             |
| ----------- | ------ | --------------------------------------- |
| `city`      | string | Optional               |
| `lat`       | float  | Latitude of the location                |
| `lon`       | float  | Longitude of the location               |
| `elevation` | float  | Elevation above sea level in meters     |
| `date`      | string | Observation date in `dd-mm-yyyy` format |
| `timezone`  | string | IANA timezone string (`Asia/Karachi`)   |

### Response (Example)

```json
{
    "date": "2025-05-06",
    "location": {
        "city": "Karachi",
        "latitude": 24.8607,
        "longitude": 67.0011,
        "elevation": 10.0,
        "horizon": 0,
        "epoch": 2000
    },
    "moon": {
        "conj_time": "19:31:05.832017",
        "moon_altitude": 66.0618,
        "moon_azimuth": 127.6396,
        "arcv": 66.3244,
        "arcl": 113.1291,
        "crescent_width": 0.0063,
        "moon_phase": 69.7402,
        "moon_illumination": 69.6,
        "moon_angular_diameter": 30.5158,
        "moon_distance_au": 0.0026,
        "elongation": 113.1291,
        "moonset_time": "21:46:21.874486",
        "moon_age": "210 hrs 33 mins",
        "q_value": 5.68,
        "visibility_criterion": "A"
    },
    "sun": {
        "sun_altitude": -0.2626,
        "sun_azimuth": 288.9104,
        "sunset_time": "14:04:40.216956",
        "daz": 161.2708
    }
}
```

---

## 🧠 Dependencies

All dependencies are listed in `requirements.txt`. Key libraries used:

* `fastapi`
* `pydantic`
* `uvicorn`
* `ephem`
* `pytz`
* `datetime`

---

## 📄 License

MIT License

---

## 🤝 Contributing

Pull requests and suggestions welcome. For major changes, open an issue first to discuss what you’d like to change.

---

## 📬 Contact

Maintainer: [yasirkhan](mailto:yasirkhan1301@gmail.com)
LinkedIn: in/yasir-khan-13194dt




