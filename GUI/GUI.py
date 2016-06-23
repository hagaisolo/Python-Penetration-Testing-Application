from Tkinter import *
import tkMessageBox
from PIL import ImageTk, Image
import UI
from Core.DA import DA

data_analyzer = DA.DA()
ui = UI.UI()
tpb = UI.BuildTestPlan()


class DAWindow(object):
    def __init__(self):
        pass

    def run(self):
        self.root = Toplevel()
        self.root.geometry('600x80')
        self.root.wm_title("DA")
        background_image = jpg_image("GUI/pic/cyber_tpb.jpg")
        background_label=Label(self.root, image=background_image, width=240, height=300)
        background_label.place(x=140,y=0,relwidth=1, relheight=1)

        f1 = Frame(self.root, height=32, width=240)
        f1.pack_propagate(0)
        button1 = Button(f1, text="Display", command=data_analyzer.display)
        button1.pack(fill=BOTH, expand=1)
        f1.grid(row=1, column=0)

        """
        f2 = Frame(self.root, height=32, width=240)
        f2.pack_propagate(0)
        button2 = Button(f2, text="Analyze", command=tpb.test_planner.full_test_plan)
        button2.pack(fill=BOTH, expand=1)
        f2.grid(row=2)
        """

        f3 = Frame(self.root, height=32, width=240)
        f3.pack_propagate(0)
        button3 = Button(f3, text="Exit", command=self.root.destroy)
        button3.pack(fill=BOTH, expand=1)
        f3.grid(row=3)

        self.root.mainloop()


class TPBWindow(object):
    def __init__(self):
        pass

    def run(self):
        self.root = Toplevel()
        self.root.geometry('600x224')
        self.root.wm_title("Test Plan Builder")
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
        button3 = Button(f3, text="Custom Test Plan", command=self.custom)
        button3.pack(fill=BOTH, expand=1)
        f3.grid(row=3)

        f4 = Frame(self.root, height=32, width=240)
        f4.pack_propagate(0)
        button4 = Button(f4, text="Smart Test Plan", command=self.smart)
        button4.pack(fill=BOTH, expand=1)
        f4.grid(row=4)

        f5 = Frame(self.root, height=32, width=240)
        f5.pack_propagate(0)
        button5 = Button(f5, text="List all groups", command=self.list_all_groups)
        button5.pack(fill=BOTH, expand=1)
        f5.grid(row=5)

        f6 = Frame(self.root, height=32, width=240)
        f6.pack_propagate(0)
        button6 = Button(f6, text="Exit", command=self.root.destroy)
        button6.pack(fill=BOTH, expand=1)
        f6.grid(row=6)

        f7 = Frame(self.root, height=32, width=240)
        f7.pack_propagate(0)
        button7 = Button(f7, text="Help", command=self.help)
        button7.pack(fill=BOTH, expand=1)
        f7.grid(row=7)

        self.root.mainloop()

    @staticmethod
    def single():
        def callBack():
            group = [e.get()]
            try:
                if tpb.test_planner.single_test_plan(group):
                    newroot.destroy()
            except Exception as msg:
                tkMessageBox.showinfo(msg.message,msg.message)
        newroot = Toplevel()
        newroot.geometry('400x40')
        newroot.wm_title("Single Test")
        e = Entry(newroot)
        e.pack(side=TOP)

        f7 = Frame(newroot, height=32, width=240)
        f7.pack_propagate(0)
        button7 = Button(f7, text="Press", command=callBack)
        button7.pack(fill=BOTH, expand=1)
        f7.pack(side=TOP)
        e.insert(0, "Group Name")

    @staticmethod
    def custom():
        def callBack():
            groups = e.get()
            try:
                if tpb.test_planner.custom_test_plan(groups):
                    newroot.destroy()
            except Exception as msg:
                tkMessageBox.showinfo(msg.message,msg.message)
        newroot = Toplevel()
        newroot.geometry('400x40')
        newroot.wm_title("Custom Test Plan")
        e = Entry(newroot, width=60)
        e.pack(side=TOP)

        f7 = Frame(newroot, height=32, width=400)
        f7.pack_propagate(0)
        button7 = Button(f7, text="Press", command=callBack)
        button7.pack(fill=BOTH, expand=1)
        f7.pack(side=TOP)
        e.insert(0, "Enter Group\s name\s seperated by space [PingA PingB ...]")

    @staticmethod
    def list_all_groups():
        # tkMessageBox.showinfo("",tpb.test_planner.list_all_groups())
        help_text = '\n'.join(tpb.test_planner.list_all_groups())
        new_root = Toplevel()
        new_root.geometry("500x400")
        T = Text(new_root, height=20, width=60)
        T.pack()
        T.insert(END,help_text )

    @staticmethod
    def smart():
        scrollbar = ['']*5
        listboxs  = ['']*5
        char_button = ['']*5
        select_buttons = ['']*5

        def run_smart_test():
            tpb.test_planner.smart_test_plan()
            new_root.destroy()

        def select(_layer, _charact, _option):
            tpb.test_planner.iot_user.add_characterization(_layer, (_charact, _option))

        def choose(_layer, _charact, _row):
            scrollbar[_layer-1] = Scrollbar(new_root)
            scrollbar[_layer-1].grid(row=_row, column=5)
            listboxs[_layer-1] = Listbox(new_root, yscrollcommand=scrollbar[_layer-1], height=3)
            print _charact
            for option in tpb.test_planner.iot_all.layers[_layer-1][_charact]:
                listboxs[_layer-1].insert(END, option)
            listboxs[_layer-1].grid(row=_row, column=4)
            scrollbar[_layer-1].config(command=listboxs[_layer-1].yview)

            select_buttons[_layer-1] = Button(new_root, text="Select", command= lambda: select(_layer=_layer,
                            _charact = _charact,
                            _option=listboxs[_layer-1].get(listboxs[_layer-1].curselection()[0])))
            select_buttons[_layer-1].grid(row=_row, column=6)



        # tpb.test_planner.smart_test_plan()
        new_root = Toplevel()
        new_root.geometry("800x400")

        # we form a 6 X 2 grid 5 rows for each layer and scroll bar to choose and 1 row for help

        # row 1
        Label(new_root, text="Layer_1_-_Device_______________________________:").grid(row=0, column=0)
        scrollbar_layer1 = Scrollbar(new_root)
        scrollbar_layer1.grid(row=0, column=2)
        listbox_layer1 = Listbox(new_root, yscrollcommand=scrollbar_layer1, height=3)
        for it in tpb.test_planner.iot_all.layers[0].iterkeys():
            listbox_layer1.insert(END, it)
        listbox_layer1.grid(row=0, column=1)
        scrollbar_layer1.config(command=listbox_layer1.yview)

        char_button[0] = Button(new_root, text="Choose", command= lambda: choose(_layer=1,
                            _charact=listbox_layer1.get(listbox_layer1.curselection()[0]) , _row=0))
        char_button[0].grid(row=0, column=3)

        # row 2
        Label(new_root, text="Layer_2_-_Setup________________________________:").grid(row=1, column=0)
        scrollbar_layer2 = Scrollbar(new_root)
        scrollbar_layer2.grid(row=1, column=2)
        listbox_layer2 = Listbox(new_root, yscrollcommand=scrollbar_layer2, height=3)
        for it in (tpb.test_planner.iot_all.layers[1].iterkeys()):
            listbox_layer2.insert(END, it)
        listbox_layer2.grid(row=1, column=1)
        scrollbar_layer2.config(command=listbox_layer2.yview)

        char_button[1] = Button(new_root, text="Choose", command= lambda: choose(_layer=2,
                            _charact=listbox_layer2.get(listbox_layer2.curselection()[0]) , _row=1))
        char_button[1].grid(row=1, column=3)

        # row 3
        Label(new_root, text="Layer 3 - Low Level Communication Protocols :").grid(row=2, column=0)
        scrollbar_layer3 = Scrollbar(new_root)
        scrollbar_layer3.grid(row=2, column=2)
        listbox_layer3 = Listbox(new_root, yscrollcommand=scrollbar_layer3, height=3)
        for it in tpb.test_planner.iot_all.layers[2].iterkeys():
            listbox_layer3.insert(END, it)
        listbox_layer3.grid(row=2, column=1)
        scrollbar_layer3.config(command=listbox_layer3.yview)

        char_button[2] = Button(new_root, text="Choose", command= lambda: choose(_layer=3,
                            _charact=listbox_layer3.get(listbox_layer3.curselection()[0]) , _row=2))
        char_button[2].grid(row=2, column=3)

        # row 4
        Label(new_root, text="Layer 4 - High level Communication Protocols:").grid(row=3, column=0)
        scrollbar_layer4 = Scrollbar(new_root)
        scrollbar_layer4.grid(row=3, column=2)
        listbox_layer4 = Listbox(new_root, yscrollcommand=scrollbar_layer4, height=3)
        for it in tpb.test_planner.iot_all.layers[3].iterkeys():
            listbox_layer4.insert(END, it)
        listbox_layer4.grid(row=3, column=1)
        scrollbar_layer4.config(command=listbox_layer4.yview)

        char_button[3] = Button(new_root, text="Choose", command= lambda: choose(_layer=4,
                            _charact=listbox_layer4.get(listbox_layer4.curselection()[0]) , _row=3))
        char_button[3].grid(row=3, column=3)

        # row 5
        Label(new_root, text="Layer 5 - Representation and Encryption     :").grid(row=4, column=0)
        scrollbar_layer5 = Scrollbar(new_root)
        scrollbar_layer5.grid(row=4, column=2)
        listbox_layer5 = Listbox(new_root, yscrollcommand=scrollbar_layer5, height=3)
        for it in tpb.test_planner.iot_all.layers[4].iterkeys():
            listbox_layer5.insert(END, it)
        listbox_layer5.grid(row=4, column=1)
        scrollbar_layer5.config(command=listbox_layer5.yview)

        char_button[4] = Button(new_root, text="Choose", command= lambda: choose(_layer=5,
                            _charact=listbox_layer5.get(listbox_layer5.curselection()[0]) , _row=4))
        char_button[4].grid(row=4, column=3)


        initiate_button = Button(new_root, text="Select Test Plan", command = run_smart_test)
        initiate_button.grid(row=5, column=0)

    @staticmethod
    def help():
        help_text = tpb.test_planner.help_text()
        new_root = Toplevel()
        new_root.geometry("500x400")
        T = Text(new_root, height=20, width=60)
        T.pack()
        T.insert(END,help_text )



da = DAWindow()
te = TPBWindow()


def jpg_image(img_path):
    # Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    image = Image.open(img_path)
    image = image.resize((400, 320), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)


class MainWindow(object):
    def __init__(self):
        self.root = Tk()
        self.root.geometry('400x280')
        self.root.wm_title("IoT Penetration Testing Python Platform")
        background_image = jpg_image("GUI/pic/cyber_main.jpg")
        background_label = Label(self.root, image=background_image)
        background_label.place(x=0, y=0)

        f_top_left = Frame(self.root, height=400, width=100)
        f_top_left.pack_propagate(0)
        f_top_left.pack(side=LEFT)

        button1 = Button(f_top_left, text="Create Test Plan", command=te.run, height=2)
        button1.pack(side=TOP, fill=X)

        button2 = Button(f_top_left, text="Get Parameters", command=ui.gather_parameters,  height=2)
        button2.pack(side=TOP, fill=X)

        button3 = Button(f_top_left, text="Tests Results", command=da.run,  height=2)
        button3.pack(side=TOP, fill=X)

        button4 = Button(f_top_left, text="Run Tests", command=ui.run_tests,  height=2)
        button4.pack(side=TOP, fill=X)

        button5 = Button(f_top_left, text="Show Test Plan", command=self.test_plan_msg,  height=2)
        button5.pack(side=TOP, fill=X)

        button6 = Button(f_top_left, text="Exit", command=exit,  height=2)
        button6.pack(side=TOP, fill=X)

        button7 = Button(f_top_left, text="Help", command=None,  height=2)
        button7.pack(side=TOP, fill=X)

        self.root.mainloop()

    def test_plan_msg(self):
        lst = ui.get_test_plan().get_list()
        text = "Test Plan:\n"
        for item, num in zip(lst, range(len(lst))):
            text = text + str(num+1) + ". " + item + "\n"
        msg = Message(self.root, text=text)
        msg.config(bg='grey', font=('times', 8))
        msg.pack()


if __name__ == "__main__":
    MainWindow()
