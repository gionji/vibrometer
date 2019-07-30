#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mpu6050 import mpu6050

import numpy as np
import argparse
import sys
import time

arg_parser = argparse.ArgumentParser(sys.argv[0])
arg_parser.add_argument('-n', '--num-samples', dest='num_samples', required=False, default=1000, help='Number of samples to collect.', type=int)
arg_parser.add_argument('-c', '--accel-config', dest='accel_config', required=False, default=0, help='Check MPU6050\'s documentation.', type=int)
arg_parser.add_argument('-b', '--i2c-bus', dest='i2c_bus', required=True, help='I2C bus where the accelerometer is connected.', type=int)
arg_parser.add_argument('-f', '--dest-file', dest='dest_file', required=False, help='File where accelerometer data will be saved.', type=str)
arg_parser.add_argument('-d', '--device-addr', dest='device_addr', required=False, default = '0x68', help='MPU6050 i2c address / default 0x68', type=str)
arg_parser.add_argument('-p', '--print-data', dest='print_data', default=False, help='Print data', action='store_true')

# Parse command line arguments
args = arg_parser.parse_args()
n_samples = args.num_samples
accel_config = args.accel_config
i2c_bus = args.i2c_bus
dest_file = args.dest_file
device_addr = int(args.device_addr, 16)
print_data = args.print_data

print( args )

print( 'Se ti facesse tutti zeri va fatto l enable a mano per qualche motivo: i2cset -y 1 0x68 0x6b 1' )

# Initialize the MPU6050
mpu = mpu6050(bus_number=i2c_bus, device_addr=0x68)

print('Reading accelerometer data...')

startTime = time.time()
data = mpu.read_data(n_samples=n_samples)
endTime = time.time()

print('Execution time for ' + str(n_samples) + ': ', (endTime - startTime), len(data))
print('Effective frequency: ', int(1/((endTime - startTime) / n_samples)) , ' Hz') 

if(print_data):
	print( data )

data = np.asarray(data).reshape((-1, 3))

fft = np.fft.fft(data)

print(fft)


