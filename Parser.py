class STX:
    def __init__(self,ByteValue):
        self.D0 = bool(ByteValue & 0b00000001)
        self.D1 = bool(ByteValue & 0b00000010)
        self.D2 = bool(ByteValue & 0b00000100)
        self.D3 = bool(ByteValue & 0b00001000)
        self.D4 = bool(ByteValue & 0b00010000)
        self.D5 = bool(ByteValue & 0b00100000)
        self.D6 = bool(ByteValue & 0b01000000)
        self.D7 = bool(ByteValue & 0b10000000)
     
    def print_values(self):
        attributes = vars(self)
        result = ""
        for attr_name, attr_value in attributes.items():
            if isinstance(attr_value, bool) and attr_value and not attr_name.startswith('D'):
                result += f"{attr_name}, "
        return result
        
class ST1(STX):
    def __init__(self,ByteValue):
        super().__init__(ByteValue)
        self.Leakage_Alarm  = self.D2
        self.Burst_Alarm    = self.D3
        self.Tamper_Alarm   = self.D4
        self.Freezing_Alarm = self.D5
        
    def trigger(self):
        child_attributes = [attr_name for attr_name in vars(self) if not attr_name.startswith('D')]
        return any(getattr(self, attr_name) for attr_name in child_attributes if isinstance(getattr(self, attr_name), bool))
        
class ST2(STX):
    def __init__(self,bytevalue):
        super().__init__(bytevalue)
        self.Meter_Battery_Alarm = self.D0
        self.Empty_Pipe_Alarm    = self.D1
        self.Reverse_Flow_Alarm  = self.D2
        self.Over_Range_Alarm    = self.D3
        self.Temperature_Alarm   = self.D4
        self.EE_Error            = self.D5
        self.Transduce_IN_Error  = self.D6
        self.Transduce_OUT_Error = self.D7
    def trigger(self):
        attributes = vars(self)
        return any(isinstance(attr_value, bool) and attr_value for attr_value in attributes.values())

class DataParser:
    def __init__(self, data):
        self.data = data
        self.parse()

    def parse(self):
        # Split the input data into chunks
        data_chunks = [self.data[i:i+2] for i in range(0, len(self.data), 2)]

        # Assign the chunks to the respective attributes
        self.control_code = data_chunks[0]
        self.data_length  = data_chunks[1]
        self.data_identification = data_chunks[2:4]
        self.count_number        = data_chunks[4]
        self.unit                = data_chunks[5]

        # Reorder the priority bit string
        priority_bit_string = data_chunks[6:10]
        self.priority_bit = [priority_bit_string[i] for i in [3, 2, 1, 0]]
        units = {"2B": 0.001, "2C": 0.01, "2D": 0.1, "2E": 1, "35": 0.0001}
        
        self.totalCurrent = int(''.join(self.priority_bit[:3]))*units[self.unit]*100000

        self.ST1 = ST1(int(data_chunks[10],16))
        self.ST2 = ST2(int(data_chunks[11],16))
        self.battery = data_chunks[12]
        

    def print_values(self):
        print(f'Control code: {self.control_code}')
        print(f'Data length: {self.data_length}')
        print(f'Data identification: {self.data_identification}')
        print(f'Count number: {self.count_number}')
        print(f'Unit: {self.unit}')
        print(f'Priority bit: {self.priority_bit}')
        print(f'Total flow: {self.totalCurrent} L')
        print(f'ST1: {self.ST1.print_values()}')
        print(f'ST2: {self.ST2.print_values()}')
        print(f'Battery: {self.battery}')

#sample_data = "810A901F002B0010050000027F"
#parser = DataParser(sample_data)
#parser.print_values()