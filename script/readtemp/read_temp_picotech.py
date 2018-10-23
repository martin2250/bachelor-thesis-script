#!/usr/bin/env python

import sys
import usb.core
import usb.util
import numpy as np

idVendor  = 0x1a86
idProduct = 0xe008
interface = 0

# find usb device
dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)

if dev is None:
    raise NameError('Device not found')

if dev.is_kernel_driver_active(interface) is True:
    print('Detaching kernel driver')
    dev.detach_kernel_driver(interface)
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
interface_number = cfg[(0,0)].bInterfaceNumber
alternate_setting = usb.control.get_interface(dev,interface_number)
intf = usb.util.find_descriptor(
    cfg, bInterfaceNumber = interface_number,
    bAlternateSetting = alternate_setting
)

ep = usb.util.find_descriptor(
    intf,
    # match the first IN endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN
)

assert ep is not None

# set 2400 baud (0x09, 0x60), 7 bits (0x02), see https://sigrok.org/wiki/WCH_CH9325
message = [0x09, 0x60, 0x00, 0x00, 0x02]
assert dev.ctrl_transfer(0x21, 9, 0x0300, 0, message)
print("Feature Report Sent")




(T, R) = np.loadtxt('calibration.dat', unpack=True)
sortindex = np.argsort(R)
T = T[sortindex]
R = R[sortindex]


def showFrame(frame):
    if len(frame) != 9:
        print(f"wrong frame length: {len(frame)} instead of 10")
        return

    frame = np.array([b & ( ~(1<<7) ) for b in frame])

    exponent = frame[0] - ord('0') - 1
    mantissa_data = frame[1:5] - ord('0')
    mantissa = np.sum(mantissa_data * np.array([1000, 100, 10, 1]))

    value = mantissa * 10**exponent
    temp = np.interp(value, R, T, -1, 999)

    print(f'Temperature: {temp:3.1f}K   {temp - 273.15:3.1f}°C \r', end='')





try:
    print("Start Reading Messages")

    buffer = []

    while True:
        answer = dev.read(ep.bEndpointAddress, ep.wMaxPacketSize, timeout=1000)

        if len(answer) != 8:
            raise NameError("Invalid report received (len != 8 bytes)")

        nbytes = answer[0] & 0x7
        if nbytes == 0:
            continue

        data = answer[1:nbytes+1]
        data = [b & ( ~(1<<7) ) for b in data]
        buffer += data

        for i in range(len(buffer)):
            if buffer[i] == ord('\n'):
                frame = buffer[0:i-1]   # i - 1 to remove preceding \r
                buffer = buffer[i+1:]
                showFrame(frame)

except KeyboardInterrupt:
    print("You pressed CTRL-C, stopping...")
