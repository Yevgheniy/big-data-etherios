from devicecloud import DeviceCloud
import pprint

# The following lines require manual changes
username = "nanri-test" # enter your username
password = "!Nanri0118" # enter your password


dc = DeviceCloud(username, password)

# show the MAC address of all devices that are currently connected
#
# This is done using the device cloud DeviceCore functionality
# print "== Connected Devices =="
# for device in dc.devicecore.get_devices():
#     if device.is_connected():
#         print device.get_mac()

print "== All our Devices =="
for device in dc.devicecore.get_devices():
    print device.get_mac()
print
print


# get the name of all data streams

print "== All our streams =="
for stream in dc.streams.get_streams():
    print "%s " % (stream.get_stream_id())
    raw_data_from_devicecloud = list(stream.read())
    print 'This stream contains {} datapoints'.format(len(raw_data_from_devicecloud))
    pprint.pprint(raw_data_from_devicecloud)
    print

# get the name and current value of all data streams having values
# with a floating point type
#
# This is done using the device cloud stream functionality
print "== Our digit streams =="
for stream in dc.streams.get_streams():
    if stream.get_data_type().lower() in ('float', 'double'):
        print "%s -> %s" % (stream.get_stream_id(), stream.get_current_value())
        raw_data_from_devicecloud = list(stream.read())
        # for dc in raw_data_from_device cloud:
        print("Read {} data points.".format(len(raw_data_from_devicecloud)))
    print
