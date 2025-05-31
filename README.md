
# 📍 Phone Location Tracker

A simple and visually-enhanced **Tkinter-based desktop application** that helps you track the **location**, **country/region**, **service provider**, and **GPS coordinates** of any valid phone number.  
It supports international numbers including 🇱🇰 **Sri Lanka**, 🇮🇳 **India**, 🇺🇸 **USA**, 🇦🇺 **Australia**, and more.

---

## ✨ Features

- ✅ Dropdown to select international country codes  
- 📞 Validates phone number format (with special rules for Sri Lankan mobile numbers)  
- 🌍 Shows detailed location information:
  - Country / Region  
  - Service Provider (Sri Lanka only)  
  - Latitude & Longitude  
- 🗺️ One-click access to **Google Maps**  
- 🎨 Clean and modern user interface with icons and improved layout

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Tkinter** – for GUI  
- [`phonenumbers`](https://pypi.org/project/phonenumbers/) – number validation and region detection  
- [`geopy`](https://pypi.org/project/geopy/) – geolocation via Nominatim  
- **webbrowser** – to open Google Maps in the default browser  

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Kalharapasan/Location-Tracking-System-In-Python.git
cd Location-Tracking-System-In-Python


# Install required dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 📌 Sri Lankan Number Rules

- Must have **exactly 9 digits** (without the leading `0`)
- Valid prefixes: `70`, `71`, `72`, `75`, `77`, `78`  
- ✅ Example of valid number: `781234567`

---

## 🌐 Supported Countries & Codes

| Country        | Code |
|----------------|------|
| 🇱🇰 Sri Lanka   | +94  |
| 🇺🇸 USA         | +1   |
| 🇬🇧 UK          | +44  |
| 🇮🇳 India       | +91  |
| 🇯🇵 Japan       | +81  |
| 🇦🇺 Australia   | +61  |
| 🇨🇳 China       | +86  |
| 🇷🇺 Russia      | +7   |
| 🇩🇪 Germany     | +49  |

---

## 📸 Screenshot

![image](https://github.com/user-attachments/assets/939ba8e9-fdae-4600-a894-fd7ac2c5dddf)

---

## ✅ TODO

- [ ] Add reverse geocoding to display exact city/district
- [ ] Show tracking history or logs
- [ ] Add dark mode toggle for better UX

---

## 📃 License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and contribute.

---

> Built with ❤️ using Python & Tkinter
