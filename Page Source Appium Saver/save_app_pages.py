import time
import hashlib
import os
import xml.etree.ElementTree as ET
from appium import webdriver

# Configuration
APP_BUNDLE_ID = "ANY BUNDLE ID"  # Target app bundle ID
DEVICE_UDID = "UDID"  # Your device's UDID

# Set up Appium capabilities
caps = {
    "platformName": "iOS",
    "deviceName": "iPhone",
    "udid": DEVICE_UDID,
    "automationName": "XCUITest",
    "bundleId": APP_BUNDLE_ID,   # Launches only this app
    "noReset": True,             # Preserves the app state
    "newCommandTimeout": 300     # Prevents session timeouts
}

# For Appium v2, use the URL below; for v1, append '/wd/hub'
driver = webdriver.Remote("http://localhost:4723", caps)
# driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)

def compute_filtered_hash(page_source: str) -> str:
    """
    Parses the XML page source and removes dynamic attributes like 'value'
    so that minor changes (e.g., typing) are ignored. Returns an MD5 hash.
    """
    try:
        root = ET.fromstring(page_source)
    except ET.ParseError:
        # If parsing fails, fall back to full hash of the raw source
        return hashlib.md5(page_source.encode()).hexdigest()
    
    # Remove dynamic attributes that change with text input
    for elem in root.iter():
        if 'value' in elem.attrib:
            del elem.attrib['value']
    filtered_source = ET.tostring(root, encoding='utf-8')
    return hashlib.md5(filtered_source).hexdigest()

# Initialize tracking variables
saved_hashes = set()
page_count = 0

print(f"🔍 Tracking app: {APP_BUNDLE_ID}")

try:
    while True:
        # Get info about the currently active app
        active_app_info = driver.execute_script("mobile: activeAppInfo")
        current_app = active_app_info.get("bundleId", "")

        if current_app == APP_BUNDLE_ID:
            # Get the current page source
            page_source = driver.page_source
            # Compute the filtered hash
            current_filtered_hash = compute_filtered_hash(page_source)
            
            if current_filtered_hash not in saved_hashes:
                saved_hashes.add(current_filtered_hash)
                page_count += 1
                filename = f"page_{page_count}.xml"
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(page_source)
                print(f"📄 Saved new page source: {filename}")
            else:
                print("🔄 Page already saved, skipping.")
        else:
            print(f"⚠️ Not in {APP_BUNDLE_ID} (currently in {current_app}), waiting...")

        # Adjust sleep duration as needed (e.g., 2 seconds)
        time.sleep(2)

except KeyboardInterrupt:
    print("\n🛑 Stopped capturing page sources.")

finally:
    driver.quit()
