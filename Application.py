"""
A graphical user interface for users to easily price various options with your pricer.
"""

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
import tkinter.font as tkFont
from MCArithAsianOption import MCArithAsianOption
from MCArithBasketOption import MCArithBasketOption


class Application:
    
    def __init__(self):
        
        self.window = Tk()
        self.window.title("Mini Option Pricer")
        self.window.geometry('%dx%d' % (700, 400))
        self.menubar = Menu(self.window)

        self.__createPage()
        self.__HomePage()
        self.__createMenu()

        self.window.config(menu=self.menubar)
        
        self.__forgetFrame()
        self.frame6.pack()  # Place frame6 into the window
        
        # design the homepage
        ft = tkFont.Font(size = 23, weight = tkFont.BOLD)
        Label(self.frame6, text = "Mini Option Pricer", font = ft,  fg = "grey", height = 11).pack()
        Label(self.frame6, text = "Authors: Wu Bijia, Zhang Weibin, Xue Botu").pack()
        
        self.window.mainloop()

    def __createPage(self):
        
        self.frame1 = Frame(self.window)
        self.frame2 = Frame(self.window)
        self.frame3 = Frame(self.window)
        self.frame4 = Frame(self.window)
        self.frame5 = Frame(self.window)
        self.frame6 = Frame(self.window)

    def __HomePage(self):
        
        homepage = Menu(self.menubar, tearoff=0)
        homepage.add_command(label="Homepage", command=self.run_homepage)
        homepage.add_command(label="Quit", command = self.Quit)
        self.menubar.add_cascade(label = 'Homepage', menu = homepage)

    def __createMenu(self):
        
        filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Select Pricer Model', menu=filemenu)
        filemenu.add_command(label="Pricer 1: European Options - Black-Scholes Formulas", command=self.task1)
        filemenu.add_command(label="Pricer 2: Implied volatility - European Options", command=self.task2)
        filemenu.add_command(label="Pricer 3: Geometric Asian Options & Geometric Basket Options - Closed-Form Formulas", command=self.task4)
        filemenu.add_command(label="Pricer 4: Arithmetic Asian Options - Monte Carlo Method", command=self.task4)
        filemenu.add_command(label="Pricer 5: Arithmetic Mean Basket Options - Monte Carlo Method", command=self.task5)

    # For switching page, forget the current page and jump to another page
    def __forgetFrame(self):
        
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame4.pack_forget()
        self.frame5.pack_forget()
        self.frame6.pack_forget()

    def task1(self):
        
        self.__forgetFrame()
        frame = self.frame1
        frame.pack()  # Place frame1 into the window
        
        # define labels
        label_title = Label(frame, text = "Implement Black-Scholes Formulas for European call/put options.", fg = "red", justify = "right").grid(row = 1, column = 1,sticky = W)
        label_s0 = Label(frame, text = "Spot Price of Asset:").grid(row = 3, column = 1, sticky = W)
        label_sigma = Label(frame, text = "Volatility:").grid(row = 4, column = 1, sticky = W)
        label_r = Label(frame, text = "Risk-free Interest Rate:").grid(row = 5, column = 1, sticky = W)
        label_repo = Label(frame, text = "Repo Rate:").grid(row = 6, column = 1, sticky = W)
        label_T = Label(frame, text = "Time to Maturity (in years):").grid(row = 7, column = 1, sticky = W)
        label_K = Label(frame, text = "Strike:").grid(row = 8, column = 1, sticky = W)
        label_OptionType = Label(frame, text = "Option Type:").grid(row = 9, column = 1, sticky = W)
        
        # define input type for input input variables
        self.s0 = DoubleVar()
        self.sigma = DoubleVar()
        self.r = DoubleVar()
        self.repo = DoubleVar()
        self.T = DoubleVar()
        self.K = DoubleVar()
        self.option_type = StringVar()
        
        # define input boxes for input variables
        entry_s0 = Entry(frame, textvariable = self.s0).grid(row = 3, column = 2, sticky = W)
        entry_sigma = Entry(frame, textvariable = self.sigma).grid(row = 4, column = 2, sticky = W)
        entry_r = Entry(frame, textvariable = self.r).grid(row = 5, column = 2, sticky = W)
        entry_repo = Entry(frame, textvariable = self.repo).grid(row = 6, column = 2, sticky = W)
        entry_T = Entry(frame, textvariable = self.T).grid(row = 7, column = 2, sticky = W)
        entry_K = Entry(frame, textvariable = self.K).grid(row = 8, column = 2, sticky = W)
        
        # define the list for user to select option type
        comboboxlist = ttk.Combobox(frame, width = 17, values = ("Select Option Type", "Call Option", "Put Option"),textvariable = self.option_type, postcommand = self.run_task1)  
        comboboxlist.current(0) # set the default Option Type: Call Option
        comboboxlist.grid(row = 9, column = 2, sticky = W)
        
        # Reset the input and the log
        btReset = Button(frame, width = 10, text = "Reset", command = self.ResetTask1).grid(row=10, column=2, columnspan = 1, sticky = E)
        
        # define run button to run the computing
        btRun = Button(frame, width = 10, text = "Run", command = self.run_task1).grid(row=10, column=2, columnspan = 1, sticky = W)
        
        # define the window to display the result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height = 12)
        self.logs.grid(row = 20, column = 1, rowspan = 4, columnspan=2, sticky = W)
        
    def task2(self):
        
        self.__forgetFrame()
        frame = self.frame2
        frame.pack()  # Place frame2 into the window
        
        # define labels
        label_title = Label(frame, text = "Implied Volatility Calculator", fg = "red", justify = "right").grid(row = 1, column = 1,sticky = W)
        label_s0 = Label(frame, text = "Spot Price of Asset:").grid(row = 3, column = 1, sticky = W)
        label_sigma = Label(frame, text = "Volatility:").grid(row = 4, column = 1, sticky = W)
        label_r = Label(frame, text = "Risk-free Interest Rate:").grid(row = 5, column = 1, sticky = W)
        label_T = Label(frame, text = "Time to Maturity (in years):").grid(row = 6, column = 1, sticky = W)
        label_K = Label(frame, text = "Strike:").grid(row = 7, column = 1, sticky = W)
        label_N = Label(frame, text = "number of steps:").grid(row = 8, column = 1, sticky = W)
        label_OptionType = Label(frame, text="Option Type:").grid(row = 9, column = 1, sticky = W)
        
        # define input type for input input variables
        self.s0 = DoubleVar()
        self.sigma = DoubleVar()
        self.r = DoubleVar()
        self.T = DoubleVar()
        self.K = DoubleVar()
        self.N = IntVar()
        self.option_type = StringVar()
        
        # define input boxes for input variables
        entry_s0 = Entry(frame, textvariable = self.s0).grid(row = 3, column = 2, sticky = E)
        entry_sigma = Entry(frame, textvariable = self.sigma).grid(row = 4, column = 2, sticky = E)
        entry_r = Entry(frame, textvariable = self.r).grid(row = 5, column = 2, sticky = E)
        entry_T = Entry(frame, textvariable = self.T).grid(row = 6, column = 2, sticky = E)
        entry_K = Entry(frame, textvariable = self.K).grid(row = 7, column = 2, sticky = E)
        entry_N = Entry(frame, textvariable = self.N).grid(row = 8, column = 2, sticky = E)
        
        # define the list for user to select option type
        comboboxlist = ttk.Combobox(frame, width = 17, values = ("Select Option Type", "Call Option", "Put Option"),textvariable = self.option_type, postcommand = self.run_task1)  
        comboboxlist.current(0) # set the default Option Type: Call Option
        comboboxlist.grid(row = 9, column = 2, sticky = E)
        
        # Reset the input and the log
        btReset = Button(frame, width = 18, text = "Reset", command = self.ResetTask2).grid(row=10, column=1, columnspan = 1, sticky = E)
        
        # define run button to run the computing
        btRun = Button(frame, width = 18, text = "Run", command = self.run_task1).grid(row=10, column=1, columnspan = 1, sticky = W)
        
        # define the window to display the result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height = 12)
        self.logs.grid(row = 20, column = 1, rowspan = 4, columnspan=2, sticky = W)
        
    def task4(self):
        frame = self.frame4
        self.__forgetFrame()
        frame.pack()  # 将框架frame4放置在window中˝

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

        self.logs = scrolledtext.ScrolledText(frame, width = 74, height = 19)
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
        
    def ResetTask1(self):
        
        frame = self.frame1
        
        self.s0 = 0
        self.sigma = 0
        self.r = 0
        self.repo = 0
        self.T = 0
        self.K = 0
        
        entry_s0 = Entry(frame, textvariable = self.s0).grid(row = 3, column = 2, sticky = W)
        entry_sigma = Entry(frame, textvariable = self.sigma).grid(row = 4, column = 2, sticky = W)
        entry_r = Entry(frame, textvariable = self.r).grid(row = 5, column = 2, sticky = W)
        entry_repo = Entry(frame, textvariable = self.repo).grid(row = 6, column = 2, sticky = W)
        entry_T = Entry(frame, textvariable = self.T).grid(row = 7, column = 2, sticky = W)
        entry_K = Entry(frame, textvariable = self.K).grid(row = 8, column = 2, sticky = W)
        
        self.task1()
        
    def run_homepage(self):
        
        self.__forgetFrame()
        self.frame6.pack()
        
    def run_task1(self):
        
        OptionType = self.option_type.get()
        
        if OptionType == "Call Option":
            
            self.logs.insert(END, "The result: {}\n".format(OptionType))
            
        elif OptionType == "Put Option":
            
            self.logs.insert(END, "The result: {}\n".format(OptionType))
            
        else:
            
            self.logs.insert(END, "The Option Type is not specified or incorrect, please specified it. \n")
            
    def ResetTask2(self):
        
        frame = self.frame2
        
        self.s0 = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.K = 0
        self.N = 0
        
        entry_s0 = Entry(frame, textvariable = self.s0).grid(row = 3, column = 2, sticky = E)
        entry_sigma = Entry(frame, textvariable = self.sigma).grid(row = 4, column = 2, sticky = E)
        entry_r = Entry(frame, textvariable = self.r).grid(row = 5, column = 2, sticky = E)
        entry_T = Entry(frame, textvariable = self.T).grid(row = 6, column = 2, sticky = E)
        entry_K = Entry(frame, textvariable = self.K).grid(row = 7, column = 2, sticky = E)
        entry_N = Entry(frame, textvariable = self.N).grid(row = 8, column = 2, sticky = E)
        
        self.task2()
        
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
        
    def Quit(self):
        
        self.window.destroy()

if __name__ == '__main__':
    Application()
