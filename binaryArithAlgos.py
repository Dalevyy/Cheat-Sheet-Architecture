'''
This file contains the algorithms needed to perform binary multiplication
and division for the Cheat Sheet GUI application
'''
import tkinter as tk
from tkinter import ttk

# Globals
defaultFont = ('Times New Roman', 15)
defaultFontBold = ('Times New Roman', 21, 'bold')

'''
Description: Prints out the table row by row
Parameters: Passing in the arithmetic frame widget, the list containing the values needing to be printed,
the current row we are printing to, the starting index of the list, and how many values to print
Return Type: None
'''
def printTable(aFrame, algoVals, rowCount, startIndex, numToPrint):
    # For each value in algoVals starting at startIndex
    # Create a new label, add it to our label list, and format the label into the table
    for i in range(startIndex, numToPrint):
        colLabel = ttk.Label(aFrame, font=defaultFont, text=f"{algoVals[i]}")
        colLabel.place(x=20+i*270, y = 185+(rowCount*30))

'''
Description: Performs either 64-Bit or 32-Bit ALU multiplication
Parameters: Two binary strings that represent the multiplicand and 
multiplier we are using 
Return Type: None 
'''
def mulAlgo(bMcand, bMplier, aFrame, algoType):
    rowCount = 0 
    stepCount = 4
    
    # Initializing Multiplier, Multiplicand, and Product variables
    product = '00000000'
    # If we need to perform 64-Bit ALU multiplication, make the mcand
    # an 8-bit number
    if algoType == 'm64':
        mcand = '0000' + bMcand 
    # Otherwise, keep it to 4 bits 
    else:
        mcand = bMcand 

    # Setting up variables to use for the table. Use a tuple for the column names
    # and use a list to keep track of each variable's values
    columnNames = ("Iteration", "Action", "Multiplier", "Multiplicand", "Product")
    algoVals = [0, "Initialize", f"{bMplier}", f"{mcand}", f"{product}"]
    
    # Print starting values 
    printTable(aFrame, columnNames, rowCount, 0, len(columnNames))
    rowCount += 1
    printTable(aFrame, algoVals, rowCount, 0, len(algoVals))
    rowCount += 1

    # Loop that will iterate through each step of the chosen mul algo 
    for i in range(stepCount):
        # Update the step we're on with each iteration
        algoVals[0] += 1

        # ACTION 1 START 
        # For BOTH algos:
        # Action 1) Check the LSB of the multiplier
        # 0 == NOP 
        # 1 == P + MCAND for 64-Bit Division, P + MCAND in LEFT HALF P for 32-Bit Division
        product = checkLSB(product, bMplier, mcand, algoVals, algoType)
        
        printTable(aFrame, algoVals, rowCount, 0, len(algoVals))
        rowCount += 1

        # ACTION 2 Start
        # 64-Bit Multiplication:
        # Action 2) Shift MCAND left 1 bit
        if algoType == 'm64':
            mcand = mcand[1:] + '0'
            algoVals[1] = "2) SLL Mcand"
            algoVals[3] = mcand
        # 32-Bit Multiplication:
        # Action 2) Shift product right 1 bit
        else:
            product = '0' + product[:-1]
            algoVals[1] = "2) SRL P"
            algoVals[4] = product 

        printTable(aFrame, algoVals, rowCount, 1, len(algoVals))
        rowCount += 1

        # ACTION 3 Start 
        # For BOTH algos:
        # Action 3) Shift MPLIER right 1 bit
        bMplier = '0' + bMplier[:-1]
        algoVals[1] = "3) SRL Mplier"
        algoVals[2] = bMplier

        printTable(aFrame, algoVals, rowCount, 1, len(algoVals))
        rowCount += 1
        
'''
Description: Performs either 64-Bit or 32-Bit ALU division
Parameters: Two binary strings that represent the dividend and
divisor we are using
Return Type: None 
'''
def divAlgo(bDvdend, bDvsor, aFrame, algoType):
    rowCount = 0 
    # Initializing Quotient, Divisor, and Remainder variables 
    quotient = '0000'
    remainder = '0000' + str(bDvdend)
    newRemainder = ''
    stepCount = 4   # stepCount: Variable that will count amount of steps to perform 
    # Determining whether or not divisor needs to be 8-bits or 4-bits long
    # If we're using the 64-bit ALU, it will be 8 bits
    # Else, it will be 4-bits long so don't change it
    if algoType == 'd64':
        bDvsor = bDvsor + '0000'
        stepCount += 1
    
    # Setting up variables to use for the table. This includes using a tuple to help
    # print out the column names alongside a list that will store the step, action, 
    # and current values for all of our variables
    columnNames = ("Iteration", "Action", "Quotient", "Divisor", "Remainder")
    algoVals = [0, "Initialize", f"{quotient}", f"{bDvsor}", f"{remainder}"]

    printTable(aFrame, columnNames, rowCount, 0, len(columnNames))
    rowCount += 1
    printTable(aFrame, algoVals, rowCount, 0, len(algoVals))
    rowCount += 1
    
    # Loop that will iterate through each step of the chosen div algo 
    for i in range(stepCount):
        # Update the step we're on with each iteration
        algoVals[0] += 1

        # ACTION 1 START 
        # If we are performing a 64-bit ALU division
        # Action 1) Remainder = Remainder - Divisor 
        if algoType == 'd64':
            # Call the subRemainder function to get the new remainder 
            newRemainder = subRemainder(remainder, bDvsor, algoType)
            algoVals[1] = "1) R - Dvsor"
            algoVals[4] = newRemainder
        # Else if we are performing a 32-bit ALU division
        # Action 1) Shift remainder to the left 1 bit
        else:
            remainder = remainder[1:] + '0'
            algoVals[1] = "1) SLL R"
            algoVals[4] = remainder 
        
        # Print table after ACTION 1 
        printTable(aFrame, algoVals, rowCount, 0, len(algoVals))
        rowCount += 1 # Update rowCount at the end of ACTION 1

        # ACTION 2 START 
        # 64-Bit ALU Division:
        # Step 2) Check MSB of remainder
        if algoType == 'd64':
           remainder, quotient = checkMSB(quotient, newRemainder, remainder, algoVals, algoType)
        # 32-Bit ALU Division:
        # Step 2) LH Remainder - Divisor 
        else:
            newRemainder = subRemainder(remainder, bDvsor, algoType)
            algoVals[1] = "2) LH R - Dvsor"
            algoVals[4] = newRemainder + remainder[4:]

        # Print table after ACTION 2 
        printTable(aFrame, algoVals, rowCount, 1, len(algoVals))
        rowCount += 1 # Update rowCount at the end of ACTION 2

        # ACTION 3 START
        # 64-BIT ALU Division:
        # Step 3) Shift divisor right 1 bit
        if algoType == 'd64':
            bDvsor = '0' + bDvsor[:-1]
            algoVals[1] = "3) SRL Dvsor"
            algoVals[3] = bDvsor  
        # 32-BIT ALU Division:
        # Step 3) Check MSB of remainder
        else:
            remainder, quotient = checkMSB(quotient, newRemainder, remainder, algoVals, algoType)
           
        # Print table after ACTION 3
        printTable(aFrame, algoVals, rowCount, 1, len(algoVals))
        rowCount += 1 # Update rowCount at the end of ACTION 3

'''
Descriptions: Performs Action 1 of the 64-Bit and 32-Bit ALU Multiplication algos
by checking the LSB and seeing if we need to add P + Mcand or not
Parameters: Product, multiplier, and multiplicand binary strings alongside the list 
storing the output values and the algorithm we are performing
Return Type: Binary string representing our new product 
'''
def checkLSB(product, bMplier, mcand, algoVals, algoType): 
    # If LSB == 0 : NOP
    if bMplier[3] == '0':
        # Use ACTION A output no matter which algo we ahve
        algoVals[1] = "1a) NOP"
    # If LSB == 1 : P + Mcand 
    else: 
        # If we are performing 32-Bit Multiplication, add the new product to 
        # the left half of the current product 
        if algoType == 'm32':
            newProduct = int(product[:4],2) + int(mcand,2)
            newProduct = format(newProduct, 'b')
            algoVals[1] = "1b) P + Mcand in LH P"
            product = newProduct + product[4:]
        # Else, just set the new product to be the current product for 64-Bit Multiplication
        else:
            # Add product and multiplicand together/convert back into binary
            newProduct = int(product,2) + int(mcand,2)  
            newProduct = format(newProduct, 'b')
 
            algoVals[1] = "1b) P + Mcand"
            product = newProduct 
        # Add any trailing 0's 
        for j in range(8-len(product)):
            product = '0' + product
    
    algoVals[4] = product 
    return product 
    
'''
Description: Checks the MSB for division algos 
Parameters: The current remainder we are checking the MSB for and 
the old remainder 
Return Type: Binary string that represents our current remainder
'''
def checkMSB(quotient, newRemainder, remainder, algoVals, algoType):
    # If MSB = 0 : SL quotient 1 bit/LSB = 1
    if newRemainder[0] == '0':
        # Use the correct ACTION A output based on the chosen algo
        if algoType == 'd64':
            algoVals[1] = "2a) SL Q/LSB=1"
            remainder = newRemainder 
        else:
            algoVals[1] = "3a) SL Q/LSB=1"  
            remainder = newRemainder + remainder[4:]
        # Set quotient's last bit to be 1 
        quotient = quotient[1:] + '1'
    # If MSB = 1 : SL quotient 1 bit/LSB = 0, revert to original remainder
    else:
        # Use the correct ACTION B output based on the chosen algo
        if algoType == 'd64':
            algoVals[1] = "2b) SL Q/LSB=0"
        else:
            algoVals[1] = "3b) SL Q/LSB=0"
        # Set quotient's last bit to be 0
        quotient = quotient[1:] + '0'
    # Set new values quotient/remainder in algoVals
    algoVals[2] = quotient 
    algoVals[4] = remainder 

    return remainder, quotient 

'''
Description: Performs Remainder - Dvsor for 64-bit ALU division OR LH Remainder -
Dvsor for 32-bit ALU division
Parameters: Pass the current remainder/divisor alongside which algo we are using
Return Type: Binary string representing the new remainder
'''
def subRemainder(remainder, bDvsor, algoType='d32'):
    bitCount = 8    # Set default bit length to be 8
    # First check if we are using the 32-bit ALU division algo
    # If so, we need to splice the remainder to only use the first
    # 4 bits and set bitCount to 4
    if algoType == 'd32':
        remainder = remainder[0:4]
        bitCount = 4
    
    # Then, convert the binary values into integers to make life easier
    # and subtract Dvsor from remainder
    remainder = int(remainder, 2)
    dvsor = int(bDvsor, 2)
    if(remainder >= dvsor):
        remainder -= dvsor 
    else:
        bDvsor = twosComplement(dvsor, algoType)
        remainder += int(bDvsor, 2)
    # Now, check whether or not we need to make remainder two's complement or not
    if(remainder < 0):
       remainder = twosComplement(remainder)
    # If not, convert back into binary and add appropriate zeroes
    else:
        remainder = format(remainder, 'b')
        for j in range(bitCount-len(remainder)):
            remainder = '0' + remainder

    # Return the new remainder back to the algo
    return remainder 

'''
Description: Converts decimal numbers into binary numbers
Parameters: Two base-10 numbers alongside the arithmetic frame 
Return Type: -1 if an error occurred or a binary string 
'''
def binaryConvert(num, num2, aFrame, errLabel3):

    # First make sure numbers don't exceed bit length
    if num > 15 or num2 > 15:
        # errLabel3: Label that outputs an error if user inputted a number equal or greater than 16
        errLabel3.place(x=60, y=200)
        return -1, -1
    errLabel3.destroy()
    # If bit length is good, then convert the first number into its binary version
    # and do a sign extend to reach 4 bits
    bNum1 = format(num, 'b')
    for i in range(4-len(bNum1)):
        bNum1 = '0' + bNum1
    # Likewise, convert the second number into its binary version and do a sign extend
    # to reach 4 bits
    bNum2 = format(num2, 'b')
    for i in range(4-len(bNum2)):
        bNum2 = '0' + bNum2

    return bNum1, bNum2, 

'''
Description: Converts a number into its signed binary representation via two's complement
Parameters: Two numbers at most 
Return Type: At most two binary strings
'''
def twosComplement(num, algoType='0'):
    bitCount = 4    # Default bit count that represents length of binary string

    # Convert number into binary 
    num = format(num, 'b')
    # If the passed algoType is m64 or d64, then we have to set the bitCount to be 8
    if algoType == 'm64' or algoType == 'd64':
        bitCount = 8
    # Add leading 0's to the binary string if we haven't reached the bitCount
    for i in range(bitCount-len(num)):
        num = '0' + num
    # Find the first instance of a "1" starting from the right of the string and splice 
    # the binary string to only include that 
    rOne = num.rfind('1')
    twosC = num[rOne:]

    # Iterate through the number of digits left before the last occurrence of "1'"
    for i in range(rOne-1,-1,-1):
        # If we have a 0, flip the bit to 1 
        if num[i] == '0':
            twosC = '1' + twosC
        # Else if we have a 1, flip the bit to 0
        else:
            twosC = '0' + twosC 

    return twosC

'''
Description: Start of the binary arithmetic portion of the app
Parameters: Current dividend/divisor we're working with, the arithmetic frame
where we will print the algo out to, and the type of algo we need to perform
Return Type: None
'''
def algoStart(num1, num2, aFrame, algoType, errLabel, errLabel2, errLabel3):

    # First, do error checking 
    try:
        # Convert each number into an int
        num1 = int(num1) 
        num2 = int(num2)
    except:
        # errLabel: label that displays whenever a user inputs a non-integer value into the entry
        errLabel.place(x=60, y=200)
        return 
    else:
        # If numbers were converted into ints, now check if any of the two are negative
        if num1 < 0 or num2 < 0:
            # errLabel2: Label that displays whenever a user inputted a negative number into the entry
            errLabel2.place(x=60, y=200)
            return 
    errLabel.destroy()
    errLabel2.destroy()
    # First, convert the two passed numbers into binary 
    bNum1, bNum2 = binaryConvert(num1, num2, aFrame, errLabel3)
    if bNum1 == -1:
        return
    
    # Then check which algo was passed to the function to make sure the proper algo is chosen
    if algoType == "d64" or algoType == "d32":
        divAlgo(bNum1, bNum2, aFrame, algoType)
    else:
        mulAlgo(bNum1, bNum2, aFrame, algoType)
    