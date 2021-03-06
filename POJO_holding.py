from DataStreamConnect import DataStreamConnect
import six
import json
from devicecloud.util import to_none_or_dt, validate_type

#  a lot of code I copypasted from DeviceCloud
STREAM_TYPE_INTEGER = "INTEGER"
STREAM_TYPE_LONG = "LONG"
STREAM_TYPE_FLOAT = "FLOAT"
STREAM_TYPE_DOUBLE = "DOUBLE"
STREAM_TYPE_STRING = "STRING"
STREAM_TYPE_BINARY = "BINARY"
STREAM_TYPE_JSON = "JSON"
STREAM_TYPE_UNKNOWN = "UNKNOWN"

# Mapping in the following form:
# <dc-type> -> (<dc-to-python-fn>, <python-to-dc-fn>)
DSTREAM_TYPE_MAP = {
    STREAM_TYPE_INTEGER: (int, str),
    STREAM_TYPE_LONG: (int, str),
    STREAM_TYPE_FLOAT: (float, str),
    STREAM_TYPE_DOUBLE: (float, str),
    STREAM_TYPE_STRING: (str, str),
    STREAM_TYPE_BINARY: (str, str),
    STREAM_TYPE_UNKNOWN: (str, str),
    STREAM_TYPE_JSON: (json.loads, json.dumps)
}

class POJO_holding:
    """Our own class, which get and store information from DeviceCloud stream"""
    def __init__(self, data=None, stream_id=None, description=None, timestamp=None,
                 quality=None, location=None, data_type=None, units=None, dp_id=None,
                 customer_id=None, server_timestamp=None):
        self._stream_id = None  # invariant: always string or None
        self._data = None  # invariant: could be any type, with conversion applied lazily
        self._description = None  # invariant: always string or None
        self._timestamp = None  # invariant: always datetime object or None
        self._quality = None  # invariant: always integer (32-bit) or None
        self._location = None  # invariant: 3-tuple<float> or None
        self._data_type = None  # invariant: always string in set of types or None
        self._units = None  # invariant: always string or None
        self._dp_id = None  # invariant: always string or None
        self._customer_id = None  # invariant: always string or None
        self._server_timestamp = None  # invariant: always None or datetime

    def get_id(self):
        """Get the ID of this data point if available
        This ID only for existing data points, so we cant create(set) ourself this ID.
        """
        return self._dp_id

    def set_id(self, dp_id):
        """It's only for existing data points"""
        self._dp_id = dp_id

    def get_data(self):
        """Get the actual data value associated with this data point"""
        return self._data

    def set_data(self, data):
        """Set the data for this data point
        This data may be converted upon access at a later point in time based
        on the data type of this stream (if set).
        """
        self._data = data

    def get_stream_id(self):
        """Get the stream ID for this data point if available"""
        return self._stream_id

    def set_stream_id(self, stream_id):
        """Set the stream id associated with this data point"""
        stream_id = validate_type(stream_id, type(None), *six.string_types)
        if stream_id is not None:
            stream_id = stream_id.lstrip('/')
        self._stream_id = stream_id

    def get_description(self):
        """Get the description associated with this data point if available"""
        return self._description

    def set_description(self, description):
        """Set the description for this data point"""
        self._description = validate_type(description, type(None), *six.string_types)

    def get_timestamp(self):
        """Get the timestamp of this datapoint as a :class:`datetime.datetime` object
        This is the client assigned timestamp for this datapoint.  If this was not
        set by the client, it will be the same as the server timestamp.
        """
        return self._timestamp

    def set_timestamp(self, timestamp):
        """Set the timestamp for this data point
        The provided value should be either None, a datetime.datetime object, or a
        string with either ISO8601 or unix timestamp form.
        """
        self._timestamp = to_none_or_dt(timestamp)

    def get_server_timestamp(self):
        """Get the date and time at which the server received this data point"""
        return self._server_timestamp

    def set_server_timestamp(self, server_timestamp):
        """set server timestamp from DataPoint object"""
        self._server_timestamp = to_none_or_dt(server_timestamp)


    def get_quality(self):
        """Get the quality as an integer
        This is a user-defined value whose meaning (if any) could vary per stream.  May
        not always be set.
        """
        return self._quality

    def set_quality(self, quality):
        """Set the quality for this sample
        Quality is stored on the device cloud as a 32-bit integer, so the input
        to this function should be either None, an integer, or a string that can
        be converted to an integer.
        """
        if isinstance(quality, *six.string_types):
            quality = int(quality)
        elif isinstance(quality, float):
            quality = int(quality)

        self._quality = validate_type(quality, type(None), *six.integer_types)

    def get_location(self):
        """Get the location for this data point
        The location will be either None or a 3-tuple of floats in the form
        (latitude-degrees, longitude-degrees, altitude-meters).
        """
        return self._location

    def set_location(self, location):
        """Set the location for this data point
        The location must be either None (if no location data is known) or a
        3-tuple of floating point values in the form
        (latitude-degrees, longitude-degrees, altitude-meters).
        """
        if location is None:
            self._location = location

        elif isinstance(location, *six.string_types):  # from device cloud, convert from csv
            parts = str(location).split(",")
            if len(parts) == 3:
                self._location = tuple(map(float, parts))
                return
            else:
                raise ValueError("Location string %r has unexpected format" % location)

        elif (isinstance(location, (tuple, list))
                and len(location) == 3
                and all([isinstance(x, (float, six.integer_types)) for x in location])):
            self._location = tuple(map(float, location))  # coerce ints to float
        else:
            raise TypeError("Location must be None or 3-tuple of floats")

        self._location = location

    def get_data_type(self):
        """Get the data type for this data point
        The data type is associted with the stream itself but may also be
        included in data point writes.  The data type information in the point
        is also used to determine which type conversions should be applied to
        the data.
        """
        return self._data_type

    def set_data_type(self, data_type):
        """Set the data type for ths data point
        The data type is actually associated with the stream itself and should
        not (generally) vary on a point-per-point basis.  That being said, if
        creating a new stream by writing a datapoint, it may be beneficial to
        include this information.
        The data type provided should be in the set of available data types of
        { INTEGER, LONG, FLOAT, DOUBLE, STRING, BINARY, UNKNOWN }.
        """
        validate_type(data_type, type(None), *six.string_types)
        if isinstance(data_type, *six.string_types):
            data_type = str(data_type).upper()
        if not data_type in ({None} | set(DSTREAM_TYPE_MAP.keys())):
            raise ValueError("Provided data type not in available set of types")
        self._data_type = data_type

    def get_units(self):
        """Get the units of this datapoints stream if available"""
        return self._units

    def set_units(self, unit):
        """Set the unit for this data point
        Unit, as with data_type, are actually associated with the stream and not
        the individual data point.  As such, changing this within a stream is
        not encouraged.  Setting the unit on the data point is useful when the
        stream might be created with the write of a data point.
        """
        self._units = validate_type(unit, type(None), *six.string_types)

if __name__ == "__main__":
    # in this example we 'll connect to Device Cloud, set defined stream and set information from data point
    #  to instances of new class. after this we 'll get information from instances
    dsc = DataStreamConnect()
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
    # trying to set correct stream
    dsc.set_stream("classroom")
    print
    # get information in data points and set it to our class
    raw_data_from_devicecloud = list(dsc.get_stream().read())
    list_POJO = list()
    for datapoint in raw_data_from_devicecloud:
        # first we create new empty instance of pojo class
        pj = POJO_holding()
        #  and now set data to it
        pj.set_id(datapoint.get_id())
        pj.set_data(datapoint.get_data())
        pj.set_data_type(datapoint.get_data_type())
        pj.set_description(datapoint.get_description())
        pj.set_location(datapoint.get_location())
        pj.set_quality(datapoint.get_quality())
        pj.set_stream_id(dsc.get_stream_id())
        pj.set_timestamp(datapoint.get_timestamp())
        pj.set_server_timestamp(datapoint.get_server_timestamp())
        pj.set_units(datapoint.get_units())
        list_POJO.append(pj)

#  so, we store information from datapoints in list of POJO_holding class
#  and can to manipulate with this data
    for pojo in list_POJO:
        print pojo.get_id()
        print pojo.get_data()
