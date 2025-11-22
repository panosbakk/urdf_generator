import json
import xml.etree.ElementTree as ET
from robot_components import Component, Link, RevoluteJoint, Joint

class Robot:

    def __init__(self, name: str):
        self.name = name
        self.components = {}

    def add_component(self, component: Component):
        self.components[component.name] = component

    def get_component(self, name: str) -> Component:
        return self.components.get(name)
    
    def save_to_json(self, filepath: str):
        data = {
            'robot_name': self.name,
            'components': [comp.to_dict() for comp in self.components.values()]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    
    def generate_urdf(self, filepath:str) -> str:
        robot_tag = ET.Element('robot', name=self.name)
        for component in self.components.values():
            if isinstance(component, (Link, Joint)):
                try:
                    xml_str = component.get_urdf_tag()
                    robot_tag.append(ET.fromstring(xml_str.strip()))
                except NotImplementedError:
                    print(f"Warning: URDF tag not implemented for {component.name}")
        from xml.dom import minidom
        xml_str = minidom.parseString(ET.tostring(robot_tag)).toprettyxml(indent="   ")
        with open(filepath, 'w') as f:
            f.write(xml_str)