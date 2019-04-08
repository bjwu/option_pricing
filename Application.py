"""
A graphical user interface for users to easily price various options with your pricer.
"""

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
import tkinter.font as tkFont
from BSEuroOption import BSEuroOption
from ImpliedVolatility import ImpliedVolatility
from CFGeoAsianOption import GeoAsianOption
import math
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
        self.frameHomePage.pack()  # Place frameHomePage into the window
        
        # design the homepage
        ft = tkFont.Font(size = 23, weight = tkFont.BOLD)
        Label(self.frameHomePage, text = "Mini Option Pricer", font = ft,  fg = "grey", height = 11).pack()
        Label(self.frameHomePage, text = "Authors: Wu Bijia, Zhang Weibin, Xue Botu").pack()
        
        self.window.mainloop()

    def __createPage(self):
        
        self.frame1 = Frame(self.window)
        self.frame2 = Frame(self.window)
        self.frame3 = Frame(self.window)
        self.frame4 = Frame(self.window)
        self.frame5 = Frame(self.window)
        self.frame6 = Frame(self.window)
        self.frameHomePage = Frame(self.window) 

    def __HomePage(self):
        
        homepage = Menu(self.menubar, tearoff=0)
        homepage.add_command(label = "Homepage", command=self.run_homepage)
        homepage.add_command(label = "Quit", command = self.Quit)
        self.menubar.add_cascade(label = 'Homepage', menu = homepage)

    def __createMenu(self):
        
        filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Select Pricer Model', menu=filemenu)
        filemenu.add_command(label = "Pricer 1: European Options - Black-Scholes Formulas", command=self.task1)
        filemenu.add_command(label = "Pricer 2: Implied volatility - European Options", command=self.task2)
        filemenu.add_command(label = "Pricer 3: Geometric Asian Options - Closed-Form Formulas", command=self.task3)
        filemenu.add_command(label = "Pricer 4: Geometric Basket Options - Closed-Form Formulas", command=self.task4)
        filemenu.add_command(label = "Pricer 5: Arithmetic Asian Options - Monte Carlo Method", command=self.task5)
        filemenu.add_command(label = "Pricer 6: Arithmetic Mean Basket Options - Monte Carlo Method", command=self.task6)

    # For switching page, forget the current page and jump to another page
    def __forgetFrame(self):
        
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame4.pack_forget()
        self.frame5.pack_forget()
        self.frame6.pack_forget()
        self.frameHomePage.pack_forget()

    # Implement Black-Scholes Formulas for European call/put option.
    def task1(self):
        
        self.__forgetFrame()
        frame = self.frame1
        frame.pack()  # Place frame1 into the window
        
        # define labels
        label_title = Label(frame, text = "Implement Black-Scholes Formulas for European Call/Put Option.", fg = "red", justify = "right").grid(row = 1, column = 1,sticky = W)
        label_s0 = Label(frame, text = "Spot Price of Asset:").grid(row = 2, column = 1, sticky = W)
        label_sigma = Label(frame, text = "Volatility:").grid(row = 3, column = 1, sticky = W)
        label_r = Label(frame, text = "Risk-free Interest Rate:").grid(row = 4, column = 1, sticky = W)
        label_repo = Label(frame, text = "Repo Rate:").grid(row = 5, column = 1, sticky = W)
        label_T = Label(frame, text = "Time to Maturity (in years):").grid(row = 6, column = 1, sticky = W)
        label_K = Label(frame, text = "Strike:").grid(row = 7, column = 1, sticky = W)
        label_OptionType = Label(frame, text = "Option Type:").grid(row = 8, column = 1, sticky = W)
        
        self.s0 = DoubleVar()
        self.sigma = DoubleVar()
        self.r = DoubleVar()
        self.repo = DoubleVar()
        self.T = DoubleVar()
        self.K = DoubleVar()
        self.option_type = StringVar()
        
        # define input boxes for input variables
        entry_s0 = Entry(frame, textvariable = self.s0).grid(row = 2, column = 2, sticky = W)
        entry_sigma = Entry(frame, textvariable = self.sigma).grid(row = 3, column = 2, sticky = W)
        entry_r = Entry(frame, textvariable = self.r).grid(row = 4, column = 2, sticky = W)
        entry_repo = Entry(frame, textvariable = self.repo).grid(row = 5, column = 2, sticky = W)
        entry_T = Entry(frame, textvariable = self.T).grid(row = 6, column = 2, sticky = W)
        entry_K = Entry(frame, textvariable = self.K).grid(row = 7, column = 2, sticky = W)
        
        # define the list for user to select option type
        self.comboboxlist_task1 = ttk.Combobox(frame, width = 17, values = ("Select Option Type", "Call Option", "Put Option"), textvariable = self.option_type, postcommand = self.run_task1)  
        self.comboboxlist_task1.current(0) # set the default selection
        self.comboboxlist_task1.grid(row = 8, column = 2, sticky = W)
        
        # Reset input and log
        btReset = Button(frame, width = 10, text = "Reset", command = self.ResetTask1).grid(row = 10, column = 2, columnspan = 1, sticky = E)
        
        # define run button to run the pricer
        btRun = Button(frame, width = 10, text = "Run", command = self.run_task1).grid(row = 10, column = 2, columnspan = 1, sticky = W)
        
        # define a window to display result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height = 12)
        self.logs.grid(row = 11, column = 1, rowspan = 4, columnspan = 2, sticky = W)
        
    # Implied volatility calculations.    
    def task2(self):
        
        self.__forgetFrame()
        frame = self.frame2
        frame.pack()  # Place frame2 into the window
        
        # define labels
        label_title = Label(frame, text = "Implied Volatility Calculator for European Option", fg = "red", justify = "right").grid(row = 1, column = 1,sticky = W)
        label_s0 = Label(frame, text = "Spot Price of Asset:").grid(row = 2, column = 1, sticky = W)
        label_r = Label(frame, text = "Risk-free Interest Rate:").grid(row = 3, column = 1, sticky = W)
        label_q = Label(frame, text = "Repo Rate:").grid(row = 4, column = 1, sticky = W)
        label_T = Label(frame, text = "Time to Maturity (in years):").grid(row = 5, column = 1, sticky = W)
        label_K = Label(frame, text = "Strike:").grid(row = 6, column = 1, sticky = W)
        label_V = Label(frame, text = "Option Premium:").grid(row = 7, column = 1, sticky = W)
        label_OptionType = Label(frame, text = "Option Type:").grid(row = 8, column = 1, sticky = W)
        
        self.s0 = DoubleVar()
        self.r = DoubleVar()
        self.q = DoubleVar()
        self.T = DoubleVar()
        self.K = DoubleVar()
        self.V = DoubleVar()
        self.option_type = StringVar()
        
        # define input boxes for input variables
        entry_s0 = Entry(frame, textvariable = self.s0).grid(row = 2, column = 2, sticky = E)
        entry_r = Entry(frame, textvariable = self.r).grid(row = 3, column = 2, sticky = E)
        entry_q = Entry(frame, textvariable = self.q).grid(row = 4, column = 2, sticky = E)
        entry_T = Entry(frame, textvariable = self.T).grid(row = 5, column = 2, sticky = E)
        entry_K = Entry(frame, textvariable = self.K).grid(row = 6, column = 2, sticky = E)
        entry_V = Entry(frame, textvariable = self.V).grid(row = 7, column = 2, sticky = E)
        
        # define the list for user to select option type
        self.comboboxlist_task2 = ttk.Combobox(frame, width = 17, values = ("Select Option Type", "Call Option", "Put Option"), textvariable = self.option_type, postcommand = self.run_task2)  
        self.comboboxlist_task2.current(0) # set the default Option Type
        self.comboboxlist_task2.grid(row = 8, column = 2, sticky = E)
        
        # Reset input and log
        btReset = Button(frame, width = 23, text = "Reset", command = self.ResetTask2).grid(row = 9, column = 1, columnspan = 1, sticky = E)
        
        # define run button to run the pricer
        btRun = Button(frame, width = 23, text = "Run", command = self.run_task2).grid(row = 9, column = 1, columnspan = 1, sticky = W)
        
        # define a window to display result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height = 12)
        self.logs.grid(row = 10, column = 1, rowspan = 4, columnspan = 2, sticky = W)
        
    # Implement closed-form formulas for geometric Asian call/put option.    
    def task3(self):
        
        self.__forgetFrame()
        frame = self.frame3
        frame.pack()  # Place frame3 into the window
        
        # define labels
        label_title = Label(frame, text = "Implement Closed-form Formulas for Geometric Asian Call/Put Option", fg = "red", justify = "right").grid(row = 1, column = 1,sticky = W)
        label_s0 = Label(frame, text = "Spot Price of Asset:").grid(row = 2, column = 1, sticky = W)
        label_sigma = Label(frame, text = "Implied Volatility:").grid(row = 3, column = 1, sticky = W)
        label_r = Label(frame, text = "Risk-free Interest Rate:").grid(row = 4, column = 1, sticky = W)
        label_T = Label(frame, text = "Time to Maturity (in years):").grid(row = 5, column = 1, sticky = W)
        label_K = Label(frame, text = "Strike:").grid(row = 6, column = 1, sticky = W)
        label_n = Label(frame, text = "Observation Times for the Geometric Average:").grid(row = 7, column = 1, sticky = W)
        label_OptionType = Label(frame, text = "Option Type:").grid(row = 8, column = 1, sticky = W)
        
        self.s0 = DoubleVar()
        self.sigma = DoubleVar()
        self.r = DoubleVar()
        self.q = DoubleVar()
        self.T = DoubleVar()
        self.K = DoubleVar()
        self.n = IntVar()
        self.option_type = StringVar()
        
        # define input boxes for input variables
        entry_s0 = Entry(frame, textvariable = self.s0).grid(row = 2, column = 2, sticky = E)
        entry_sigma = Entry(frame, textvariable = self.sigma).grid(row = 3, column = 2, sticky = E)
        entry_r = Entry(frame, textvariable = self.r).grid(row = 4, column = 2, sticky = E)
        entry_T = Entry(frame, textvariable = self.T).grid(row = 5, column = 2, sticky = E)
        entry_K = Entry(frame, textvariable = self.K).grid(row = 6, column = 2, sticky = E)
        entry_n = Entry(frame, textvariable = self.n).grid(row = 7, column = 2, sticky = E)
        
        # define the list for user to select option type
        self.comboboxlist_task3 = ttk.Combobox(frame, width = 17, values = ("Select Option Type", "Call Option", "Put Option"), textvariable = self.option_type, postcommand = self.run_task3)  
        self.comboboxlist_task3.current(0) # set the default Option Type
        self.comboboxlist_task3.grid(row = 8, column = 2, sticky = E)
        
        # Reset input and log
        btReset = Button(frame, width = 29, text = "Reset", command = self.ResetTask3).grid(row = 9, column = 1, columnspan = 1, sticky = E)
        
        # define run button to run the pricer
        btRun = Button(frame, width = 29, text = "Run", command = self.run_task3).grid(row = 9, column = 1, columnspan = 1, sticky = W)
        
        # define a window to display result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height = 12)
        self.logs.grid(row = 10, column = 1, rowspan = 4, columnspan = 2, sticky = W)
    
    # Implement closed-form formulas for geometric basket call/put options.
    def task4(self):
        
        self.__forgetFrame()
        frame = self.frame4
        frame.pack()  # Place frame4 into the window
        
        # define labels
        label_title = Label(frame, text = "Implement Closed-form Formulas for Geometric Basket Call/Put Option", fg = "red", justify = "right").grid(row = 1, column = 1,sticky = W)
        label_s0_1 = Label(frame, text = "Spot Price of Asset 1:").grid(row = 2, column = 1, sticky = W)
        label_s0_2 = Label(frame, text = "Spot Price of Asset 2:").grid(row = 3, column = 1, sticky = W)
        label_sigma_1 = Label(frame, text = "Volatility of Asset 1:").grid(row = 4, column = 1, sticky = W)
        label_sigma_2 = Label(frame, text = "Volatility of Asset 2:").grid(row = 5, column = 1, sticky = W)
        label_r = Label(frame, text = "Risk-free Interest Rate:").grid(row = 6, column = 1, sticky = W)
        label_T = Label(frame, text = "Time to Maturity (in year):").grid(row = 7, column = 1, sticky = W)
        label_K = Label(frame, text = "Strike:").grid(row = 8, column = 1, sticky = W)
        label_rho = Label(frame, text = "Correlation:").grid(row = 9, column = 1, sticky = W)
        label_OptionType = Label(frame, text = "Option Type:").grid(row = 10, column = 1, sticky = W)
        
        self.s0_1 = DoubleVar()
        self.s0_2 = DoubleVar()
        self.sigma_1 = DoubleVar()
        self.sigma_2 = DoubleVar()
        self.r = DoubleVar()
        self.T = DoubleVar()
        self.K = DoubleVar()
        self.rho = DoubleVar()
        self.option_type = StringVar()
        
        # define input boxes for input variables
        entry_s0_1 = Entry(frame, textvariable = self.s0_1).grid(row = 2, column = 2, sticky = E)
        entry_s0_2 = Entry(frame, textvariable = self.s0_2).grid(row = 3, column = 2, sticky = E)
        entry_sigma_1 = Entry(frame, textvariable = self.sigma_1).grid(row = 4, column = 2, sticky = E)
        entry_sigma_2 = Entry(frame, textvariable = self.sigma_2).grid(row = 5, column = 2, sticky = E)
        entry_r = Entry(frame, textvariable = self.r).grid(row = 6, column = 2, sticky = E)
        entry_T = Entry(frame, textvariable = self.T).grid(row = 7, column = 2, sticky = E)
        entry_K = Entry(frame, textvariable = self.K).grid(row = 8, column = 2, sticky = E)
        entry_rho = Entry(frame, textvariable = self.rho).grid(row = 9, column = 2, sticky = E)
        
        # define the list for user to select option type
        self.comboboxlist_task4 = ttk.Combobox(frame, width = 17, values = ("Select Option Type", "Call Option", "Put Option"), textvariable = self.option_type, postcommand = self.run_task4)  
        self.comboboxlist_task4.current(0) # set the default Option Type
        self.comboboxlist_task4.grid(row = 10, column = 2, sticky = E)
        
        # Reset input and log
        btReset = Button(frame, width = 29, text = "Reset", command = self.ResetTask4).grid(row = 11, column = 1, columnspan = 1, sticky = E)
        
        # define run button to run the pricer
        btRun = Button(frame, width = 29, text = "Run", command = self.run_task4).grid(row = 11, column = 1, columnspan = 1, sticky = W)
        
        # define a window to display result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height = 9)
        self.logs.grid(row = 12, column = 1, rowspan = 4, columnspan = 2, sticky = W)
    
    # Implement the Monte Carlo method with control variate technique for arithmetic Asian call/put options.
    def task5(self):
        
        frame = self.frame5
        self.__forgetFrame()
        frame.pack()  # Place frame5 into within the window

        label_s0 = Label(frame, text="S0").grid(row=1, column=1)
        label_sigma = Label(frame, text="sigma").grid(row=1, column=3)
        label_r = Label(frame, text="r").grid(row=2, column=1)
        label_T = Label(frame, text="T").grid(row=2, column=3)
        label_n = Label(frame, text="n").grid(row=3, column=1)
        label_K = Label(frame, text="K").grid(row=3, column=3)

        self.s0 = DoubleVar()
        self.sigma = DoubleVar()
        self.r = DoubleVar()
        self.T = DoubleVar()
        self.n = IntVar()
        self.K = DoubleVar()
        self.option_type = StringVar()
        self.ctrl_var = BooleanVar()

        entry_s0 = Entry(frame, textvariable=self.s0).grid(row=1, column=2)
        entry_sigma = Entry(frame, textvariable=self.sigma).grid(row=1, column=4)
        entry_r = Entry(frame, textvariable=self.r).grid(row=2, column=2)
        entry_T = Entry(frame, textvariable=self.T).grid(row=2, column=4)
        entry_n = Entry(frame, textvariable=self.n).grid(row=3, column=2)
        entry_K = Entry(frame, textvariable=self.K).grid(row=3, column=4)

        cbtCV = Checkbutton(frame, text="Control Variate?", variable=self.ctrl_var).grid(row=4, column=1)

        rbPut = Radiobutton(frame, text="Put", bg="red", variable=self.option_type, value='put').grid(row=4, column=2)
        rbCall = Radiobutton(frame, text="Call", bg="yellow", variable=self.option_type, value='call').grid(row=4, column=3)

        btRun = Button(frame, text="Run", command=self.run_task5).grid(row=5, column=1, columnspan=4)

        self.logs = scrolledtext.ScrolledText(frame, width = 74, height = 19).grid(row=6, column=1, columnspan=4)
        
    # Implement the Monte Carlo method with control variate technique for arithmetric mean basket call/put options. (for the case a basket with two assets)
    def task6(self):
        
        frame = self.frame6
        self.__forgetFrame()
        frame.pack()

        label_s0_1 = Label(frame, text="S0_1").grid(row=1, column=1)
        label_s0_2 = Label(frame, text="S0_2").grid(row=1, column=3)
        label_sigma_1 = Label(frame, text="sigma_1").grid(row=2, column=1)
        label_sigma_2 = Label(frame, text="sigma_2").grid(row=2, column=3)
        label_r = Label(frame, text="r").grid(row=3, column=1)
        label_T = Label(frame, text="T").grid(row=3, column=3)
        label_n = Label(frame, text="n").grid(row=4, column=1)
        label_K = Label(frame, text="K").grid(row=4, column=3)
        label_rho = Label(frame, text="rho").grid(row=5, column=1)

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

        entry_s0_1 = Entry(frame, textvariable=self.s0_1).grid(row=1, column=2)
        entry_s0_2 = Entry(frame, textvariable=self.s0_2).grid(row=1, column=4)
        entry_sigma_1 = Entry(frame, textvariable=self.sigma_1).grid(row=2, column=2)
        entry_sigma_2 = Entry(frame, textvariable=self.sigma_2).grid(row=2, column=4)
        entry_r = Entry(frame, textvariable=self.r).grid(row=3, column=2)
        entry_T = Entry(frame, textvariable=self.T).grid(row=3, column=4)
        entry_n = Entry(frame, textvariable=self.n).grid(row=4, column=2)
        entry_K = Entry(frame, textvariable=self.K).grid(row=4, column=4)
        entry_rho = Entry(frame, textvariable=self.rho).grid(row=5, column=2)


        cbtCV = Checkbutton(frame, text="Control Variate?", variable=self.ctrl_var).grid(row=6, column=1)
        
        rbPut = Radiobutton(frame, text="Put", bg="red", variable=self.option_type, value='put').grid(row=6, column=2)
        rbCall = Radiobutton(frame, text="Call", bg="yellow", variable=self.option_type, value='call').grid(row=6, column=3)

        btRun = Button(frame, text="Run", command=self.run_task6).grid(row=7, column=1, columnspan=4)

        self.logs = scrolledtext.ScrolledText(frame).grid(row=8, column=1, columnspan=4)
        
    # The Binomial Tree method for American call/put options.
    def task7(self):
        
        pass
        
    def run_homepage(self):
        
        self.__forgetFrame()
        self.frameHomePage.pack()
        
    def run_task1(self):
        
        OptionType = self.option_type.get()
        
        if OptionType == "Call Option":
            
            try:
  
                option = BSEuroOption()
                result = option.CallOption(S = self.s0.get(), sigma = self.sigma.get(), r = self.r.get(), q = self.repo.get(), T = self.T.get(), K = self.K.get())
                self.logs.insert(END, "The Call Option Premium is: {}\n".format(result))
                
            except ZeroDivisionError:
                
                self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")
                
        elif OptionType == "Put Option": 
            
            try:
            
                option = BSEuroOption()
                result = option.PutOption(S = self.s0.get(), sigma = self.sigma.get(), r = self.r.get(), q = self.repo.get(), T = self.T.get(), K = self.K.get())
                self.logs.insert(END, "The Put Option Premium is: {}\n".format(result))
            
            except ZeroDivisionError:
                
                self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")
        
        else:
            
            pass
        
        self.comboboxlist_task1.current(0)
            
    def ResetTask1(self):
        
        self.s0 = 0
        self.sigma = 0
        self.r = 0
        self.repo = 0
        self.T = 0
        self.K = 0
        
        self.task1()
        
    def run_task2(self):
        
        OptionType = self.option_type.get()
        
        if OptionType == "Call Option":
            
            try:
  
                instance = ImpliedVolatility(S = self.s0.get(), r = self.r.get(), q = self.q.get(), T = self.T.get(), K = self.K.get(), V = self.V.get())
                result = instance.CallVolatility()
                
                if math.isnan(result) or math.isinf(result):
                    
                    self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")
                    
                else:
                    
                    self.logs.insert(END, "The Implied Volatility for Call Option is: {}\n".format(result))
                
            except ZeroDivisionError:
                
                self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")
                
        if OptionType == "Put Option": 
            
            try:
            
                instance = ImpliedVolatility(S = self.s0.get(), r = self.r.get(), q = self.q.get(), T = self.T.get(), K = self.K.get(), V = self.V.get())
                result = instance.PutVolatility()
                
                if math.isnan(result) or math.isinf(result):
                    
                    self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")
                    
                else:
                    
                    self.logs.insert(END, "The Implied Volatility for Put Option is: {}\n".format(result))
            
            except ZeroDivisionError:
                
                self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")
                
        self.comboboxlist_task2.current(0)
            
    def ResetTask2(self):
                
        self.s0 = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.K = 0
        self.N = 0
        
        self.task2()
        
    def run_task3(self):
        
        OptionType = self.option_type.get()
        
        if OptionType == "Call Option":
            
            try:
  
                instance = GeoAsianOption(S = self.s0.get(), sigma = self.sigma.get(), r = self.r.get(), T = self.T.get(), K = self.K.get(), n = self.n.get())
                result = instance.CallGeoAsian()
                
                if math.isnan(result) or math.isinf(result):
                    
                    self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")
                    
                else:
                    
                    self.logs.insert(END, "The Call Option Premium is: {}\n".format(result))
                
            except ZeroDivisionError:
                
                self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")
                
        if OptionType == "Put Option": 
            
            try:
            
                instance = GeoAsianOption(S = self.s0.get(), sigma = self.sigma.get(), r = self.r.get(), T = self.T.get(), K = self.K.get(), n = self.n.get())
                result = instance.PutGeoAsian()
                
                if math.isnan(result) or math.isinf(result):
                    
                    self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")
                    
                else:
                    
                    self.logs.insert(END, "The Put Option Premium is: {}\n".format(result))
            
            except ZeroDivisionError:
                
                self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")
                
        self.comboboxlist_task3.current(0)
        
    def ResetTask3(self):
                
        self.s0 = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.K = 0
        self.n = 0
        
        self.task3()
        
    def run_task4(self):
        
        pass
    
    def ResetTask4(self):
                
        self.s0_1 = 0
        self.s0_2 = 0
        self.sigma_1 = 0
        self.sigma_2 = 0
        self.r = 0
        self.T = 0
        self.K = 0
        self.rho = 0
        
        self.task4()
        
    def run_task5(self):
        
        self.logs.insert(END, "waiting.... [It may take you several minutes]\n\n")

        option = MCArithAsianOption(s0=self.s0.get(), sigma=self.sigma.get(), r=self.r.get(),
                                    T=self.T.get(), K=self.K.get(),
                                    option_type=self.option_type.get(), ctrl_var=self.ctrl_var.get())
        result = option.pricing(num_randoms=self.n.get())
        self.logs.insert(END, "The result: {}\n".format(result))

    def run_task6(self):
        
        self.logs.insert(END, "waiting.... [It may take you several minutes]\n\n")

        option = MCArithBasketOption(s0_1=self.s0_1.get() ,s0_2=self.s0_2.get(), sigma_1=self.sigma_1.get(),
                                     sigma_2=self.sigma_2.get(), r=self.r.get(), T=self.T.get(), K=self.K.get(),
                                     rho=self.rho.get(),option_type=self.option_type.get(),
                                     ctrl_var=self.ctrl_var.get())
        result = option.pricing(num_randoms=self.n.get())
        self.logs.insert(END, "The result: {}\n".format(result))
        
    def Quit(self):
        
        self.window.destroy()

if __name__ == '__main__':
    
    Application()
