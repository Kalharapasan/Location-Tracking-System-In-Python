import tkinter as tk
from tkinter import messagebox, ttk
import phonenumbers
from phonenumbers import geocoder, carrier
from geopy.geocoders import Nominatim
import webbrowser

class PhoneLocationTracker:
    def __init__(self, master):
        self.master = master
        master.title("📍 Phone Location Tracker")
        master.geometry("600x700")
        master.configure(bg='white')

        self.style = ttk.Style()
        self.style.configure('TLabel', background='white', font=('Segoe UI', 12))
        self.style.configure('TButton', font=('Segoe UI', 12), padding=6)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.master, text="📱 Phone Location Tracker", font=("Segoe UI", 18, 'bold')).pack(pady=(20, 10))

        # Country code selection
        ttk.Label(self.master, text="Select Country Code:").pack(pady=(10, 5))
        country_codes = [
            "+1 (USA)", "+44 (UK)", "+91 (India)", "+94 (Sri Lanka)", "+81 (Japan)",
            "+61 (Australia)", "+86 (China)", "+49 (Germany)", "+7 (Russia)"
        ]
        self.country_code = tk.StringVar(value=country_codes[0])
        country_dropdown = ttk.Combobox(self.master, textvariable=self.country_code, values=country_codes, width=30)
        country_dropdown.pack(pady=5)

        # Phone number entry
        ttk.Label(self.master, text="Enter Phone Number:").pack(pady=(10, 5))
        self.phone_entry = ttk.Entry(self.master, width=40)
        self.phone_entry.pack(pady=5)

        # Track Button
        track_btn = ttk.Button(self.master, text="🔍 Track Location", command=self.track_location)
        track_btn.pack(pady=20)

        # Results frame
        self.result_frame = tk.Frame(self.master, bg='white')
        self.result_frame.pack(pady=10)

        self.result_labels = {}

        fields = ['location', 'region', 'network', 'latitude', 'longitude']
        icons = {
            'location': '🔑', 'region': '🌍', 'network': '🔧',
            'latitude': '🧽', 'longitude': '🧽'
        }

        for field in fields:
            label = ttk.Label(self.result_frame, text="", font=('Segoe UI', 11))
            label.pack(pady=2)
            self.result_labels[field] = label

        self.map_button = None

    def validate_sri_lankan_number(self, number):
        number = number.replace(' ', '').replace('-', '')
        if not number.isdigit() or len(number) != 9:
            return False
        return number[:2] in ['70', '71', '72', '75', '77', '78']

    def track_location(self):
        for label in self.result_labels.values():
            label.config(text="")

        if self.map_button:
            self.map_button.destroy()

        raw_number = self.phone_entry.get().strip()
        country_code = self.country_code.get().split()[0]
        full_number = country_code + raw_number

        try:
            # Sri Lanka validation
            if country_code == "+94" and not self.validate_sri_lankan_number(raw_number):
                messagebox.showerror("Invalid", "Sri Lankan number must be like: 781234567 or 771234567")
                return

            parsed = phonenumbers.parse(full_number)
            if not phonenumbers.is_valid_number(parsed):
                messagebox.showerror("Error", "Invalid phone number")
                return

            region = geocoder.description_for_number(parsed, "en")
            network = carrier.name_for_number(parsed, "en")

            if not network:
                network = "Unknown"

            geolocator = Nominatim(user_agent="phone_location_tracker")

            if country_code == "+94":
                location = geolocator.geocode("Sri Lanka")
                custom_networks = {
                    '70': 'CellTel Network',
                    '71': 'Dialog Network',
                    '72': 'Mobitel Network',
                    '75': 'Hutch Network',
                    '77': 'Dialog Network',
                    '78': 'Mobitel Network'
                }
                network = custom_networks.get(raw_number[:2], 'Unknown')

            else:
                location = geolocator.geocode(region)

            if location:
                self.result_labels['location'].config(text=f"🔑 Location: {region}")
                self.result_labels['region'].config(text=f"🌍 Country/Region: {region}")
                self.result_labels['network'].config(text=f"🔧 Service Provider: {network}")
                self.result_labels['latitude'].config(text=f"🧽 Latitude: {location.latitude}")
                self.result_labels['longitude'].config(text=f"🧽 Longitude: {location.longitude}")

                maps_url = f"https://www.google.com/maps/search/?api=1&query={location.latitude},{location.longitude}"
                self.map_button = tk.Button(self.master, text="🗺️ Open in Google Maps", bg='#28a745', fg='white',
                                            font=("Segoe UI", 11, 'bold'), padx=10, pady=5,
                                            command=lambda: webbrowser.open(maps_url))
                self.map_button.pack(pady=20)
            else:
                messagebox.showinfo("Not Found", "Could not determine location.")

        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    app = PhoneLocationTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
