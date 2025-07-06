from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import PushRosNamespace

def generate_launch_description():
    pkg_ros_gz_sim = FindPackageShare('ros_gz_sim')
    pkg_surface = FindPackageShare('ashwin')
    gz_launch_path = PathJoinSubstitution([pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'])

    agents = [f'x500{i+1}' for i in range(3)]
    agent_launches = []

    for agent in agents:
        agent_launches.append(
            GroupAction([
                PushRosNamespace(agent),
                Node(
                    package='ros_gz_bridge',
                    executable='parameter_bridge',
                               
                     arguments=[
                         f'/world/multi_task_world/model/{agent}/model/x500/link/base_link/sensor/imu_sensor/imu@sensor_msgs/msg/Imu@gz.msgs.IMU',
            f'/model/{agent}/command/motor_speed@actuator_msgs/msg/Actuators@gz.msgs.Actuators',
                       ],
                    remappings=[
                        (f'/world/multi_task_world/model/{agent}/model/x500/link/base_link/sensor/imu_sensor/imu',
                        f'/{agent}/sensors/imu/data'),
                        (f'/model/{agent}/command/motor_speed',
                        f'/{agent}/command/motor_speed'),
                        ],
                    

                    output='screen'
                )
            ])
        )

    return LaunchDescription([
        SetEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH', PathJoinSubstitution([pkg_surface, 'models'])
        ),
        SetEnvironmentVariable(
            'GZ_SIM_PLUGIN_PATH', PathJoinSubstitution([pkg_surface, 'plugins'])
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch_path),
            launch_arguments={
                'gz_args': [PathJoinSubstitution([pkg_surface, 'worlds/multi_task_world.sdf'])],
                'on_exit_shutdown': 'True'
            }.items(),
        ),
    ] + agent_launches)

