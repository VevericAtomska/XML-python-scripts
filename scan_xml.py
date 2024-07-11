import xml.etree.ElementTree as ET

xml_data = 'your_XML_data'

def decrypt_wifi_key(encrypted_key):
    try:
        encrypted_key_bytes = b64decode(encrypted_key)
        decrypted_key_bytes = win32crypt.CryptUnprotectData(encrypted_key_bytes, None, None, None, 0)[1]
        return decrypted_key_bytes.decode('utf-8')
    except Exception as e:
        print(f"Error decrypting key: {e}")
        return "Error decrypting key"

def parse_wifi_policy(xml_data):
    namespaces = {
        'gpo': 'http://www.microsoft.com/GroupPolicy/Settings',
        'types': 'http://www.microsoft.com/GroupPolicy/Types',
        'sec': 'http://www.microsoft.com/GroupPolicy/Types/Security',
        'wl': 'http://www.microsoft.com/networking/WLAN/policy/v1'
    }

    root = ET.fromstring(xml_data)
    profiles = []

    for profile in root.findall('.//wl:WLANProfile', namespaces):
        ssid = profile.find('.//wl:SSID/wl:name', namespaces).text
        encrypted_key = profile.find('.//wl:keyMaterial', namespaces)
        if encrypted_key is not None:
            encrypted_key_text = encrypted_key.text
            decrypted_key = decrypt_wifi_key(encrypted_key_text)
        else:
            decrypted_key = 'No key found'

        profiles.append({'SSID': ssid, 'Key': decrypted_key})

    return profiles

profiles = parse_wifi_policy(xml_data)

for profile in profiles:
    print(f"SSID: {profile['SSID']}, Key: {profile['Key']}")