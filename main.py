import lwsf45 as lw
import serial
import numpy as np
import time
from lidar_db import Lidar_DB

#--------------------------------------------------------------------------------------------------------------
# Main application.
#--------------------------------------------------------------------------------------------------------------
print('Running SF45/B LWNX Test.')

print("Starting...")

serial_port_name = 'COM3'
serial_port_baudrate = 921600
sensor_port = serial.Serial(serial_port_name, serial_port_baudrate, timeout = 0.1)
lw.set_update_rate(sensor_port, 1)
lw.set_default_distance_output(sensor_port)
lw.set_distance_stream_enable(sensor_port, True)
    
db = Lidar_DB("lidar_data.db")
db.open_connection()
db.create_lidar_table()
run_id = db.query_run() + 1
    
print("run {}".format(run_id))

while True:
    try:
        db.open_connection()
        distance, yaw_angle = lw.wait_for_reading(sensor_port)
            
        if distance != -1:
            db.insert_lidar_data(run_id, time.time(), distance, yaw_angle)
            print('time: {} Distance: {} m, Yaw Angle: {} deg'.format(time.time(), distance, yaw_angle))
        else:
            db.insert_lidar_data(run_id, time.time(), np.nan, np.nan)
            print('time: {} Distance: {} m, Yaw Angle: {} deg'.format(time.time(), distance, yaw_angle))
        
    except KeyboardInterrupt:
        db.close_connection()
        break