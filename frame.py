import serial
import time

Magic_code = {"AT+RDMETER=UL"     :"11",
              "AT+PERIOD=INTERVAL":"8A",
              "AT+ID=DevAddr"     :"84",
              "AT+RILINK=STAT"    :"63",
              "AT+RILINK=CFG"     :"F6"}#132

def GenerateAT(AT,number):
    # Mesage prepare
    Header     = "FEFE6820AAAAAAAAAAAAAA22"
    msg_len    = None
    padding    = "000000"
    msg        = AT
    msg_len    = str(len(msg)-3)
    hex_msg    = str(bytes(msg, "utf-8").hex()).upper()
    #check      = hex(number).lstrip("0x").upper().zfill(2)
    check      = Magic_code[AT]
    end        = "16"
    payload    = Header+msg_len+padding+hex_msg+check+end
    return payload

#AT+PERIOD=INTERVAL
#payload = GenerateAT("AT+PERIOD=INTERVAL")
#payload = GenerateAT("AT+RDMETER=UL")
#print(GenerateAT("AT+ID=DevAddr",1))
for key, value in Magic_code.items():
    print(key)
    print(GenerateAT(key,1))

"""
## Message sent into serial
port = "/dev/ttyUSB0"
baudrate = 2400
parity = "E"
timeout = 1  # Timeout in seconds

# Open the serial port
ser = serial.Serial(port, baudrate, parity=parity, timeout=timeout)


for i in range(1,256):
    payload = GenerateAT("AT+RILINK=CFG",i)

    # Convert payload string to bytes
    payload_bytes = bytes.fromhex(payload)

    # Send payload
    ser.write(payload_bytes)

    # Wait for response
    time.sleep(1)  # Adjust the delay if needed

    # Read response
    response_bytes = ser.read_all()

    if len(response_bytes) != 0:
        print("winner is : "+hex(i).upper())
        print("payload is : ")
        print(payload_bytes)
        # Print the response
        for byte in response_bytes:
            if byte < 32 or byte > 126:
                print(f" {byte:02X}", end=" ")  # Print as hexadecimal value
            else:
                print(chr(byte), end="")  # Print as ASCII character
        break
    else:
        print("we try : "+hex(i).upper())
    # Close the serial port



ser.close()
"""