from devicecloud import DeviceCloud
from devicecloud.streams import DataPoint
import random
import time


def write_stream_and_points(dc):
    # get a test stream reference
    test_stream = dc.streams.get_stream_if_exists("temperature_test_stream")

    # I can create only one stream, so delete it before creating new.
    if test_stream is not None:
        test_stream.delete()

    test_stream = dc.streams.create_stream(
        stream_id="temperature_test_stream",
        data_type='DOUBLE',
        description='this stream used for testing',
        data_ttl=8035200,
        rollup_ttl=63244800,
        units='C',
    )

    print("Writing data points with two second delay")
    for i in range(30):
        print("Writing point {} ".format(i + 1))
        test_stream.write(DataPoint(
            data = round(random.uniform(20,30),2),
            description="this data points used for testing",
            # location - Kharkiv
            location=(49.980556,36.252500,113)
        ))
        time.sleep(2)

    points = list(test_stream.read(newest_first=False))
    print("Read {} data points".format(len(points)))


username = "nanri-test" # our username
password = "!Nanri0118" # our password

dc = DeviceCloud(username, password)
write_stream_and_points(dc)
