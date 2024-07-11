import xml.etree.ElementTree as ET

xml_data = 'your_XML_data'

def print_xml_elements(element, level=0):
    indent = " " * (level * 2)
    print(f"{indent}Tag: {element.tag}, Attributes: {element.attrib}, Text: {element.text.strip() if element.text else ''}")
    for child in element:
        print_xml_elements(child, level + 1)

try:
    root = ET.fromstring(xml_data)
    print("Parsed XML successfully!")
    print_xml_elements(root)
except ET.ParseError as e:
    print(f"Error parsing XML: {e}")

