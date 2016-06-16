from Tkinter import *
from PIL import ImageTk, Image
import UI


ui = UI.UI()
tpb = UI.BuildTestPlan()


class TPBWindow(object):
    def __init__(self):
        self.root = Toplevel()
        self.root.geometry('600x224')
        self.root.wm_title("Test Plan Builder")

    def run(self):
        background_image = jpg_image("GUI/pic/cyber_tpb.jpg")
        background_label=Label(self.root, image=background_image, width=240, height=300)
        background_label.place(x=140,y=0,relwidth=1, relheight=1)

        f1 = Frame(self.root, height=32, width=240)
        f1.pack_propagate(0)
        button1 = Button(f1, text="Single (Run single test)", command=self.single)
        button1.pack(fill=BOTH, expand=1)
        f1.grid(row=1, column=0)

        f2 = Frame(self.root, height=32, width=240)
        f2.pack_propagate(0)
        button2 = Button(f2, text="Full Test Plan (run all tests)", command=tpb.test_planner.full_test_plan)
        button2.pack(fill=BOTH, expand=1)
        f2.grid(row=2)

        f3 = Frame(self.root, height=32, width=240)
        f3.pack_propagate(0)
        button3 = Button(f3, text="Custom Test Plan", command=tpb.test_planner.custom_test_plan)
        button3.pack(fill=BOTH, expand=1)
        f3.grid(row=3)

        f4 = Frame(self.root, height=32, width=240)
        f4.pack_propagate(0)
        button4 = Button(f4, text="Smart Test Plan", command=tpb.test_planner.smart_test_plan)
        button4.pack(fill=BOTH, expand=1)
        f4.grid(row=4)

        f5 = Frame(self.root, height=32, width=240)
        f5.pack_propagate(0)
        button5 = Button(f5, text="List all groups", command=tpb.test_planner.list_all_groups)
        button5.pack(fill=BOTH, expand=1)
        f5.grid(row=5)

        f6 = Frame(self.root, height=32, width=240)
        f6.pack_propagate(0)
        button6 = Button(f6, text="Exit", command=root.destroy)
        button6.pack(fill=BOTH, expand=1)
        f6.grid(row=6)

        f7 = Frame(self.root, height=32, width=240)
        f7.pack_propagate(0)
        button7 = Button(f7, text="Help", command=None)
        button7.pack(fill=BOTH, expand=1)
        f7.grid(row=7)

        self.root.mainloop()

    def single(self):
        e = Entry(self.root)
        e.pack(side=TOP)
        temp = sys.stdin
        str = sys.stdin
        tpb.test_planner.single_test_plan()
        e.insert(str)
        write = sys.stdout.write
        read  = sys.stdin.read


te = TPBWindow()


def jpg_image(img_path):
    # Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    image = Image.open(img_path)
    image = image.resize((400, 320), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)


class MainWindow(object):
    def __init__(self):
        root = Tk()
        self.root = root
        root.geometry('400x280')
        root.wm_title("IoT Penetration Testing Python Platform")
        background_image = jpg_image("GUI/pic/cyber_main.jpg")
        background_label = Label(root, image=background_image)
        background_label.place(x=0,y=0)

        f_top_left = Frame(root, height=400, width=100)
        f_top_left.pack_propagate(0)
        f_top_left.pack(side=LEFT)

        button1 = Button(f_top_left, text="Create Test Plan", command=te.run, height=2)
        button1.pack(side=TOP, fill=X)

        button2 = Button(f_top_left, text="Get Parameters", command=ui.gather_parameters,  height=2)
        button2.pack(side=TOP, fill=X)

        button3 = Button(f_top_left, text="Tests Results", command=ui.data_collect,  height=2)
        button3.pack(side=TOP, fill=X)

        button4 = Button(f_top_left, text="Run Tests", command=ui.run_tests,  height=2)
        button4.pack(side=TOP, fill=X)

        button5 = Button(f_top_left, text="Show Test Plan", command=self.test_plan_msg,  height=2)
        button5.pack(side=TOP, fill=X)

        button6 = Button(f_top_left, text="Exit", command=exit,  height=2)
        button6.pack(side=TOP, fill=X)

        button7 = Button(f_top_left, text="Help", command=None,  height=2)
        button7.pack(side=TOP, fill=X)

        root.mainloop()

    def test_plan_msg(self):
        lst = ui.get_test_plan().get_list()
        text = "Test Plan:\n"
        for item,num in zip(lst,range(len(lst))):
            text = text + str(num+1) + ". " + item + "\n"
        msg = Message(self.root, text=text)
        msg.config(bg='grey', font=('times', 8))
        msg.pack( )



if __name__ == "__main__":
    MainWindow()
