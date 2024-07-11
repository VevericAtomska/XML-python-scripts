import os
import xml.etree.ElementTree as ET
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import base64
import win32crypt
 

directory = "C:\\Users\\User"
 
def decrypt_wifi_key(encrypted_key):
    
    try:
        encrypted_key_bytes = base64.b64decode(encrypted_key)
    except Exception as e:
        print(f"Error decoding base64: {e}")
        return "Error decoding base64"
 
    
    try:
        decrypted_key_bytes = win32crypt.CryptUnprotectData(encrypted_key_bytes, None, None, None, 0)[1]
        return decrypted_key_bytes.decode('utf-8')
    except Exception as e:
        print(f"Error decrypting key: {e}")
        return "Error decrypting key"
 
def parse_wifi_profile(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespace = {'ns': 'http://www.microsoft.com/networking/WLAN/profile/v1'}
    # Pronađi SSID ime
    ssid = root.find("ns:SSIDConfig/ns:SSID/ns:name", namespace)
    ssid_text = ssid.text if ssid is not None else "No SSID found"
    # Pronađi Wi-Fi ključ
    key = root.find("ns:MSM/ns:security/ns:sharedKey/ns:keyMaterial", namespace)
    key_text = "No key found"
    if key is not None:
        try:
            key_text = decrypt_wifi_key(key.text)
        except Exception as e:
            key_text = f"Error: {e}"
 
    return ssid_text, key_text
 

for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        file_path = os.path.join(directory, filename)
        ssid, key = parse_wifi_profile(file_path)
        print(f"SSID: {ssid}, Key: {key}")