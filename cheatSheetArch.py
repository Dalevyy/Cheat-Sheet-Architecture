import tkinter as tk
import os 
from tkinter import ttk
from PIL import ImageTk, Image
from idlelib.tooltip import Hovertip
from random import randint
from binaryArithAlgos import algoStart
from conversion import forwardConvertStart

# Globals
defaultMainFrameFont = ('Times New Roman', 30, 'bold')
defaultFont = ('Times New Roman', 21)
defaultFontLine = ('Times New Roman', 21, 'underline', 'bold')
defaultFontBold = ('Times New Roman', 21, 'bold')
instructFont = ('Times New Roman', 25)
instructFontBold = ('Times New Roman', 25, 'bold')

class CheatSheetWindow(tk.Tk):  
    '''
    Decription: Default constructor for CheatSheetWindow class
    Parameters: Self
    Return Type: None
    '''
    def __init__(self):
        super().__init__()
        self.title("Cheat Sheet Architecture")

        # Setting up window size based on user's monitor
        self.width = 1280
        self.height = 720

        user_width = self.winfo_screenwidth()
        user_height = self.winfo_screenheight()

        user_x = int((user_width/2) - (self.width/2))
        user_y = int((user_height/2) - (self.height/2))
        self.geometry(f"{self.width}x{self.height}+{user_x}+{user_y}")

        self.resizable(0, 0)
        # Setting up main frame now
        self.mainFrame = MainFrame(self)

class MainFrame(ttk.Frame):
    '''
    Description: Default constructor for the MainFrame class
    Parameters: Self and the master window
    Return Type: None
    '''
    def __init__(self, master):
        super().__init__(master)
        # Create the basic properties for the mainframe
        self.frameLabel = ttk.Label(self,background='DarkBlue').pack(fill='both',expand=True)
        self.pack(fill='both', expand =True)
        self.createMainFrame(master)
    
    '''
    Description: Creates the widgets needed for the starting screen
    Parameters: Self
    Return Type: None
    '''
    def createMainFrame(self, master):
        # Start screen image label
        self.startImg = tk.PhotoImage(file=f"{os.getcwd()}/welcomeScreen.png")
        self.imgLabel = tk.Label(self, image=self.startImg)    
        
        # Four buttons for the user to interact with 
        # performBut: Button that takes user to the performance section of the app
        self.performBut = tk.Button(self, text="Performance", 
            font= defaultMainFrameFont, command=lambda: [self.destroy(), PerformFrame(master)])
        performTip = Hovertip(self.performBut, text="Click here to calculate the clock rate for \na CPU in relation to another CPU!")
        
        # instructBut: Button that goes to the MIPS instruction converter
        self.instructBut = tk.Button(self, text="Instructions", 
            font= defaultMainFrameFont, command=lambda: [self.destroy(), InstructFrame(master)])
        instructTip = Hovertip(self.instructBut, text="Click here to convert a MIPS instruction \ninto its binary and hexadecimal form!")
        
        # arithBut: Button that goes to the binary arithmetic algorithms
        self.arithBut = tk.Button(self, text="Arithmetic", 
            font= defaultMainFrameFont, command=lambda: [self.destroy(), ArithFrame(master)] )
        arithTip = Hovertip(self.arithBut, text="Click here to see how computers\ndo binary multiplication and division!")
    
        # pathBut:Button that takes user to the datapath section of the app
        self.pathBut = tk.Button(self, text= "Datapath", 
            font= defaultMainFrameFont, command=lambda: [self.destroy(), DatapathFrame(master)])
        pathTip = Hovertip(self.pathBut, text="Click here to learn the components\nof a simple CPU datapath!")

        self.mainFrameLayout()
    
    '''
    Description: Places all the widgets into the main frame 
    Parameters: Self
    Return Type: None 
    '''
    def mainFrameLayout(self):
        self.imgLabel.place(relx=0.035,rely=0.050)
        self.performBut.place(relx=0.03,rely=0.8)
        self.instructBut.place(relx=0.3,rely=0.8)
        self.arithBut.place(relx=0.56,rely=0.8)
        self.pathBut.place(relx=0.79, rely= 0.8)

class PerformFrame(ttk.Frame):
    '''
    Description: Default constructor for PerformFrame class
    Parameters: Object and the master window
    Return Type: None
    '''
    def __init__(self, master):
        super().__init__(master)
        # Create the basic properties for the mainframe
        self.frameLabel = ttk.Label(self).pack(fill='both',expand=True)
        self.pack(fill='both', expand =True)
        self.createPerformFrame(master)    

    def createPerformFrame(self, master):
        # performPrompt: Label that gives the main prompt for the performance section of app
        self.performPrompt = ttk.Label(self,text= "Find CPU B's Clock Rate by giving CPU A's" 
                                     " and CPU B's current known benchmarks.", font=defaultFont)
        
        # labelETa: Label that gives an input prompt for ET of CPU A
        self.labelETa = ttk.Label(self,text= "Enter CPU A's Execution Time (s): ", font=defaultFont)
        # valETa: Entry that takes in input for ET A 
        self.valETa = ttk.Entry(self, width=3, font=defaultFont)

        # labelETb: Label that gives an input prompt for ET of CPU B
        self.labelETb = ttk.Label(self,text= "Enter CPU B's Execution Time (s): ", font=defaultFont)
        # valETb: Entry that takes in input for ET B
        self.valETb = ttk.Entry(self, width=3, font=defaultFont)

        # labelCRa: Label that gives an input prompt for CR of CPU A
        self.labelCRa = ttk.Label(self, text="Enter CPU A's Clock Rate (GHz): ", font=defaultFont)
        # valCRa: Entry that takes in input for CR A
        self.valCRa = ttk.Entry(self, width=3, font=defaultFont)
    
        # labelCCb: Label that gives an input prompt for CC difference of CPU B
        self.labelCCb = ttk.Label(self, text="Enter CPU B's Clock Cycles Difference: ", font=defaultFont)
        # valCCb: Entry that takes in input for CC B
        self.valCCb = ttk.Entry(self, width=3, font=defaultFont)

        # calcBut: Button that will calculate the clock rate for CPU 2 based on user input
        self.calcBut = tk.Button(self, text="Calculate CR for CPU B", font = ('Times New Roman',30, 'bold'), command=lambda:[self.performCalc(master,self.valETa.get(),self.valETb.get(),self.valCRa.get(),self.valCCb.get())],state="active")
                     #command=lambda: [performCalc(performFrame,valETa.get(),valETb.get(),valCRa.get(),valCCb.get())])
        # calcButTip: Tip that tells the user what values they should input for the entries written above
        self.calcButTip = Hovertip(self.calcBut, text="Enter any number greater than 0:\nEx. ET A = 10 s, ET B = 5 s, CR A = 3 Ghz, CC B = 1.4")
        self.errorLabel = ttk.Label(self,text= f"Error! Invalid number inputted. Please try again!", font=defaultFontBold,foreground='red',background='black')
        self.errorLabel2 = ttk.Label(self,text= f"Error! Negative number inputted. Please try again!", font=defaultFontBold,foreground='red',background='black')
        # backBut: Button that returns user back to the start screen
        self.backBut = BackButton(self, master)
        self.performFrameLayout()
        
    '''
    Description: Formats the performance frame onto the app
    Parameters: Self
    Return Type: None
    '''
    def performFrameLayout(self):
        self.backBut.place(relx=0.0,rely=0.0)
        self.performPrompt.place(relx=0.025,rely=0.1)
        
        self.labelETa.place(relx=0.025,rely=0.2)
        self.valETa.place(relx=0.42,rely=0.2)

        self.labelETb.place(relx=0.025,rely=0.27)
        self.valETb.place(relx=0.42,rely=0.27)

        self.labelCRa.place(relx=0.025,rely=0.34)
        self.valCRa.place(relx=0.41,rely=0.34)

        self.labelCCb.place(relx=0.025,rely=0.41)
        self.valCCb.place(relx=0.48,rely=0.41)

        self.calcBut.place(relx=0.50,rely=0.25)

    def performCalc(self, master, aET, bET, aCR, bCC):
        # Next, do some error checking to ensure user inputted correct values
        try:
            # Convert the execution times/clock rate for CPU A into ints
            aET = int(aET)
            bET = int(bET)
            aCR = int(aCR)
            # Convert CPU's B clock cycle increase/decrease value to a float
            bCC = float(bCC)
        except:
            # If any error occurred doing type conversions, output an error prompt and let the user reinput info
            # errorLabel: Label that prints when user puts nothing/wrong input into one of the entry boxes
            self.errorLabel.place(relx=0.220,rely=0.57)
            return
        else:
            # If any of the values inputted are negative, output an error prompt letting the user know this isn't possible and ask to reinput
            if aET < 0 or bET < 0 or aCR < 0 or bCC < 0:
                # errorLabel2: Label that prints when user puts a negative number into any of the entry boxes
                self.errorLabel2.place(relx=0.220,rely=0.57)
                return
        self.errorLabel.destroy()
        self.errorLabel2.destroy()
        # performStartLabel: Label that marks the beginning of the outputted calculations
        self.performStartLabel = ttk.Label(self,text= "Steps to Perform: ", font=defaultFontLine)

        # First, get the total clock cycles for CPU A
        # firstStepLabel: Label that displays what the first step will perform      
        self.firstStepLabel = ttk.Label(self,text= "Step 1) Calculate CPU A's Clock Cycles: ", font=defaultFontBold)
        # ETA = CCA / CRA, CCA = EAA * CRA
        aCC = aET * aCR 
    
        # ccLabelA: Label that prints out the equation we will use to find CC A 
        self.ccLabelA = ttk.Label(self,text= f"Clock Cycles A = Execution Time A * Clock Rate A", font=defaultFont)
        # ccAnsLabelA: Label that prints out the value of CC A 
        self.ccAnsLabelA = ttk.Label(self,text= f"= {aET} * ({aCR}*10^9) = {aCC}*10^9 cycles", font=defaultFont)

        # Next, get the total clock cycles for CPU B
        # secondStepLabel: Label that displays what the second step will perform
        self.secondStepLabel = ttk.Label(self,text= "Step 2) Calculate CPU B's Clock Cycles: ", font=defaultFontBold)
        bCCNew = bCC * aCC

        # ccLabelB: Label that prints out the equation we will use to find CC B
        self.ccLabelB = ttk.Label(self,text= f"B Clock Cycles = {bCC} * A Clock Cycles", font=defaultFont)
        # ccAnsLabelB: Label that prints out the value of CC B
        self.ccAnsLabelB = ttk.Label(self,text= f"= {bCC} * {aCC} = {bCCNew}*10^9 cycles", font=defaultFont)

        # Finally, get the new clock rate for CPU B
        # thirdStepLabel: Label that displays what the third step will perform
        self.thirdStepLabel = ttk.Label(self,text= "Step 3) Calculate CPU B's Clock Rate: ", font=defaultFontBold)
        # ET2 = CC2 / CR2, CR2 = CC2 / ET2
        bCR = bCCNew / bET 
    
        # crLabelB: Label that prints out the equation we will use to find CR B
        self.crLabelB = ttk.Label(self,text= f"B Clock Rate = Clock Cycles / Execution Time", font=defaultFont)
        # crAnsLabelB: Label that prints out the value of CR B
        self.crAnsLabelB = ttk.Label(self,text= f"= {bCCNew}*10^9 / {bET} = ", font=defaultFont)
        self.crAnsLabel = ttk.Label(self, text=f"{bCR} GHz", font=defaultFontBold, borderwidth=7, background="orange",relief="solid")
        # tryAgainBut = Button that prompts the user to reinput new values to solve for a new CR B 
        self.tryAgainBut = tk.Button(self, text="Try Again?",font = defaultFontBold,command=lambda: [self.destroy(),PerformFrame(master)])
        # tryAgainTip = When a user's mouse is over the tryAgainButton, it will let the user know what will happen when they click the button
        self.tryAgainTip = Hovertip(self.tryAgainBut, text="Click if you want to try again\nwith new CPU benchmarks.")
        
        self.performCalcLayout()

    def performCalcLayout(self):
        self.performStartLabel.place(relx=0.025, rely=0.50)
        self.firstStepLabel.place(relx=0.025, rely=0.57)
        self.ccLabelA.place(relx=0.025, rely=0.63)
        self.ccAnsLabelA.place(relx=0.600, rely=0.63)
        self.secondStepLabel.place(relx=0.025, rely=0.69)
        self.ccLabelB.place(relx=0.025, rely=0.75)
        self.ccAnsLabelB.place(relx=0.460, rely=0.75)
        self.thirdStepLabel.place(relx=0.025, rely=0.81)
        self.crLabelB.place(relx=0.025, rely=0.87)
        self.crAnsLabelB.place(relx=0.550, rely=0.87)
        self.crAnsLabel.place(relx=0.760,rely=0.87)
        self.tryAgainBut.place(relx=0.420,rely=0.93)

class InstructFrame(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.frameLabel = ttk.Label(self).pack(fill='both',expand=True)
        self.pack(fill='both', expand =True)
        self.createInstructFrame(master) 

    def createInstructFrame(self,master):
        self.backBut = BackButton(self, master)
        # instructPrompt: Label that displays the instruction prompt for the user
        self.instructPrompt = ttk.Label(self,text= "Enter a Supported MIPS Instruction: ", font=instructFont)

        # instructStr: Entry that gets the instruction from the user 
        self.instructStr = tk.Entry(self, width=18, font=instructFont)

        # instructLearnBut: Button that takes the user to a separate window discussing MIPS formatting 
        self.instructLearnBut = tk.Button(self, text="Learn More", font=instructFontBold, command=InstructLearnWindow)
        #instructLearnBut.place(x=1000,y=60)
        # instructLearnTip: Tip that appears over the instructLearnBut to tell the user what the button will do 
        instructLearnTip = Hovertip(self.instructLearnBut, text="Click here to learn more about the MIPS instruction" 
                                "\nformats alongside which instructions are supported.")
        self.errorLabel = ttk.Label(self,text= "Error! An invalid instruction was inputted."
                                     " Please try again!", font=instructFontBold,foreground='red',background='black')
        # instructInputBut: Button Convert button for the user to confirm their input
        self.instructInputBut = tk.Button(self, text="Convert", font=instructFontBold, width = 7, command=lambda: [self.convertInstruct(master, self.instructStr)])
        # instructInputTip: Tip that appears over the instructInputBut that gives an example of what the user should input
        instructInputTip = Hovertip(self.instructInputBut, text="Enter a valid MIPS instruction.\nEx. add $s0, $s1, $s2\nEx. lw $t1, 32($t0)\nEx. j 2400")
   
        self.instructFrameLayout()

    def instructFrameLayout(self):
        self.backBut.place(relx=0.0,rely=0.0)
        self.instructPrompt.place(relx=.020,rely=0.10)
        self.instructStr.place(relx=.520,rely=0.10)
        self.instructLearnBut.place(relx=.410,rely=.01)
        self.instructInputBut.place(relx=.830,rely=0.0930)

    def convertInstruct(self, master, instruct):
        # Local lists to help output the table later
        instructFormat = ["I", "R", "J"]
        columnsR = ["OP", "RS", "RT", "RD", "SHAMT", "FUNCT"]
        columnsI = ["OP", "RS", "RT", "Immediate"]
        columnsJ = ["OP", "Address"]

        # Next, convert the instruction by going to the conversion.py file starting
        # in the forwardConvertStart function
        bStr, hStr, instructLst, ogLst = forwardConvertStart(instruct.get())

        # Now check if any error was returned by the conversion.py file
        # If there was, don't output anything to the screen and ask the user to try again
        if bStr == -1:
            # errorLabel: Label that outputs an error was found with the user inputted instruction
            self.errorLabel.place(relx=0.075,rely=0.200)
            return
        self.errorLabel.destroy()
        # If we have a valid instruction, then print out the correct table
        # First, if we have an OP != 0 and the instruction doesn't have two parts to it, print out 
        # the table for an I-Format instruction
        if instructLst[0] != '000000' and len(ogLst) != 2:
            self.instructCreateTable(instructLst, ogLst, columnsI, instructFormat[0])
        # Next if our instruction list has exactly 6 elements in it, then we know we have to print
        # out a R-Format instruction table
        elif len(instructLst) == 6:
            self.instructCreateTable(instructLst, ogLst, columnsR, instructFormat[1])
        # Finally if neither of the above conditions are met, we need to print out a J-Format
        # instruction table
        else:
            self.instructCreateTable(instructLst, ogLst, columnsJ, instructFormat[2])
    
        # binaryLabel: Label that prints the prompt for the binary instruction
        self.binaryLabel = ttk.Label(self,text= "Binary Instruction: ", font=instructFontBold)
        # outputB: Label that outputs the binary instruction to the user
        self.outputB = ttk.Label(self,text= bStr, font=instructFont)

        # hexLabel: Label that prints the prompt for the hex instruction
        self.hexLabel = ttk.Label(self,text= "Hex Instruction: ", font=instructFontBold)
         # outputH: Label that outputs the hex instruction to the user 
        self.outputH = ttk.Label(self,text= "0x" + hStr, font=instructFont, borderwidth=7, background="orange",relief="solid")

        # tryAgainInstructBut: Button that prompts the user to try inputting a different instruction to conver instead
        self.tryAgainBut = tk.Button(self, text="Try Again?",font = instructFontBold,command=lambda: [self.destroy(),InstructFrame(master)])
        # tryAgainInstructTip: Tip that hovers over the tryAgainInstructBut to let user know what the button will do 
        tryAgainTip = Hovertip(self.tryAgainBut, text="Click if you want to try to convert \na different MIPS instruction instead.")

        self.instructAdditionalLayout()
    
    def instructAdditionalLayout(self):
        self.binaryLabel.place(relx=.050, rely=.700)
        self.outputB.place(relx=.340, rely=.700)
        self.hexLabel.place(relx=.090, rely=.760)
        self.outputH.place(relx=.340, rely=.760)
        self.tryAgainBut.place(relx=0.375,rely=.850)

    def instructCreateTable(self, instructLst, ogLst, columnLst, instructType):
        # tableLabel: Label that prints out the type of instruction the user inputted
        tableLabel = ttk.Label(self,text= f"{instructType}-Format Instruction", font=instructFontBold)
        tableLabel.place(relx=0.375,rely=.230)

        # For loop that will help print out each label needed for the table by column
        for i in range(len(columnLst)):
            # First Label: Prints out the column name 
            ttk.Label(self,text= columnLst[i], font=instructFont).place(x=100+200*i,y=250)
            # Second Label: Prints out the original element of the instruction
            ttk.Label(self,text= ogLst[i], font=instructFont).place(x=100+200*i,y=300)
            # Third Label: Prints out the decimal element of the instruction
            ttk.Label(self,text= int(instructLst[i],2), font=instructFont).place(x=100+200*i,y=350)
            # Fourth Label: Prints out the binary element of the instruction
            ttk.Label(self,text= instructLst[i], font=instructFont).place(x=100+200*i,y=400)
        
        # SPECIAL CASE: SRL/SLL need to replace the RS and SHAMT values
        if(instructType == 'R' and (ogLst[5] == 'srl' or ogLst[5] == 'sll')):
            # First Label will replace RS to be 0 (since RS == 0 for shift instructions)
            ttk.Label(self,text= '0    ', font=instructFont).place(x=300,y=300)
            # Second Label will make SHAMT equal to the number of bits we are shifting
            ttk.Label(self,text= ogLst[2], font=instructFont).place(x=900,y=300)

class ArithFrame(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)        
        self.frameLabel = ttk.Label(self).pack(fill='both',expand=True)
        self.pack(fill='both', expand =True)
        self.createArithFrame(master) 
    
    def createArithFrame(self,master):
        self.backBut = BackButton(self, master)
        # arithPrompt: Label that askes a user to choose an algorithm they want to see
        self.arithPrompt = tk.Label(self, text="Choose an Algorithm to Perform:", font=defaultFontBold)
        
        # algos: Tuple containing the four main algos for this part of the program
        algos = ("","64-Bit ALU Multiplication", "32-Bit ALU Multiplication",
                      "64-Bit ALU Division", "32-Bit ALU Division")
        # Setting the default option to be 64-BIT ALU Multiplication
        algo = tk.StringVar(self)
        algo.set(algos[1])
        # algoChooser: Option menu that allows user to choose which algo they want to see performed
        self.algoChooser = ttk.OptionMenu(self, algo, *algos, command =lambda x: self.performArith(x, master))
        self.arithFrameLayout()

    def arithFrameLayout(self):
        self.backBut.place(relx=0.0, rely=0.0)
        self.arithPrompt.place(relx=0.025,rely=0.1)
        self.algoChooser.place(relx=0.140,rely=0.18)

    def performArith(self, algoType, master):
        # Must write here to be able to destroy later 
        errLabel = ttk.Label(self,font=defaultFontBold, text=f"Error! A number was not inputted. Please try again!",foreground='red',background='black')
        errLabel2 = ttk.Label(self, font=defaultFontBold, text=f"Error! A negative number was inputted. Please try again!",foreground='red',background='black')
        errLabel3 = ttk.Label(self,font=defaultFontBold, text=f"Error! Number exceeds 4-bit length. Please try again!", foreground='red',background='black')
        
        divInput1 = ttk.Label(self,text= "Enter Base-10 Dividend:      ", font=defaultFont)
        divInput2 = ttk.Label(self,text= "Enter Base-10 Divisor:     ", font=defaultFont)
        mulInput1 = ttk.Label(self,text= "Enter Base-10 Multiplicand: ", font=defaultFont)
        mulInput2 = ttk.Label(self,text= "Enter Base-10 Multiplier: ", font=defaultFont)

        # First, checking to see if the user wants to perform a division algo
        if algoType == "64-Bit ALU Division" or algoType == "32-Bit ALU Division":
            mulInput1.destroy()
            mulInput2.destroy()
            # If so, first output the dividend label for the user 
            divInput1.place(relx=0.500,rely=0.1)
            # Next output the divisor label 
            divInput2.place(relx=0.500, rely=0.18)
        # If not, the user wants to see a multiplication algo
        else: 
            divInput1.destroy()
            divInput2.destroy()
            # First output the multiplicand label 
            mulInput1.place(relx=0.500,rely=0.1)
            # Then output the multiplier label
            mulInput2.place(relx=0.500, rely=0.18)
        
        # Next, set up the entry boxes for the user to input numbers into 
        # Entry box 1 for dividend/multiplicand input 
        num1 = tk.Entry(self, width=5, font=defaultFont)
        num1.place(relx=0.820,rely=0.1)
        # Entry box 2 for divisor/multiplier input
        num2 = tk.Entry(self, width=5, font=defaultFont)
        num2.place(relx=0.800,rely=0.18)

        # Then set the correct algoToUse field to make sure the correct algorithm is performed when the user hits the algoButton below
        algoSelect = {"64-Bit ALU Multiplication": "m64", "32-Bit ALU Multiplication": "m32", "Booth's Algorithm": "mB",
                  "64-Bit ALU Division": "d64", "32-Bit ALU Division": "d32"}
        algoToUse = algoSelect[algoType]

        performDivBut = tk.Button(self, text="Quotient", font= defaultFontBold, command=lambda: [algoStart(num1.get(),num2.get(),self, algoToUse, errLabel, errLabel2, errLabel3), self.tryAgain(master)])
        performMultBut = tk.Button(self, text="Product", font= defaultFontBold, command=lambda: [algoStart(num1.get(),num2.get(),self, algoToUse, errLabel, errLabel2, errLabel3), self.tryAgain(master)])

        # Now, figure out which algo the user chose to set up the button to perform the correct algo
        # If the user selected any division algo, set up the button to say "Quotient"
        if algoToUse == "d64" or algoToUse == "d32":
            performMultBut.destroy()
            # performDivBut: Button that will perform binary division when clicked
            performDivBut.place(relx=0.650,rely=0.02, relheight=0.05, relwidth=0.15)
            # divTip: Tip that displays what the performDivBut will do
            divTip = Hovertip(performDivBut, text= "Enter two unsigned numbers less than 16. \nEx. Dividend = 5, Divisor = 3")
        # Else set up the button to say "Product" instead 
        else:
            performDivBut.destroy()
            # performMultBut: Button that will perform binary multiplication when clicked
            performMultBut.place(relx=0.650,rely=0.02, relheight=0.05, relwidth=0.15)           
            # multTip: Tip that displays what the performMultBut will do
            multTip = Hovertip(performMultBut, text= "Enter two unsigned numbers less than 16. \nEx. Multiplicand = 5, Multiplier = 3")
    
    def tryAgain(self,master):
        # tryAgainBut = Button that prompts the user to reinput new values to solve for a new CR B 
        self.tryAgainBut = tk.Button(self, text="Try Again?",font = defaultFontBold,command=lambda: [self.destroy(),ArithFrame(master)])
        self.tryAgainBut.place(relx=0.5,rely=0.9)
        # tryAgainTip = When a user's mouse is over the tryAgainButton, it will let the user know what will happen when they click the button
        self.tryAgainTip = Hovertip(self.tryAgainBut, text="Click if you want to calculate another \nexpression with a different algorithm.")

class DatapathFrame(ttk.Frame):
    '''
    Description: Default constructor for the DatapathFrame class
    Parameters: Frame object followed by the root window
    Return Type: Frame containing a datapath for the user
    '''
    def __init__(self,master):
        super().__init__(master)
        self.pack(fill='both', expand =True)
        self.datapathImg = tk.PhotoImage(file=f"{os.getcwd()}/datapathDiagram.png")
        self.createDatapathFrame(master)

    def createDatapathFrame(self, master):
        self.BackBut = BackButton(self,master)
        
        # Setting up the top portion of the frame to ask the user to input 
        # the correct number that corresponds to the following CPU components
        pathComponents = ["Program Counter", "Instruction Memory", "RegDst Mux", "Register File", "Sign Extend",
                      "ALUSrc Mux", "ALU", "Data Memory", "MemToReg Mux", "Branch Mux", "Jump Mux"]
        # Using RNG to determine which component the user will be prompted to locate
        cpuComponent = randint(0,10)
        pathText = f"Enter a number where the following CPU component is located on the diagram: "
        # pathLabel: Label representing the input prompt for the datapath section
        self.pathLabel = ttk.Label(self,text=pathText, font=defaultFont)
        self.randomComponent = ttk.Label(self,text=f"{pathComponents[cpuComponent]}",font=defaultFontBold)
        # cpuNum: Entry Box that allows a user to input a number that corresponds to the number on the CPU diagram
        self.cpuNum = ttk.Entry(self, width=3, font=defaultFont)
        # imgLabel: Label that outputs the complete simple CPU datapath to the frame 
        self.imgLabel = ttk.Label(self, image=self.datapathImg)

        # pathEnterBut: Button that user clicks which determines whether or not the user inputted the correct number
        self.pathEnterBut = tk.Button(self, text="Enter", font = defaultFontBold, command=lambda: [self.datapathCheck(master, self.cpuNum.get(),cpuComponent,pathComponents)])
        # pathEnterTip: Tip that informs user what pressing the pathEnterBut will do 
        pathEnterTip = Hovertip(self.pathEnterBut, text="Enter a number between 1-11\nEx. Entering 1 chooses the component labeled 1 on diagram")

        # learnBut: Button that opens a new window for the user to learn about the different components of a CPU
        self.learnBut = tk.Button(self, text="Learn More", font = defaultFontBold,command= DatapathLearnWindow)
        # learnTip: Tip that tells the user they can learn more about the current CPU component by pressing the button
        learnTip = Hovertip( self.learnBut, text=f"If you would like to first learn more\nabout the {pathComponents[cpuComponent]}, click here!")

        self.notAnIntLabel = ttk.Label(self,text= "Error! A non-integer value\n        was inputted.\n     Please try again!", font=defaultFont)
        self.invalidRangeLabel = ttk.Label(self,text="Error! Number exceeds\n   the valid range(1-11).\n       Please try again!", font=defaultFont)
        self.incorrectPathLabel = ttk.Label(self,text= f"Error! Wrong Component\nSelected. Please try Again!", font=defaultFont)  

        self.datapathFrameLayout()

    def datapathFrameLayout(self):
        self.BackBut.place(relx=0.0, rely=0.0)
        self.pathLabel.place(relx=0.025, rely=0.08)
        self.randomComponent.place(relx=0.745,rely=0.15)
        self.cpuNum.place(relx=0.730, rely=0.22)
        self.pathEnterBut.place(relx=0.800, rely=0.21)        
        self.learnBut.place(relx=.410,rely=.01)
        self.imgLabel.place(relx=0.025, rely=0.14)
 
    def datapathCheck(self, master, userNum, correctNum, components):
         # Next, we will do some error checking to see if we have valid input
        try:
            # inputtedNum is passed as a string, so convert it into an integer
            userNum = int(userNum)
        except:
            # If inputtedNum can't be converted into an integer, output an error message
            # notAnIntLabel: Label that outputs a conversion error to the user, prompting them to reinput 
            self.notAnIntLabel.place(relx=0.690, rely=0.500)
            return 
        else:
            # If inputtedNum can be converted into an int, then check whether or not the number is in the range of 1-11 inclusively
            if userNum < 1 or userNum > 11:
                # If it isn't, then output an error
                # invalidRangeLabel: Label that outputs an invalid range error to the user, asking them to reinput 
                self.invalidRangeLabel.place(relx=0.690, rely=0.500)
                return
        self.notAnIntLabel.destroy()
        self.invalidRangeLabel.destroy()
        # Finally, if error checking is passed... then check to see if the user chose the correct CPU component or not
        # This is done by checking if the inputtedNum corresponds to the right CPU component in the pathComponents list by checking cpuComponent + 1
        if(userNum != correctNum+1):
            # If not, output an error message and let the user try again
            # incorrectPathLabel: Label that prints out text saying the user did not input the correct value and asks them to retry 
            self.incorrectPathLabel.place(relx=0.690, rely=0.500)
        else:
            self.incorrectPathLabel.destroy()
            # Else, output a message saying the user chose the correct CPU component
            # correctPathLabel: Label that prints out text saying the user correctly chose the right input 
            self.correctPathLabel1 = ttk.Label(self,text= f"Correct! You chose the ", font=defaultFont)  
            self.correctPathLabel1.place(relx=0.710, rely=0.500)
            self.correctPathLabel2 = ttk.Label(self,text= f"{components[userNum-1]}!", font=defaultFontBold)
            self.correctPathLabel2.place(relx=0.730, rely=0.550)

            # tryAgainButton: Button that prompts the user to locate a different CPU component on the diagram without having to refresh the page
            self.tryAgainButton = tk.Button(self, text="Try Again?",font = defaultFontBold,command=lambda: [self.destroy(),DatapathFrame(master)])
            self.tryAgainButton.place(relx=0.750, rely=0.650)
            # tryAgainTip: When a user's mouse is over the tryAgainButton, it will tell the user the button will refresh the page to repeat the process
            self.tryAgainTip = Hovertip( self.tryAgainButton, text="Click if you want to locate a \ndifferent CPU component on the diagram.")

class ScrollFrame(ttk.Frame):
    def __init__(self, window, output):
        super().__init__(master= window)
        self.pack(expand= True, fill= 'both')
        # Need to use canvas for scrolling so here we are 
        self.canvas = tk.Canvas(self, background= 'blue', scrollregion= (0,0,1600,900))
        self.canvas.pack(expand= True, fill = 'both')

        self.frame = ttk.Frame(self)
        # Use labels to output the text into the app 
        for i in range(len(output)):
            tk.Label(self.frame,text= output[i], font=defaultFont).place(x=30, y=50+50*i)
        self.canvas.create_window((0,0), window= self.frame, anchor= 'nw', width = 1600, height=900)

        # Okay so this is for Linux mouse binds (4-UP, 5-Down)
        self.canvas.bind_all('<Button-4>', lambda event: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all('<Button-5>', lambda event: self.canvas.yview_scroll(1, "units"))

class InstructLearnWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Learn about the MIPS Instruction Set Architecture!")
        self.geometry("1000x600")
        # Get the text from a separate file
        instructLearnLst = [line for line in open("instructLearnInfo.txt", 'r')]
        
        learnScrollFrame = ScrollFrame(self, instructLearnLst)
                
class DatapathLearnWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1450x670") 
        self.title("Learn about the components of a CPU!")
        # learnStartLabel: Label that informs users the following list gives the components of a CPU
        learnStartLabel = ttk.Label(self,text= "This is a list of the eleven main components of a CPU.", font=defaultFontBold)
        learnStartLabel.place(x=20, y=35)

        # Get the text from a separate file
        learnInfo = [line for line in open("pathLearnInfo.txt", 'r')]

        # For each line, create a label to output it to the window 
        for i in range(len(learnInfo)):
            ttk.Label(self,text= f"{i+1}) " + learnInfo[i], font=defaultFont).place(x=30, y=100+50*i)

'''
BackButton creates a back button for the user that will destroy the 
current frame and return the user back to the start screen 
'''
class BackButton(tk.Button):
    '''
    Description: Default constructor for the BackButton class
    Parameters: It will take the button itself, the current frame the
    button will be put into, and the root window
    Return Type: Returns back button to caller 
    '''
    def __init__(self, currFrame, master):
        super().__init__(currFrame,text="Back", font= defaultFontBold,command=lambda: [currFrame.destroy(), MainFrame(master)])
        self.backTip = Hovertip(self,text= "Go back to the start screen")
        
'''
Description: Main function for Cheat Sheet Architecture
Parameters: None
Return Type: Int (0)
'''
if __name__ == "__main__":
    root = CheatSheetWindow()
    root.mainloop()
