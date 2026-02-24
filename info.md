# Bridge Heat

Bridge Heat is a lightweight Home Assistant integration designed to collect selected environmental sensor data and securely upload it for external analysis.

## What Bridge Heat Does

Bridge Heat allows you to share temperature-related sensor data from your Home Assistant instance. The integration periodically gathers data from supported sensors and transmits it to an external service for processing.

This can be useful for:
- Remote environmental monitoring
- Data logging and analytics
- Research or personal dashboards
- Cloud-based visualization

---

## What Data Is Collected

Bridge Heat only collects the types of data you explicitly allow during setup.

Depending on your selection, this may include:

- 🌡 **Temperature data**
- 💧 **Humidity data**
- 🌬 **Pressure data**

Only sensor values and timestamps are collected.  
No personal information, location data, account credentials, or unrelated entities are accessed.

---

## Your Control & Permissions

You are always in control.

During the next step of setup, you will be asked to choose which sensor categories you want to enable. Only the options you select will be collected and uploaded.

If you change your mind later, you can modify your permissions at any time in the integration's Options settings.

---

## Transparency & Privacy

Bridge Heat does **not**:
- Modify your sensors
- Control devices
- Access cameras or media
- Collect unrelated Home Assistant data

It reads only the sensor types you approve and operates in the background at scheduled intervals.

---

When you click **Install** or **Configure**, you will be prompted to select your permissions.

Please review your choices carefully before continuing.
