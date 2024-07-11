import xml.etree.ElementTree as ET


xml_data = 'your_xml_data'

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
        profiles.append({'SSID': ssid})

    return profiles

profiles = parse_wifi_policy(xml_data)

for profile in profiles:
    print(f"SSID: {profile['SSID']}")
