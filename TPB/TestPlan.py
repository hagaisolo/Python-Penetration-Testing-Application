# This class is the test plan include all hte details is needs
# The object is created by the TPB and returned to main
# later according to this object the Test Manager run the tests.


class TestPlan(object):
    def __init__(self,some_list):
        self.group_list = []
        self.group_list.append(some_list)
