from devicecloud import DeviceCloud


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
        # we are retrieving list of streams in device cloud for our credential
        if self.is_connect():
            print "List of streams:"
            for stream in self.dc.streams.get_streams():
                print "%s " % (stream.get_stream_id())
        else:
            print "You are not connected"

    def set_stream(self, stream_id):
        # we 're trying to set stream, if not correct we send about it
        if self.dc.streams.get_stream_if_exists(stream_id):
            self.current_stream = stream_id
            print "Set current stream: %s" % (stream_id)
        else:
            print "There not stream with such stream_id: %s" % (stream_id)

    def get_stream(self):
        # get username information about current connection
        return self.current_stream

    def get_stream_metadata(self, use_cached=True):
        # get metadata about current stream
        if self.current_stream is not None:
            return self.dc.streams.get_stream(self.current_stream)._get_stream_metadata(use_cached)

    def get_data_type(self, use_cached=True):
        #  get information about dataType of current stream
        dtype = self.get_stream_metadata(use_cached).get("dataType")
        if dtype is not None:
            dtype = dtype.upper()
        return dtype

    def get_units(self, use_cached=True):
        # get information about units of current stream
        return self.get_stream_metadata(use_cached).get("units")

    def get_description(self, use_cached=True):
        # get information about units of current stream
        return self.get_stream_metadata(use_cached).get("description")

    def get_data_ttl(self, use_cached=True):
        # get information about time-to-live of current stream
        data_ttl_text = self.get_stream_metadata(use_cached).get("dataTtl")
        return int(data_ttl_text)

    def get_rollup_ttl(self, use_cached=True):
        # get information about time-to-live roll-up aggregate data in the stream
        rollup_ttl_text = self.get_stream_metadata(use_cached).get("rollupTtl")
        return int(rollup_ttl_text)

    def get_current_value(self, use_cached=False):
        # get last written data point for current stream
        from devicecloud.streams import DataPoint
        current_value = self.get_stream_metadata(use_cached).get("currentValue")
        if current_value:
            return DataPoint.from_json(self.dc.streams.get_stream(self.current_stream), current_value)
        else:
            return None

    def get_datapoints(self):
        # we are retrieving list of streams in device cloud for our credential
        if self.current_stream is not None:
            raw_data_from_devicecloud = list(self.dc.streams.get_stream(self.current_stream).read())
            for datapoint in raw_data_from_devicecloud:
                print datapoint

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
# trying to set incorrect stream
dsc.set_stream("classroom1")
# trying to set correct stream
dsc.set_stream("classroom")
print
print "Data type of the stream: ", dsc.get_data_type()
print "Units of the stream: ",dsc.get_units()
print "Description of the stream: ", dsc.get_description()
print "Data TTL of the stream", dsc.get_data_ttl()
print "Rollup TTL of the stream", dsc.get_rollup_ttl()
print "Last written data point in the stream: ", dsc.get_current_value()
print
dsc.get_datapoints()
dsc.set_stream("00000000-00000000-00409DFF-FF521DB2/freeMemory")
print
print "Data type of the stream: ", dsc.get_data_type()
print "Units of the stream: ",dsc.get_units()
print "Description of the stream: ", dsc.get_description()
print "Data TTL of the stream", dsc.get_data_ttl()
print "Rollup TTL of the stream", dsc.get_rollup_ttl()
print "Last written data point in the stream: ", dsc.get_current_value()
print
dsc.get_datapoints()