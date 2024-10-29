import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk, ImageSequence
import threading
import time

# Import functions from the script (these should match the previous implementation)
from usbswitcher import switchDeviceToModemMode
from at_utils import enableADB
from adb_utils import waitForDevice, uploadAndRunFRPBypass

# Initialize main window with a futuristic dark theme
root = ThemedTk(theme="arc")
root.title("Device Control Dashboard")
root.geometry("800x600")
root.configure(bg="#0d0d0d")

# Font and style configurations
neon_font = ("Helvetica", 14, "bold")
status_font = ("Helvetica", 10, "bold")
neon_color = "#39ff14"  # Bright neon green for a cyberpunk effect

# Background image
bg_image_path = "/path/to/your/background.jpg"
bg_image = Image.open(bg_image_path).resize((800, 600))
bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Status display
status_label = tk.Label(root, text="Status: Ready", font=status_font, bg="#0d0d0d", fg=neon_color)
status_label.pack(pady=10)

# Function to update the status label with real-time feedback
def update_status(message):
    status_label.config(text=f"Status: {message}")
    status_label.update()

# Neon-styled buttons with hover effect
def neon_button(text, command, row):
    btn = tk.Button(
        root, text=text, font=neon_font, fg=neon_color, bg="#1a1a1a", activebackground="#333333", activeforeground=neon_color,
        bd=0, highlightthickness=0, padx=10, pady=5, command=command
    )
    btn.grid(row=row, column=1, pady=15, padx=5)
    return btn

# Run the device switching process
def switch_to_modem_mode():
    update_status("Switching device to modem mode...")
    threading.Thread(target=lambda: run_in_thread(switchDeviceToModemMode, "Device in modem mode")).start()

# Enable ADB on the connected device
def enable_adb_mode():
    update_status("Enabling ADB...")
    threading.Thread(target=lambda: run_in_thread(enableADB, "ADB Enabled")).start()

# Wait for device connection
def wait_for_device():
    update_status("Waiting for device connection...")
    threading.Thread(target=lambda: run_in_thread(waitForDevice, "Device connected")).start()

# Run FRP bypass
def run_frp_bypass():
    update_status("Running FRP bypass...")
    threading.Thread(target=lambda: run_in_thread(uploadAndRunFRPBypass, "FRP bypass complete")).start()

# Helper function to run commands in a thread with status updates
def run_in_thread(command, success_message):
    try:
        command()
        update_status(success_message)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        update_status("Error encountered")

# Add buttons with corresponding functions
neon_button("Switch to Modem Mode", switch_to_modem_mode, 1)
neon_button("Enable ADB", enable_adb_mode, 2)
neon_button("Wait for Device", wait_for_device, 3)
neon_button("Run FRP Bypass", run_frp_bypass, 4)

# Animated neon loader (optional)
loader_path = "/path/to/loader.gif"
try:
    loader_image = Image.open(loader_path)
    frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(loader_image)]
    loader_label = tk.Label(root, bg="#0d0d0d")
    loader_label.grid(row=5, column=1)

    def animate_loader():
        while True:
            for frame in frames:
                loader_label.config(image=frame)
                loader_label.update()
                time.sleep(0.1)
except Exception as e:
    print(f"Loader animation error: {e}")

# Start loader animation in a separate thread
threading.Thread(target=animate_loader, daemon=True).start()

# Run the main loop
root.mainloop()
