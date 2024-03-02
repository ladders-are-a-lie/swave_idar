import lwsf45 as lw
import serial
import numpy as np
#--------------------------------------------------------------------------------------------------------------
# Main application.
#--------------------------------------------------------------------------------------------------------------
print('Running SF45/B LWNX Test.')

# Make a connection to the serial port.
# NOTE: You will need to change the port name and baud rate to match your connected SF45.
# Common Rapsberry Pi port name: /dev/ttyACM1
serial_port_name = 'COM3'
serial_port_baudrate = 921600
sensor_port = serial.Serial(serial_port_name, serial_port_baudrate, timeout = 0.1)

# Get sensor information.
lw.print_product_information(sensor_port)

# Configure the sensor.
# NOTE: See the set_update_rate function for values that can be used.
lw.set_update_rate(sensor_port, 1)
lw.set_default_distance_output(sensor_port)

# Start streaming distances.
lw.set_distance_stream_enable(sensor_port, True)
distances = []
yaw_angles = []

while True:
	distance, yaw_angle = lw.wait_for_reading(sensor_port)

	if distance != -1:
		distances.append(distance)
		yaw_angles.append(yaw_angle)
	else:
		distances.append(np.nan)
		yaw_angles.append(np.nan)

lidar_data = np.array([distances, yaw_angles])