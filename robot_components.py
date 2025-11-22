import json
import uuid
from abc import ABC, abstractmethod

class Component(ABC):

    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
    
    def to_dict(self) -> dict:
        data = {'id':self.id, 'name':self.name, 'type':self.__class__.__name__}
        return data

    @abstractmethod
    def get_urdf_tag(self) -> str:
        pass


class Link(Component):
    
    def __init__(self, name:str, mass:float, inertia_matrix:list, centermass:list):
        super().__init__(name)
        self.mass = mass
        self.inertia = inertia_matrix
        self.cm = centermass

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({'mass':self.mass, 'inertia':self.inertia, 'cm':self.cm})
        return data
    
    def get_urdf_tag(self) -> str:
        inertia_str = f"ixx='{self.inertia[0]}' iyy='{self.inertia[1]}' izz='{self.inertia[2]}'"
        return f""" 
<link name="{self.name}">
    <inertial>
        <mass value="{self.mass}"/>
        <origin xyz="{''.join(map(str, self.cm))}"/>
        <inertia {inertia_str}/>
    </inertial>
</link>
"""

class Joint(Component):

    def __init__(self, name:str, parent_link_name:str, child_link_name:str, axis:list):
        super().__init__(name)
        self.parent = parent_link_name
        self.child = child_link_name
        self.axis = axis
    
class RevoluteJoint(Joint):

    def __init__(self, name:str, parent_link_name:str, child_link_name:str, axis:list, limits:tuple):
        super().__init__(name, parent_link_name, child_link_name, axis)
        self.lower_limit = self.upper_limit = limits
    
    def get_urdf_tag(self) -> str:
        axis_str = ''.join(map(str, self.axis))
        return f""" 
<joint name="{self.name}" type="revolute">
    <parent link="{self.parent}" />
    <child link="{self.child}" />
    <axis xyz="{axis_str}" />
    <limit effort="100.0" velocity="10.0" lower="{self.lower_limit}" upper="{self.upper_limit}" />
</joint>
"""


    