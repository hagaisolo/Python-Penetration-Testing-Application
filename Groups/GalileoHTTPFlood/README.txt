The GalileoHTTPFlood Group is a single test group.
The test initiate tcp communication (socket) with my Galileo device and start sending
pakcet to the device. the device is a HTTP server serving weather data collected by the Galileo board.

In this test we check if it is possible to block communication to the device and how many stress
is required to do so.

This test was design to the specific device and applicaiton. it is not a good test valid for any device!