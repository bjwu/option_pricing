"""
A graphical user interface for users to easily price various options with your pricer.
"""

from tkinter import *
from tkinter import scrolledtext
from MCArithAsianOption import MCArithAsianOption
from MCArithBasketOption import MCArithBasketOption


class Application:
    def __init__(self):
        self.window = Tk()
        self.window.title("Option Pricing")
        self.window.geometry('%dx%d' % (600, 400))
        self.menubar = Menu(self.window)

        self.__createPage()
        self.__createMenu()

        self.window.config(menu=self.menubar)
        self.window.mainloop()

    def __createPage(self):
        self.frame1 = Frame(self.window)
        self.frame2 = Frame(self.window)
        self.frame3 = Frame(self.window)
        self.frame4 = Frame(self.window)
        self.frame5 = Frame(self.window)
        self.frame6 = Frame(self.window)

    def __createMenu(self):
        filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Method', menu=filemenu)
        filemenu.add_command(label="Task 4", command=self.task4)
        filemenu.add_command(label="Task 5", command=self.task5)

    # For switching page, forget the current page and jump to another page
    def __forgetFrame(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame4.pack_forget()
        self.frame5.pack_forget()
        self.frame6.pack_forget()

    def task4(self):
        frame = self.frame4
        self.__forgetFrame()
        frame.pack()  # 将框架frame1放置在window中˝

        label_s0 = Label(frame, text="S0")
        label_sigma = Label(frame, text="sigma")
        label_r = Label(frame, text="r")
        label_T = Label(frame, text="T")
        label_n = Label(frame, text="n")
        label_K = Label(frame, text="K")

        self.s0 = DoubleVar()
        self.sigma = DoubleVar()
        self.r = DoubleVar()
        self.T = DoubleVar()
        self.n = IntVar()
        self.K = DoubleVar()
        self.option_type = StringVar()
        self.ctrl_var = BooleanVar()

        entry_s0 = Entry(frame, textvariable=self.s0)
        entry_sigma = Entry(frame, textvariable=self.sigma)
        entry_r = Entry(frame, textvariable=self.r)
        entry_T = Entry(frame, textvariable=self.T)
        entry_n = Entry(frame, textvariable=self.n)
        entry_K = Entry(frame, textvariable=self.K)

        cbtCV = Checkbutton(frame, text="Control Variate?", variable=self.ctrl_var)

        rbPut = Radiobutton(frame, text="Put", bg="red",
                            variable=self.option_type, value='put')
        rbCall = Radiobutton(frame, text="Call", bg="yellow",
                               variable=self.option_type, value='call')

        btRun = Button(frame, text="Run", command=self.run_task4)

        label_s0.grid(row=1, column=1)
        label_sigma.grid(row=1, column=3)
        label_r.grid(row=2, column=1)
        label_T.grid(row=2, column=3)
        label_n.grid(row=3, column=1)
        label_K.grid(row=3, column=3)

        entry_s0.grid(row=1, column=2)
        entry_sigma.grid(row=1, column=4)
        entry_r.grid(row=2, column=2)
        entry_T.grid(row=2, column=4)
        entry_n.grid(row=3, column=2)
        entry_K.grid(row=3, column=4)

        cbtCV.grid(row=4, column=1)
        rbPut.grid(row=4, column=2)
        rbCall.grid(row=4, column=3)

        btRun.grid(row=5, column=1, columnspan=4)

        self.logs = scrolledtext.ScrolledText(frame)
        self.logs.grid(row=6, column=1, columnspan=4)

    def task5(self):
        frame = self.frame5
        self.__forgetFrame()
        frame.pack()

        label_s0_1 = Label(frame, text="S0_1")
        label_s0_2 = Label(frame, text="S0_2")
        label_sigma_1 = Label(frame, text="sigma_1")
        label_sigma_2 = Label(frame, text="sigma_2")
        label_r = Label(frame, text="r")
        label_T = Label(frame, text="T")
        label_n = Label(frame, text="n")
        label_K = Label(frame, text="K")
        label_rho = Label(frame, text="rho")

        self.s0_1 = DoubleVar()
        self.s0_2 = DoubleVar()
        self.sigma_1 = DoubleVar()
        self.sigma_2 = DoubleVar()
        self.r = DoubleVar()
        self.T = DoubleVar()
        self.n = IntVar()
        self.K = DoubleVar()
        self.rho = DoubleVar()
        self.option_type = StringVar()
        self.ctrl_var = BooleanVar()

        entry_s0_1 = Entry(frame, textvariable=self.s0_1)
        entry_s0_2 = Entry(frame, textvariable=self.s0_2)
        entry_sigma_1 = Entry(frame, textvariable=self.sigma_1)
        entry_sigma_2 = Entry(frame, textvariable=self.sigma_2)
        entry_r = Entry(frame, textvariable=self.r)
        entry_T = Entry(frame, textvariable=self.T)
        entry_n = Entry(frame, textvariable=self.n)
        entry_K = Entry(frame, textvariable=self.K)
        entry_rho = Entry(frame, textvariable=self.rho)


        cbtCV = Checkbutton(frame, text="Control Variate?", variable=self.ctrl_var)

        rbPut = Radiobutton(frame, text="Put", bg="red",
                            variable=self.option_type, value='put')
        rbCall = Radiobutton(frame, text="Call", bg="yellow",
                             variable=self.option_type, value='call')

        btRun = Button(frame, text="Run", command=self.run_task5)

        label_s0_1.grid(row=1, column=1)
        label_s0_2.grid(row=1, column=3)
        label_sigma_1.grid(row=2, column=1)
        label_sigma_2.grid(row=2, column=3)
        label_r.grid(row=3, column=1)
        label_T.grid(row=3, column=3)
        label_n.grid(row=4, column=1)
        label_K.grid(row=4, column=3)
        label_rho.grid(row=5, column=1)


        entry_s0_1.grid(row=1, column=2)
        entry_s0_2.grid(row=1, column=4)
        entry_sigma_1.grid(row=2, column=2)
        entry_sigma_2.grid(row=2, column=4)
        entry_r.grid(row=3, column=2)
        entry_T.grid(row=3, column=4)
        entry_n.grid(row=4, column=2)
        entry_K.grid(row=4, column=4)
        entry_rho.grid(row=5, column=2)

        cbtCV.grid(row=6, column=1)
        rbPut.grid(row=6, column=2)
        rbCall.grid(row=6, column=3)

        btRun.grid(row=7, column=1, columnspan=4)

        self.logs = scrolledtext.ScrolledText(frame)
        self.logs.grid(row=8, column=1, columnspan=4)

    def run_task4(self):
        self.logs.insert(END, "waiting.... [It may take you several minutes]\n\n")

        option = MCArithAsianOption(s0=self.s0.get(), sigma=self.sigma.get(), r=self.r.get(),
                                    T=self.T.get(), K=self.K.get(), n=self.n.get(),
                                    option_type=self.option_type.get(), ctrl_var=self.ctrl_var.get())
        result = option.pricing(num_randoms=100)
        self.logs.insert(END, "The result: {}\n".format(result))

    def run_task5(self):
        self.logs.insert(END, "waiting.... [It may take you several minutes]\n\n")

        option = MCArithBasketOption(s0_1=self.s0_1.get() ,s0_2=self.s0_2.get(), sigma_1=self.sigma_1.get(),
                                     sigma_2=self.sigma_2.get(), r=self.r.get(), T=self.T.get(), K=self.K.get(),
                                     rho=self.rho.get(), n=self.n.get(),option_type=self.option_type.get(),
                                     ctrl_var=self.ctrl_var.get())
        result = option.pricing(num_randoms=100)
        self.logs.insert(END, "The result: {}\n".format(result))


if __name__ == '__main__':
    Application()
