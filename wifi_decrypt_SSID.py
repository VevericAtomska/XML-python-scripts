import binascii
import win32crypt

def decrypt_wifi_key(encrypted_key):
    try:
        encrypted_key_bytes = binascii.unhexlify(encrypted_key)
        decrypted_key_bytes = win32crypt.CryptUnprotectData(encrypted_key_bytes, None, None, None, 0)[1]
        return decrypted_key_bytes.decode('utf-8')
    except Exception as e:
        print(f"Error decrypting key: {e}")
        return "Error decrypting key"

wifi_data = "your_SSID_data_from_wifi"

wifi_profiles = []
for line in wifi_data.strip().split('\n'):
    if "SSID:" in line:
        ssid = line.split("SSID: ")[1].split(", Key: ")[0].strip()
        key = line.split(", Key: ")[1].strip()
        wifi_profiles.append({"SSID": ssid, "Key": key})

for profile in wifi_profiles:
    if profile["Key"] != "No key found":
        decrypted_key = decrypt_wifi_key(profile["Key"])
        print(f"SSID: {profile['SSID']}, Key: {decrypted_key}")
    else:
        print(f"SSID: {profile['SSID']}, Key: No key found")
