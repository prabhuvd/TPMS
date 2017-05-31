"""
Created on May 10, 2017

Radio module is the most crucial module of the project.
The device can be configured for most of the configurations using serial(UART) interface.

The class is responsible for configuring the radio receiver and filtering the received data 
based on the 4byte(32 bit)  ID's of the sensor.

The ID's have to be read using a LF ( 125kHz) trigger tool or drive around your 
car with a compatible receiver and analyze the received data.  

@author: pdesai
"""
import serial
import time


class Radio:
    """ receiver port """
    __portInstance = 0
    ''' TPM sensor ID's and the corresponding temperature and pressure value.
    '   read_tpm_sensors() method reads the sensors , decodes the pressure and temperature 
    '   and stores into the dictionary.
    '''
    __sensor_ids = {"0d224bff": [00, 00],
                    "0d224bf4": [00, 00],
                    "0d2262b9": [00, 00],
                    "0d22622a": [00, 00]}
    ''' Turn on the receiver '''
    __receiver_on_cmd = ["03 20 30 01"]
    ''' Read the sensor '''
    __read_sensor_cmd = ["03 20 38 00"]

    '''
    ' ----------------------------------------------------
    ' Configuration is for MY2012 Mazda 5 sport
    ' ----------------------------------------------------
    '    Signal Parameters are:
    '    Baud Rate : 19200 chips/s
    '    Frequency Deviation : 35kHz
    '    Coding Style for run-in and data :  Manchester
    '    Modulation : FSK
    '    Channel Filter : 10000 Hz
    '    Intermediate Frequency : -20kHz
    '    Data Length :  10bytes
    '    Preamble : 0x0001
    '
    '
    '  The hard coded constants are the register values of NCK2983 for the above configuration. 
    '    
    '''
    
    __vehicle_rf_config = [
        "02 20 10",  # RC_CMD_RADIO_OFF
        "03 20 32 01",  # RC_CMD_RADIO_RX_DEFAULTS
        "0B 20 13 10 82 B9 06 00 48 04 16 03",  # RC_CMD_RADIO_LO_FREQUENCY
        "03 20 34 02",  # RC_CMD_RADIO_RX_INPUT
        "05 20 39 00 02 00",  # RC_CMD_RADIO_RX_DBG_CTRL
        "05 20 3F 01 07 07",  # RC_CMD_RADIO_RX_CONFIG_RSSI
        "21 20 3C 00 01 00 00 00 07 00 00 00 00 00 07 00 00 00 50 00 00 01 B6 46 66 00 00 05 02 03 01 01 01 01",
        # RC_CMD_RADIO_RX_DPROC_2
        "11 20 3B 00 62 B5 00 00 39 0E 31 01 00 00 05 00 00 01",  # RC_CMD_RADIO_RX_CONFIG_2
        "13 20 3D 00 00 E8 01 00 04 00 31 00 05 00 D7 03 00 00 00 0A",  # RC_CMD_RADIO_RX_CDREC_2
        "19 20 3E 00 DB 06 1F 00 40 C0 1F 00 1F 00 03 00 39 01 3A 08 03 00 34 01 05 08",  # RC_CMD_RADIO_RX_SM_2_NCK2983
        "03 20 30 01",  # RC_CMD_RADIO_RX_ON
        "03 20 38 00",  # RC_CMD_RADIO_RX_DATA
    ]

    def __init__(self, portnum, baud=115200):
        try:
            self.__portInstance = serial.Serial(portnum, baud, timeout=.01)
        except IOError as e:
            print (e)

    def close(self):
        self.__portInstance.close()

    @staticmethod
    def byte_to_hex(bytestr):
        """
        Convert a byte string to it's hex string representation e.g. for output.
        """
        # Uses list comprehension which is a fractionally faster implementation than
        # the alternative, more readable, implementation below
        #
        #    hex = []
        #    for aChar in bytestr:
        #        hex.append( "%02X " % ord( aChar ) )
        #
        #    return ''.join( hex ).strip()
        return ''.join(["%02X " % ord(x) for x in bytestr]).strip()

    @staticmethod
    def hex_to_byte(hexstr):
        """
        Convert a string hex byte values into a byte string. The Hex Byte values may
        or may not be space separated.
        """
        # The list comprehension implementation is fractionally slower in this case
        #
        #    hexstr = ''.join( hexstr.split(" ") )
        #    return ''.join( ["%c" % chr( int ( hexstr[i:i+2],16 ) ) \
        #                                   for i in range(0, len( hexstr ), 2) ] )

        dbytes = []
        hexstr = ''.join(hexstr.split(" "))

        for i in range(0, len(hexstr), 2):
            dbytes.append(chr(int(hexstr[i:i + 2], 16)))

        return ''.join(dbytes)

    # noinspection PyPep8Naming
    @staticmethod
    def get_temperature_F(msg):
        return int(msg[6], 16)

    # noinspection PyPep8Naming
    @staticmethod
    def get_pressure_PSI(msg):
        return int(msg[5], 16) * 0.2

    # noinspection PyPep8Naming
    @staticmethod
    def get_TPM_ID(msg):
        tpm_id = ""
        for id_byte in range(4):
            tpm_id = tpm_id + msg[id_byte]
        return tpm_id.lower()

    def write_command(self, command):
        # This flag will decided to Turn ON the receiver again.
        # print "send:",command
        if 0 == self.__portInstance.write(self.hex_to_byte(command)):
            print ("Write error : flushing I/O buffers")
            self.__portInstance.flushInput()
            self.__portInstance.flushOutput()
        # This delay is MUST after every command to Radio  
        time.sleep(.01)
        first_byte, rx_byte = self.read_cmd_response()
        return first_byte, rx_byte
    
    def read_cmd_response(self):
        # Reads one byte response which indicates the length of remaining  following bytes
        read_1_byte = self.byte_to_hex(self.__portInstance.read(1))
        read_byte_array = read_1_byte.split()

        # Check if there was at least one byte received.
        if len(read_byte_array) >= 1:
            # The first byte from the receiver indicates the length
            # of the following message
            rsp_length = int(read_byte_array[0], 16)
            rx_byte = self.byte_to_hex(self.__portInstance.read(rsp_length))
            return rsp_length, rx_byte
        else:
            return 0, 0

    def write_list_commands(self, cmdlist):
        for commands in range(len(cmdlist)):
            self.write_command(cmdlist[commands])

    def configure_device(self):
        self.write_list_commands(self.__vehicle_rf_config)

    def read_tpm_sensors(self):
        # This is a very crucual part of the interface with RF receiver.
        # Do not modify this without being fully aware of the protocol.
        first_byte, sensor_data = self.write_command(self.__read_sensor_cmd[0])
        rx_data = sensor_data.split()
        if first_byte > 6:
            # Ignore the return parameters , this is required to turn on 
            # the receiver after successful reception.
            self.write_command(self.__receiver_on_cmd[0])
            sensor_msg = rx_data[6:]
            if len(sensor_msg) > 6:
                extracted_id = self.get_TPM_ID(sensor_msg)
                # Filter the data and store only the values for learned ID's
                if self.get_TPM_ID(sensor_msg) in self.__sensor_ids:
                    self.__sensor_ids[extracted_id] = [self.get_pressure_PSI(sensor_msg),
                                                       self.get_temperature_F(sensor_msg)]

    def get_sensor_data(self):
        return self.__sensor_ids


__version = '0.1'