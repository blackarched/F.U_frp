from usbswitcher import switchDeviceToModemMode
from at_utils import enableADB
from adb_utils import waitForDevice, uploadAndRunFRPBypass
import time

def main():
    print("Starting Device Setup...")

    # Step 1: Switch device to modem mode
    if not switchDeviceToModemMode():
        print("Failed to switch device to modem mode. Exiting.")
        return

    # Step 2: Enable ADB on the device
    print("Enabling ADB on the device...")
    enableADB()
    
    # Step 3: Wait for device connection
    print("Waiting for the device to connect via ADB...")
    waitForDevice()
    
    # Step 4: Run FRP bypass process
    print("Running FRP bypass...")
    uploadAndRunFRPBypass()

    print("Process complete. Check your device for changes.")

if __name__ == "__main__":
    main()

