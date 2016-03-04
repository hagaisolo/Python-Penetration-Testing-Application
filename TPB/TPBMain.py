#
# This is the test plan build (TPB) main file it hold the TPB class and some methods
# some more advanced method and features of the TPB are included in neighbours files
import TPBMenu


class TPB(object):
    def __init__(self):
        pass

    @staticmethod
    def intro_menu():
        test_plan = TPBMenu.menu()
        return test_plan