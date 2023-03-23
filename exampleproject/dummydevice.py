import numpy as np

class Device:
    def getData(self):
        return np.random.uniform(0,5,10).astype(int)
    
    def close(self):
        pass

if __name__ == "__main__":
    dev = Device()
    print(dev.getData())
