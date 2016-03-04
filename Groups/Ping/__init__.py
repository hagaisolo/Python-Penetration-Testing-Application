# The group's Welcome file, it manages and run the group's tests
from Ping import collect_param as collect_param
from Ping import ping as ping

if __name__ == "__main__":
    parameters = collect_param()
    ping(ip=parameters[0][1], count=parameters[1][1])
    raw_input("Press any key To exit group")
