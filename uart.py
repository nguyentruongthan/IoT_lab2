import serial.tools.list_ports


#init Serial Communication object
ser = serial.Serial(port = "COM7", baudrate=115200)
print(ser)

def processData(data, client):
    #parameter client is object of MQTT Client

    #replace charactor ! and # at start and end of data
    data = data.replace("!", "")
    data = data.replace("#", "")
    #spilit data to array with spilt charactor is ":" 
    splitData = data.split(":")
    print(splitData)

    #send data to server Adafruit
    if splitData[1] == "TEMP":
      #publish temperature to cambien1 in Adafruit
      client.publish("cambien1", splitData[2])
    elif splitData[1] == "HUMI":
      #publish humidity to cambien3 in Adafruit
      client.publish("cambien3", splitData[2])

mess = ""
def readSerial(client):
    #	Get the number of bytes in the input buffer
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        #read all data in serial and assign to mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        #Format of data is "!<content>#" 
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1], client)
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

