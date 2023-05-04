 Before adding this package to your workspace, add the catvehicle package with its dependencies.
 
 Steps to run the car parking algorithm:
 1) Initiate the simulation with the model:
 roslaunch car_parking parking_world.launch
 
 2) Initiate the navigation stack and open rviz pre-built configuration:
 roslaunch car_parking navigation.launch
 
 3) Run the algorithm:
 rosrun car_parking find_parking.py
