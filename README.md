## PD Control Project

In this project, we implemented a position controller (PD) for the 3 robot joints. We were receiving joint values from the Gazebo simulator. We received a reference value for the joints through a service, and
we publish appropriately joint efforts (continuously with high sampling rates) to make the joints move so that we achieve the reference value.

1. Launch the Joint Control Node using:

    ```bash
    colcon build
    ```

   ```bash
   ros2 run rrbot_gazebo service_member_function
   ```

   The control strategy used is PD Control. 

   $$u = -K_{p}*e - K_{d}\dot{e}$$

   where:

   - $e$ is position error: $e = \theta_{r} - \theta$
   - $\dot{e}$ is rate of change of error: $\dot{e} = \frac{e_{t}-e_{t-\delta{t}}}{\delta{t}}$

2. Call the Joint Control service using:

   ```bash
   ros2 service call /joint_state_controller tutoral_interfaces/srv/FirstService '{x: 1, y: 2, z: 2}'
   ```
   Here x,y,z denote the joint angles/states

   Change the Joint States by trying different values for (x,y,z)
3. Results


