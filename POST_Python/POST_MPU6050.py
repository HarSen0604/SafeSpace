import smbus
import time

# MPU6050 registers and addresses
MPU6050_ADDR = 0x68
MPU6050_PWR_MGMT_1 = 0x6B
MPU6050_ACCEL_XOUT_H = 0x3B
MPU6050_ACCEL_YOUT_H = 0x3D
MPU6050_ACCEL_ZOUT_H = 0x3F
MPU6050_GYRO_XOUT_H = 0x43
MPU6050_GYRO_YOUT_H = 0x45
MPU6050_GYRO_ZOUT_H = 0x47

# Initialize I2C bus
bus = smbus.SMBus(1)

def MPU6050_init():
    # Wake up MPU6050
    bus.write_byte_data(MPU6050_ADDR, MPU6050_PWR_MGMT_1, 0)

def read_word(reg):
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg + 1)
    value = (high << 8) + low
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

def get_acceleration():
    x = read_word_2c(MPU6050_ACCEL_XOUT_H)
    y = read_word_2c(MPU6050_ACCEL_YOUT_H)
    z = read_word_2c(MPU6050_ACCEL_ZOUT_H)
    return x, y, z

def get_gyroscope():
    x = read_word_2c(MPU6050_GYRO_XOUT_H)
    y = read_word_2c(MPU6050_GYRO_YOUT_H)
    z = read_word_2c(MPU6050_GYRO_ZOUT_H)
    return x, y, z

if __name__ == "__main__":
    try:
        MPU6050_init()
        while True:
            accel_data = get_acceleration()
            gyro_data = get_gyroscope()
            print("Accelerometer: x={}, y={}, z={}".format(accel_data[0], accel_data[1], accel_data[2]))
            print("Gyroscope: x={}, y={}, z={}".format(gyro_data[0], gyro_data[1], gyro_data[2]))
            time.sleep(1)
    except KeyboardInterrupt:
        pass
