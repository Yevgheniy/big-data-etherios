from devicecloud import DeviceCloud
import math
import time

username = "11nanri-test" # our username
password = "!Nanri0118" # our password

dc = DeviceCloud(username, password)

def write_points_and_delete_some(dc):
    test_stream = dc.streams.get_stream_if_exists("temperature_test_stream")

    if test_stream is not None:
        test_stream.delete()

    # get a test stream reference
    test_stream = dc.streams.get_stream_if_exists("test")

    # we want a clean stream to work with.  If the stream exists, nuke it
    if test_stream is not None:
        test_stream.delete()

    test_stream = dc.streams.create_stream(
        stream_id="test",
        data_type='float',
        description='a stream used for testing',
        units='some-unit',
    )

    print("Writing data points with five second delay")
    for i in range(5):
        print("Writing point {} / 5".format(i + 1))
        test_stream.write(DataPoint(
            data=i * 1000,
            description="This is {} * pi".format(i)
        ))
        if i < (5 - 1):
            time.sleep(1)

    points = list(test_stream.read(newest_first=False))
    print("Read {} data points, removing the first".format(len(points)))

    # Remove the first
    test_stream.delete_datapoint(points[0])
    points = list(test_stream.read(newest_first=False))
    print("Read {} data points, removing ones written in last 30 seconds".format(len(points)))

    # delete the ones in the middle
    test_stream.delete_datapoints_in_time_range(
        start_dt=points[1].get_timestamp(),
        end_dt=points[-1].get_timestamp()
    )
    points = list(test_stream.read(newest_first=False))
    print("Read {} data points.  Will try to delete all next".format(len(points)))
    pprint.pprint(points)

    # let's try without any range at all and see if they all get deleted
    test_stream.delete_datapoints_in_time_range()
    points = list(test_stream.read(newest_first=False))
    print("Read {} data points".format(len(points)))

    test_stream.delete()

