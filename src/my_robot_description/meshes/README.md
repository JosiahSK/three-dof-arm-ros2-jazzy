# Meshes

Place your robot mesh files here (STL, DAE, OBJ).

Example naming:
- `base_link.stl`
- - `link1.stl`
  - - `link2.stl`
    - - `link3.stl`
      - - `gripper.stl`
       
        - Reference in URDF:
        - ```xml
          <mesh filename="package://my_robot_description/meshes/link1.stl"/>
          ```

          The current URDF uses primitives. Replace with meshes for a realistic appearance.
