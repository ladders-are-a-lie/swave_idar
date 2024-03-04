import sqlite3
import time
import lwsf45 as lw
import serial
import numpy as np

class Lidar_DB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.path = db_name

    def create_lidar_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lidar_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER,
                time REAL,
                distance REAL,
                yaw_angle REAL
            )
        ''')
        self.conn.commit()


    def insert_lidar_data(self, run_id, time, distance, yaw_angle):
        self.cursor.execute('''
                            INSERT INTO lidar_data (run_id, time, distance, yaw_angle) 
                            VALUES (?, ?, ?, ?)''',
                            (run_id, time, distance, yaw_angle))
        self.conn.commit()


    def get_all_lidar_data(self):
        self.cursor.execute("SELECT * FROM lidar_data")
        return self.cursor.fetchall()
    
    def get_column(self, column, table, run):
        query = "SELECT {}, time FROM {} WHERE run_id = {}".format(column, table, run)
        self.cursor.execute(query)
        column_data = self.cursor.fetchall()
        return column_data
    
    def get_current_data(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor.execute("SELECT * FROM lidar_data ORDER BY id DESC LIMIT 1")
        return self.cursor.fetchall()
    
    def query_run(self):
        run_imu = None
        run_odrive = None

        self.cursor.execute("SELECT run_id FROM lidar_data ORDER BY run_id DESC LIMIT 1")
        run_lidar = self.cursor.fetchone()

        if run_lidar:
            run_lidar = run_lidar[0]
            return run_lidar
        else:
            return 0

    def open_connection(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()



# if __name__ == "__main__":
    
#     print("Starting...")

#     serial_port_name = 'COM3'
#     serial_port_baudrate = 921600
#     sensor_port = serial.Serial(serial_port_name, serial_port_baudrate, timeout = 0.1)
#     lw.set_update_rate(sensor_port, 1)
#     lw.set_default_distance_output(sensor_port)
#     lw.set_distance_stream_enable(sensor_port, True)

#     db = Lidar_DB("lidar_data.db")
#     db.open_connection()
#     db.create_lidar_table()
#     run_id = db.query_run() + 1
    
#     print("run {}".format(run_id))

#     while True:
#         try:
#             db.open_connection()
#             distance, yaw_angle = lw.wait_for_reading(sensor_port)
            
#             if distance != -1:
#                 db.insert_lidar_data(run_id, time.time(), distance, yaw_angle)
#                 print('time: {} Distance: {} m, Yaw Angle: {} deg'.format(time.time(), distance, yaw_angle))
#             else:
#                 db.insert_lidar_data(run_id, time.time(), np.nan, np.nan)
#                 print('time: {} Distance: {} m, Yaw Angle: {} deg'.format(time.time(), distance, yaw_angle))
        
#         except KeyboardInterrupt:
#             db.close_connection()
#             break

