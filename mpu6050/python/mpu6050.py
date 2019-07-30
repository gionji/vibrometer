#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smbus2  # SMBus module of I2C

# Some MPU6050 Registers and their addresses
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
ACCEL_CONFIG = 0x1C
INT_ENABLE   = 0x38

ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40

GYRO_XOUT_H  = 0x43
GYRO_XOUT_L  = 0x44
GYRO_YOUT_H  = 0x45
GYRO_YOUT_L  = 0x46
GYRO_ZOUT_H  = 0x47
GYRO_ZOUT_L  = 0x48


class mpu6050:

	def __init__(self, bus_number=1, device_addr=0x68):

		self.bus = smbus2.SMBus(bus_number)
		self.device_addr = device_addr


	def mpu_init(self, sample_rate_div=7, gyro_config=24, accel_config=0):

		# Sample Rate = Gyroscope Output Rate / (1 + SMPLRT_DIV)
		# 	where Gyroscope Output Rate = 8kHz.
		# This would result in a Sample Rate of 1kHz
		self.bus.write_byte_data(self.device_addr, SMPLRT_DIV, sample_rate_div)

		# Disable sleep mode by writing into PWR_MGMT_1
		self.bus.write_byte_data(self.device_addr, PWR_MGMT_1, 1)

		# Write to Configuration register
		self.bus.write_byte_data(self.device_addr, CONFIG, 0)

		# Sets Gyroscope's full scale range (gyro_config=24 corresponds to ±2000°/s)
		self.bus.write_byte_data(self.device_addr, GYRO_CONFIG, gyro_config)

		# Sets Accelerometer's full scale range (accel_config=0 corresponds to ±2g)
		self.bus.write_byte_data(self.device_addr, ACCEL_CONFIG, accel_config)

		# Write to interrupt enable register
		self.bus.write_byte_data(self.device_addr, INT_ENABLE, 1)

		# Perform some washout readings to drop initial zero values
		self.read_data(n_samples=10)


	def mpu_init_acc_only(self):
		print('pippa')



	# Combines two 8-bits unsigned integers into a 16-bit signed integer
	def combine(self, high, low):

		# Combine the two 8-bits values
		value = ((high << 8) | low)
		# Get a signed value
		if (value > 32768):
			value = value - 65536
		return value


	def read_sample(self):

		# Read accelerometer data in bulk
		return self.bus.read_i2c_block_data(self.device_addr, ACCEL_XOUT_H, 6)


	def read_data(self, n_samples=1000):

		data = []
		# Read Accelerometer values
		for i in range(n_samples):
			row = self.read_sample()
			data.append(row)

		# Concatenate higher and lower values AND get signed values
		data = [[self.combine(x_h, x_l),
                 self.combine(y_h, y_l),
                 self.combine(z_h, z_l)] for (x_h, x_l, y_h, y_l, z_h, z_l) in data]

		return data
