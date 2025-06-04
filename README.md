# 🌙 MoonAI API (FastAPI)

This is a FastAPI-based web service that provides astronomical data for the **moon and sun**, including visibility, phase, altitude, azimuth, and more based on a given location, date, and timezone.

---

## 📦 Features

- Calculate **sunset time** based on geographic coordinates
- Retrieve **moon parameters** like:
  - Altitude, azimuth
  - Illumination
  - Angular diameter
  - Elongation, crescent width
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
   cd moon-data-api
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**:

   ```bash
   uvicorn main:app --reload
   ```

---

## 🛰️ API Usage

### Endpoint

```
POST /moon_data
```

### Request Body (JSON)

```json
{
  "lat": 24.8607,
  "lon": 67.0011,
  "elevation": 10,
  "date": "28-02-2025",
  "timezone": "Asia/Karachi"
}
```

| Field       | Type   | Description                             |
| ----------- | ------ | --------------------------------------- |
| `lat`       | float  | Latitude of the location                |
| `lon`       | float  | Longitude of the location               |
| `elevation` | float  | Elevation above sea level in meters     |
| `date`      | string | Observation date in `dd-mm-yyyy` format |
| `timezone`  | string | IANA timezone string (`Asia/Karachi`)   |

### Response (Example)

```json
{
  "moon_altitude": 13.5,
  "moon_azimuth": 123.4,
  "sun_altitude": -2.1,
  "sun_azimuth": 245.2,
  "arcv": 7.1,
  "arcl": 9.2,
  "crescent_width": 0.12,
  "moon_phase": "waxing crescent",
  "moon_illumination": 0.32,
  "moon_angular_diameter": 29.8,
  "moon_distance_au": 0.0025,
  "daz": 15.3,
  "elongation": 12.8,
  "sunset_time": "2025-02-28T18:12:00+05:00",
  "moonset_time": "2025-02-28T19:03:00+05:00",
  "moon_age": "2.3 days",
  "conj_time": "2025-02-26T07:34:00Z"
}
```

---

## 🧠 Dependencies

All dependencies are listed in `requirements.txt`. Key libraries used:

* `fastapi`
* `uvicorn`
* `ephem`
* `skyfield`
* `numpy`
* `astropy`
* `pandas`
* `pytz`

---

## ⚠️ Python 3.6 Notice

This project supports **Python 3.6.13**, which is **end-of-life**. Future updates may require Python 3.8+.

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




