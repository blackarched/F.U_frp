import usb.core
import usb.util
import time
import sys
import subprocess

# Samsung Galaxy and MediaTek device IDs
DEVICE_IDS = {
    "samsung": [{"vendor_id": 0x04e8, "product_id": 0x6860}],
    "mediatek": [
        {"vendor_id": 0x0e8d, "product_id": 0x2000},  # Preloader mode
        {"vendor_id": 0x0e8d, "product_id": 0x0003},  # DA USB mode
    ],
}

USB_MODEM_CONFIGURATION = 0x2

def check_dependencies():
    """Ensure necessary dependencies are installed for USB and ADB support."""
    try:
        import usb.core
    except ImportError:
        print("pyusb not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyusb"])
    
    adb_check = subprocess.run(["which", "adb"], capture_output=True, text=True)
    if adb_check.returncode != 0:
        print("ADB is not installed. Installing...")
        subprocess.run(["sudo", "apt", "install", "android-tools-adb", "-y"])

def setUSBConfig(dev: usb.core.Device, config: int) -> bool:
    try:
        dev.reset()
        dev.set_configuration(config)
        print("Device configuration set successfully.")
        return True
    except usb.core.USBError as e:
        print(f"USB configuration error: {e}")
        return False

def switchDeviceToModemMode() -> bool:
    check_dependencies()
    for device_type, device_ids in DEVICE_IDS.items():
        for ids in device_ids:
            dev = usb.core.find(idVendor=ids["vendor_id"], idProduct=ids["product_id"])
            if dev:
                print(f"{device_type.capitalize()} device detected.")
                return configureDevice(dev, device_type)
    
    print("No compatible devices found. Ensure the device is connected and drivers are installed.")
    return False

def configureDevice(dev: usb.core.Device, device_type: str) -> bool:
    try:
        actualConfig = dev.get_active_configuration().bConfigurationValue
        print(f"Device currently in USB configuration {actualConfig}.")
        
        if actualConfig != USB_MODEM_CONFIGURATION:
            print(f"Switching {device_type} device to modem mode...")
            if setUSBConfig(dev, USB_MODEM_CONFIGURATION):
                print("Device successfully switched to modem mode.")
                return True
            else:
                print("Retrying to switch configuration...")
                time.sleep(1)
                return setUSBConfig(dev, USB_MODEM_CONFIGURATION)
        else:
            print("Device is already in modem mode.")
            return True
    except usb.core.USBError as e:
        print(f"Device configuration error: {e}")
    return False

if __name__ == "__main__":
    print("Attempting to switch device to modem mode...")
    if not switchDeviceToModemMode():
        print("Failed to switch device to modem mode. Please check compatibility.")
