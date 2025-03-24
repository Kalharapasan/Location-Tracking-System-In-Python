import tkinter as tk
from tkinter import messagebox, ttk
import phonenumbers
from phonenumbers import geocoder
from geopy.geocoders import Nominatim
import webbrowser
import os

class PhoneLocationTracker:
    def __init__(self, master):
        self.master = master
        master.title("Phone Location Tracker")
        master.geometry("600x700")
        master.configure(bg='#f0f0f0')

        # Style
        self.style = ttk.Style()
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12))

        # Create UI Components
        self.create_widgets()

    def create_widgets(self):
        # Country Code Dropdown
        ttk.Label(self.master, text="Select Country Code:", style='TLabel').pack(pady=(20, 5))
        
        # Country codes list with Sri Lanka added
        country_codes = [
            "+1 (USA)", "+44 (UK)", "+91 (India)", "+86 (China)", 
            "+81 (Japan)", "+49 (Germany)", "+7 (Russia)", "+61 (Australia)",
            "+94 (Sri Lanka)"
        ]
        self.country_code = tk.StringVar(value=country_codes[0])
        country_dropdown = ttk.Combobox(
            self.master, 
            textvariable=self.country_code, 
            values=country_codes, 
            width=30
        )
        country_dropdown.pack(pady=5)

        # Phone Number Entry with placeholder and validation
        ttk.Label(self.master, text="Enter Phone Number:", style='TLabel').pack(pady=(10, 5))
        self.phone_entry = ttk.Entry(self.master, width=40)
        self.phone_entry.insert(0, "Valid formats: 701234567, 711234567, 721234567, 751234567, 771234567, 781234567")
        self.phone_entry.bind('<FocusIn>', self.clear_placeholder)
        self.phone_entry.bind('<FocusOut>', self.restore_placeholder)
        self.phone_entry.pack(pady=5)

        # Track Button
        track_button = ttk.Button(
            self.master, 
            text="Track Location", 
            command=self.track_location,
            style='TButton'
        )
        track_button.pack(pady=20)

        # Result Display Area
        self.result_frame = tk.Frame(self.master, bg='#f0f0f0')
        self.result_frame.pack(pady=10, expand=True, fill='both')

        # Location Details Labels
        self.location_label = ttk.Label(
            self.result_frame, 
            text="Location Details:", 
            style='TLabel'
        )
        self.location_label.pack(pady=(10, 5))

        self.details_label = ttk.Label(
            self.result_frame, 
            text="", 
            style='TLabel', 
            wraplength=500
        )
        self.details_label.pack(pady=5)

    def clear_placeholder(self, event):
        """Clear placeholder text when entry is focused"""
        if self.phone_entry.get() == "Valid formats: 701234567, 711234567, 721234567, 751234567, 771234567, 781234567":
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.config(foreground='black')

    def restore_placeholder(self, event):
        """Restore placeholder if no text is entered"""
        if not self.phone_entry.get():
            self.phone_entry.insert(0, "Valid formats: 701234567, 711234567, 721234567, 751234567, 771234567, 781234567")
            self.phone_entry.config(foreground='gray')

    def validate_sri_lankan_number(self, number):
        """
        Validate Sri Lankan mobile number formats
        Accepted formats: 
        - 701234567, 711234567, 721234567, 751234567, 771234567, 781234567 (without leading zero)
        """
        # Remove any spaces or dashes
        number = number.replace(' ', '').replace('-', '')
        
        # Check if number contains only digits
        if not number.isdigit():
            return False
        
        # Check length (9 digits)
        if len(number) != 9:
            return False
        
        # Check if starts with valid prefixes
        valid_prefixes = ['70', '71', '72', '75', '77', '78']
        return number[:2] in valid_prefixes

    def track_location(self):
        # Clear previous results
        self.details_label.config(text="")

        # Get phone number
        phone_number = self.phone_entry.get()
        country_code = self.country_code.get().split()[0]
        full_number = country_code + phone_number

        try:
            # Special validation for Sri Lankan numbers
            if country_code == "+94":
                if not self.validate_sri_lankan_number(phone_number):
                    messagebox.showerror("Error", "Invalid Sri Lankan Mobile Number\nUse formats like 701234567, 711234567, 721234567, 751234567, 771234567, or 781234567")
                    return

            # Validate phone number
            parsed_number = phonenumbers.parse(full_number)
            
            if not phonenumbers.is_valid_number(parsed_number):
                messagebox.showerror("Error", "Invalid Phone Number")
                return

            # Get region information
            region = geocoder.description_for_number(parsed_number, "en")
            
            # Use Nominatim for geocoding
            geolocator = Nominatim(user_agent="phone_location_tracker")
            
            # For Sri Lanka, use more specific location
            if country_code == "+94":
                location = geolocator.geocode("Sri Lanka")
            else:
                location = geolocator.geocode(region)

            if location:
                # Additional Sri Lankan number details
                sri_lankan_regions = {
                    '70': 'CellTel Network',
                    '71': 'Dialog Network',
                    '72': 'Mobitel Network',
                    '75': 'Hutch Network',
                    '77': 'Dialog Network',
                    '78': 'Mobitel Network'
                }

                # Display location details
                details = (
                    f"Country/Region: {region}\n"
                )
                
                # Add network information for Sri Lankan numbers
                if country_code == "+94":
                    network = sri_lankan_regions.get(phone_number[:2], 'Unknown Network')
                    details += f"Mobile Network: {network}\n"

                details += (
                    f"Latitude: {location.latitude}\n"
                    f"Longitude: {location.longitude}\n"
                )
                
                self.details_label.config(text=details)

                # Create Google Maps URL
                maps_url = f"https://www.google.com/maps/search/?api=1&query={location.latitude},{location.longitude}"
                
                # Offer to open map
                open_map = tk.Button(
                    self.result_frame, 
                    text="Open in Google Maps", 
                    command=lambda: webbrowser.open(maps_url)
                )
                open_map.pack(pady=10)

            else:
                messagebox.showinfo("Info", "Could not locate precise coordinates")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = PhoneLocationTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
