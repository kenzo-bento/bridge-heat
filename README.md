# Bridge Heat

**Bridge Heat** is a custom Home Assistant integration that collects temperature sensor data from your Home Assistant instance and uploads it to an external database for monitoring, analytics, and research use cases.

This integration is designed for users who want reliable, structured access to long-term temperature data outside of Home Assistant’s built-in recorder.

---

## Features

- Collects temperature readings from Home Assistant sensors  
- Periodic sampling at configurable intervals  
- Uploads data to an external database or API endpoint  
- Configurable via the Home Assistant UI (config flow)  
- Suitable for research, analytics, and long-term storage  

---

## Installation

### Option 1: HACS (Recommended)

1. Open **HACS** in Home Assistant  
2. Go to **Integrations**  
3. Click **⋮ → Custom repositories**  
4. Add this repository URL  
   - Category: **Integration**
5. Search for **Bridge Heat** and install
6. Restart Home Assistant

---

### Option 2: Manual Installation

1. Copy the `bridge_heat` folder into: /config/custom_components/bridge_heat/
2. Restart Home Assistant

---

## Configuration

After installation:

1. Go to **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for **Bridge Heat**
4. Follow the setup steps to:
- Select permissions for environmental data
- Configure upload intervals

All configuration is handled through the UI — no YAML required.

---

## Data Handling

- Temperature values are collected asynchronously from Home Assistant entities
- Data is batched and uploaded at configurable intervals
- No data is stored permanently inside Home Assistant unless explicitly configured

---

## Use Cases

- Research data collection  
- Long-term environmental monitoring  
- External analytics pipelines  
- Data science and modeling workflows  

---

## Requirements

- Home Assistant 2023.6 or newer (recommended)
- At least one temperature sensor entity
- Network access to the external database or API endpoint

---

## Roadmap

- [ ] Support for additional sensor types  \
- [ ] Support for additional data variables \

---

## Contributing

Contributions are welcome!

If you encounter bugs or have feature requests, please open an issue on GitHub.

---

## License

MIT License


