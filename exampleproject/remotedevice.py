import numpy as np
# PyUSB
import usb.core
import usb.util

class Device:
    def __init__(self):
        # lsusb gives information on vendor and product ids: 0bc7:0006
        self.device = usb.core.find(idVendor=0x0bc7, idProduct=0x0006)
        
        if self.device.get_active_configuration() is None:
            self.device.set_configuration()
        
        self.device.detach_kernel_driver(0)
        
        self.parity = None
    
    def getData(self):
        binned_response = [0]*10
        try:
            while True:
                response = self.read(0x81,4,10)
                    
                assert response[0] == 0x14
                
                if not (response[2] & 0b10000000):
                    if self.parity is not None and self.parity:
                        continue
                    self.parity = True
                else:
                    if self.parity is not None and not self.parity:
                        continue
                    self.parity = False
                
                assert response[3] == 0x00
                
                _id = response[2] & 0b01111111
                
                if _id >= 13 and _id <= 21:
                    binned_response[_id-12] += 1
                if _id == 23:
                    binned_response[0] += 1
        except usb.core.USBError as e:
            return np.array(binned_response)
    
    def close(self):
        usb.util.dispose_resources(self.device) # Ensure that device is not in use
        self.device.attach_kernel_driver(0) # Attach Kernel driver again

if __name__ == "__main__":
    dev = Device()
    print(dev.getData())
