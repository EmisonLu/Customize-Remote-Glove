import serial


class Port:
    def __init__(self, com, baud=19200, time_out=0.2):
        self.ser = serial.Serial(com, baud, timeout=time_out)

    def expandData(self, string):
        for i in range(5,11):
            if string[i] == "0" or string[i] == "1":
                string += "0"
            else:
                string[i] = "0"
                string += "1"
        return string

    def getData(self):
        str_data = self.ser.readline()

        # str_data = str_data.decode()
        str_data = str(str_data, encoding="utf8")
        str_data = str_data.rstrip()
        # print(str_data + str(len(str_data)))
        if len(str_data) != 11:
            return ""
        return str_data

    def flush(self):
        self.ser.flushInput()


