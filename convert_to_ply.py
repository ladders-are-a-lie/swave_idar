
import os
import sqlite3
import numpy as np

class Lidar_DB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.path = db_name

    def get_all_lidar_data(self, run_id=None):
        if run_id is not None:
            self.cursor.execute("SELECT time, distance, yaw_angle FROM lidar_data WHERE run_id = ?", (run_id,))
        else:
            self.cursor.execute("SELECT time, distance, yaw_angle FROM lidar_data")
        return self.cursor.fetchall()

    def open_connection(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

def polar_to_cartesian(distance, yaw_angle):
    rad = np.deg2rad(yaw_angle)
    x = distance * np.cos(rad)
    y = distance * np.sin(rad)
    return x, y

def write_ply(filename, points):
    with open(filename, 'w') as file:
        file.write("ply\n")
        file.write("format ascii 1.0\n")
        file.write(f"element vertex {len(points)}\n")
        file.write("property float x\n")
        file.write("property float y\n")
        file.write("end_header\n")
        for time_stamp, x, y in points:
           #file.write(f"comment Time: {time_stamp}\n") 
           file.write(f"{x} {y}\n") 
def main():
    db = Lidar_DB("lidar_data.db")
    db.open_connection()

    # Fetch data for a specific run_id
    run_id = input("Enter run ID to convert, or press enter to convert all data: ").strip()
    run_id = int(run_id) if run_id else None

    lidar_data = db.get_all_lidar_data(run_id)
    points = [(time_stamp, *polar_to_cartesian(distance, yaw_angle)) for time_stamp, distance, yaw_angle in lidar_data if distance is not None]

    db.close_connection()

    # Define the directory where PLY files will be saved
    save_directory = os.path.expanduser("~/lidar/lidar_ply_data")
    os.makedirs(save_directory, exist_ok=True)  # Create the directory if it doesn't exist

    # Update ply_filename to include the run_id and save in the specific directory
    ply_filename_suffix = f"_run_{run_id}" if run_id is not None else "_all_runs"
    ply_filename = os.path.join(save_directory, f'lidar_data{ply_filename_suffix}.ply')
   
    write_ply(ply_filename, points)
    print(f"Converted {len(points)} points to PLY format in '{ply_filename}'.")

if __name__ == "__main__":
    main()

