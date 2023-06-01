# car_parking

Car_parking is a ROS package that simulates the [catvehicle](https://github.com/jmscslgroup/catvehicle) in a parallel parking scenario. It implements a parking finding algorithm using the vehicle's front laser scanner and also a navigation stack using the navfn global planner and the TEB local planner.

## Installation

1) Install the [catvehicle](https://github.com/jmscslgroup/catvehicle) and the car_parking packages to your workspace.

Go to your workspace folder:
```bash
cd src
git clone https://github.com/jmscslgroup/catvehicle
git clone https://github.com/jmscslgroup/obstaclestopper
git clone https://github.com/jmscslgroup/control_toolbox
git clone https://github.com/jmscslgroup/sicktoolbox
git clone https://github.com/jmscslgroup/sicktoolbox_wrapper
git clone https://github.com/jmscslgroup/stepvel
git clone https://github.com/jmscslgroup/cmdvel2gazebo
git clone https://github.com/boo555/car_parking
cd ..
catkin_make
```

## Usage

To initiate the simulation environment with the catvehicle model:
```bash
roslaunch car_parking parking_world.launch
```

To initiate the navigation stack and open the pre-built rviz configuration:
```bash
roslaunch car_parking navigation.launch
```

## Contributing

Pull requests are welcome. Future work may include alternative ways of parking space detection and pose estimation.

## License

[MIT](https://choosealicense.com/licenses/mit/)
