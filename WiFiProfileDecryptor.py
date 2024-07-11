import os
import xml.etree.ElementTree as ET
from base64 import b64decode
from dpapick3.dpapi import MasterKey, MasterKeyFile, PVKFile
 

directory = "C:\\Users\\User"
 
def decrypt_wifi_key(encrypted_key):
    try:
        encrypted_key_bytes = b64decode(encrypted_key)
        masterkey_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Protect', os.getenv('USERPROFILE').split('\\')[-1])
        masterkey_file = MasterKeyFile.from_directory(masterkey_path)
        for masterkey in masterkey_file.masterkeys:
            if masterkey.decrypt(encrypted_key_bytes):
                return masterkey.decrypt(encrypted_key_bytes).decode('utf-8')
        return "No suitable masterkey found"
    except Exception as e:
        print(f"Error decrypting key: {e}")
        return "Error decrypting key"
 
def parse_wifi_profile(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespace = {'ns': 'http://www.microsoft.com/networking/WLAN/profile/v1'}
   
    ssid = root.find("ns:SSIDConfig/ns:SSID/ns:name", namespace)
    ssid_text = ssid.text if ssid is not None else "No SSID found"
    
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