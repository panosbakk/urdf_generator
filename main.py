# main.py

import os
from robot_components import Link, RevoluteJoint
from robot_framework import Robot

# --- 1. Instantiate the Robot and Components ---
def create_robot_model():
    print("--- 1. Creating Robot Model (2-DOF Planar Arm) ---")
    
    # Initialize the Robot Container
    arm = Robot(name="Tesla_2DOF_Arm")

    # Define Links (Rigid Bodies)
    # mass, inertia_matrix (ixx, iyy, izz), center_of_mass
    base_link = Link("base_link", 10.0, [1.0, 1.0, 1.0], [0.0, 0.0, 0.0])
    link_1 = Link("link_1", 5.0, [0.5, 0.5, 0.5], [0.5, 0.0, 0.0])
    link_2 = Link("link_2", 3.0, [0.3, 0.3, 0.3], [0.4, 0.0, 0.0])

    # Define Joints (Connections and Movement)
    # RevoluteJoint(name, parent_link, child_link, axis, limits)
    joint_1 = RevoluteJoint(
        name="shoulder_joint",
        parent_link_name="base_link",
        child_link_name="link_1",
        axis=[0, 0, 1],      # Rotates around Z-axis
        limits=(-2.5, 2.5)   # +/- 2.5 radians
    )
    joint_2 = RevoluteJoint(
        name="elbow_joint",
        parent_link_name="link_1",
        child_link_name="link_2",
        axis=[0, 0, 1],
        limits=(-1.5, 1.5)
    )

    # Add components to the Robot framework
    arm.add_component(base_link)
    arm.add_component(link_1)
    arm.add_component(link_2)
    arm.add_component(joint_1)
    arm.add_component(joint_2)
    
    print(f"Model created: {arm.name} with {len(arm.components)} components.")
    return arm

# --- 2. Run Utility Functions ---
if __name__ == "__main__":
    robot_model = create_robot_model()
    
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # --- A. Data Serialization (Saving the model) ---
    json_path = os.path.join(output_dir, "robot_config.json")
    print(f"\n--- 2A. Saving Data Model to {json_path} ---")
    robot_model.save_to_json(json_path)
    print("Success: Model saved (demonstrates Data Modeling).")

    # --- B. URDF Generation (Creating the simulator file) ---
    urdf_path = os.path.join(output_dir, "tesla_arm.urdf")
    print(f"\n--- 2B. Generating URDF to {urdf_path} ---")
    robot_model.generate_urdf(urdf_path)
    print("Success: URDF generated (demonstrates Automation/Utility).")