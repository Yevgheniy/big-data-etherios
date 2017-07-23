from devicecloud import DeviceCloud
import pprint


class DataStreamConnect():
    """Our own class to connect and retrieve data from device cloud
    we 're using devicecloud package
    """

    def __init__(self):
        self.dc = None
        self.connection = False
        self._cached_data = None
        self.current_user = None
        self.current_device = None
        self.current_stream = None
        self.current_datapoint = None

    def __repr__(self):
        # Provide a repr.  We want to avoid making an HTTP request here as that
        # might not be desirable
        # return ("DataStream(stream_id={stream_id!r}, "
        #             "data_type={data_type!r}, "
        #             "units={units!r}, "
        #             "description={description!r}, "
        #             "data_ttl={data_ttl!r}, "
        #             "rollup_ttl={rollup_ttl!r})".format(
        #     stream_id=self.get_stream_id(),
        #     data_type=self.get_data_type(),
        #     units=self.get_units(),
        #     description=self.get_description(),
        #     data_ttl=self.get_data_ttl(),
        #     rollup_ttl=self.get_rollup_ttl(),
        #     ))
        pass

    def connect(self,username, password):
        # first we need to connect to device cloud
        # if we "re connected first drop connect and try to connect again
        if self.connect:
            self.dc = None
        self.dc = DeviceCloud(username,password)
        if self.dc.has_valid_credentials():
            self.current_user = username
            self.connection = True
        else:
            self.dc = None
            self.current_user = None
            self.connection = False

    def is_connect(self):
        # we need to check current connection to devicecloud
        return self.connection

    def get_username(self):
        # get username information about current connection
        return self.current_user

    def get_devices(self):
        # we are retrieving list of devices in device cloud for our credential
        if self.is_connect():
            print "List of devices:"
            for device in self.dc.devicecore.get_devices():
                print "%s " % (device.get_connectware_id())
        else:
            print "You are not connected"

    def get_streams(self):
        if self.is_connect():
            print "List of streams:"
            for stream in self.dc.streams.get_streams():
                print "%s " % (stream.get_stream_id())
        else:
            print "You are not connected"

    def set_stream(self, stream_id):

        if self.dc.streams.get_stream_if_exists(stream_id)
        pass

    def get_stream(self):
        pass

    def get_datapoints(self):
        pass

# create instance of our class and retrive initial info
dsc = DataStreamConnect()
print "We are connecting? - ", dsc.is_connect()
print "What is username credential of current connection? - ", dsc.get_username()
print

# trying to connect to device cloud with wrong credentials
username = "11nanri-test" # enter your username
password = "!Nanri0118" # enter your password
dsc.connect(username,password)
# retrieving information about connection
print "We are connecting? - ", dsc.is_connect()
print "What is username credential of current connection? - ", dsc.get_username()
dsc.get_devices()
print

# trying to connect to device cloud with our right credentials
username = "nanri-test" # enter your username
password = "!Nanri0118" # enter your password
dsc.connect(username,password)
# retrieving information about connection
print "We are connecting? - ", dsc.is_connect()
print "What is username credential of current connection? - ", dsc.get_username()
# retrieving information about devices in device cloud for our credential:
dsc.get_devices()
print
# retrieving information about existing streams in device cloud for our credential:
dsc.get_streams()
print
