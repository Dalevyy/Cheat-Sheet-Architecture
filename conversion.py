'''
This file converts a passed MIPS instruction into its corresponding binary
and hexadecimal forms for the Cheat Sheet GUI application
'''

'''
Description: Converst the decimal values of an instruction into its binary/hex equivalent
Parameters: Passing in a list that contains decimal values
Return Type: None
'''
def convert(lstInstruct):
    # For loop to go through the entire list of instruction fields
    for i in range(len(lstInstruct)):
        # Convert each decimal value to its binary equivalent
        lstInstruct[i] = format(lstInstruct[i], 'b')
    # Call addZeroes to add any leading zeroes
    addZeroes(lstInstruct)
    # Join the list into a singular string and do the hex conversion
    bStr = ''.join(lstInstruct)
    return bStr, hexConvert(bStr)
    # print(f"\nBinary Instruction: {bStr}")
    # print(f"Hex Instruction: 0x{hexConvert(bStr)}")

'''
Description: Converts a binary string into a hexadecimal number
Parameter: String that represents a binary value
Return Type: String (which is formatted as a hex number)
'''
def hexConvert(bStr):
    hexNum = ''
    index = 0
    # hex: Dict that contains keys for each digit in hex
    hex = {0:'0',1:'1', 2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10: 'A', 11:'B',12:'C',13:'D',14:'E',15:'F'}
    # For loop that checks each 4 bits in a string of 32-bit chars
    for i in range(8):
        # Isolate the current 4-bit string
        fourDigit = bStr[index:index+4]
        # Conver the string into a number
        num = int(fourDigit, 2)
        # Find the corresponding hex value in the hex dict and concatenate it to our string
        for i in hex:
            if i == num:
                hexNum += hex[i]
        # Update index each iteration to get the next 4-bit string
        index += 4
    return hexNum

'''
Description: Adds leading zeroes to binary numbers
Parameters: List containing the fields of each instruction in binary
Return Type: None
'''
def addZeroes(binInstruct):
    # Loop through the length of passed instruction
    for i in range(len(binInstruct)):
        # First, zero fill the op code and funct code
        if i == 0 or i == 5:
            binInstruct[i] = binInstruct[i].zfill(6)
        # Then, check if you have an R-Format instruction to zero fill the registers 
        elif binInstruct[0] == '000000':
            binInstruct[i] = binInstruct[i].zfill(5)
        # Then, check if you have an I-Format instruction to zero fill the two registers
        elif len(binInstruct) != 2 and (i == 1 or i == 2):
            binInstruct[i] = binInstruct[i].zfill(5)
        # Check if instruction has a length of 2 which means we have to zero fill the address field
        elif len(binInstruct) == 2:
            binInstruct[i] = binInstruct[i].zfill(26)
        # Check if instruction has a length of 4 which means we have to zero fill the IMM field
        elif len(binInstruct) == 4:
            binInstruct[i] = binInstruct[i].zfill(16)

'''
Description: Checks what type of instruction was inputted and sees if it's valid or not
Parameters: String that represents our instruction
Return Type: A list of ints containing the correct decimal values for each field of the instruction
'''
def syntax(str):
    # instructFormat: Tuple that has the three MIPS instruction formats
    instructFormat = ('R','I','J')
    # ijInstruct: Dict that contains I/J format op codes 
    ijInstruct = {'j':2,'jal':3, 'beq':4,'bne':5,'addi':8,'addiu':9,'andi':12,
                  'ori':13,'slti':10,'sltiu':11,'lui':15,'lw':35,'sw':43}
    # First, remove any commas and split the string into a list to make checking syntax easier
    lst = str.replace(',', ' ').split()

    # Then, check if the instruction meets the correct word length
    # An instruction in MIPS will be either 2, 3, or 4 words long
    if len(lst) < 2 or len(lst) > 4:
        # If !(2 <= len(lst) <= 4), then return an error list to main
        badLst = [-1]
        return badLst, -1

    # Now, we will check which type of format the instruction is in
    op = lst[0] # Creating separate op variable, so we don't have to access the list each time in loop
    decLst = [0] # decLst: New list that contains the corresponding decimal numbers for each field
    # For loop to iterate through the ijInstruct dict
    for i in ijInstruct:
        # If op == current key in ijInstruct, we found the correct op code, so let's add it to decLst
        # If op code wasn't found, then we can assume instruction is R-Format which already stores 0 for op
        if(op == i):
            decLst.clear()
            decLst.append(ijInstruct[i])

    # If ops == 2 or 3, that means we have a J-Format instruction
    if decLst[0] == 2 or decLst[0] == 3 and len(lst) == 2:
        # J-Format Layout: OPP ADDRESS
        # Can just call immCheck function to set up J-Format without a separate jSyntax function needed
        immCheck(lst[1],decLst)

    # Else if ops != 0, that means we have an I-Format instruction, so call iSyntax 
    elif decLst[0] != 0:
        iSyntax(lst,decLst)
        # Once syntax was checked, set up the list to make life easier later in the
        # GUI in order to output the instruction correctly
        op = lst[0] 
        # First output format will be for LUI
        if op == 'lui':
            lst.append(0)
            RT = lst[1]
            imm = lst[2]
            lst[1] = 0
            lst[2] = RT
            lst[3] = imm 
        # Second output format will be for BEQ/BNE  
        elif op == 'beq' or op == 'bne':
            RS = lst[1]
            RT = lst[2]
        # Final output format will be for all other I-Format instructions
        else: 
            RT = lst[1]
            RS = lst[2]
            if op == 'lw' or op == 'sw':
                leftPos = RS.find('(') + 1
                rightPos = RS.find(')')
                RS = RS[leftPos:rightPos]
            lst[2] = RT
            lst[1] = RS

    # If op = 0, then call rSyntax to check R-Format instruction syntax
    else:
        rSyntax(lst,decLst)
        # After syntax was checked, rearrange list to make life easier 
        # when we are outputting from the GUI app 
        for i in range(6-len(lst)):
            lst.append(0)
        funct = lst[0]
        RD = lst[1]
        RS = lst[2]
        RT = lst[3]
        lst[0] = 0
        lst[5] = funct
        # First output format for SLL/SRL 
        if funct == 'srl' or funct == 'sll':
            lst[1] = 0
            lst[2] = RS
            lst[3] = RD 
            lst[4] = RT
        # Second output format for JR
        if funct == 'jr':
            lst[1] = RD
        # Final generic output format for all other R-Format instructions 
        else:
            lst[1] = RS 
            lst[2] = RT 
            lst[3] = RD 
            lst[4] = 0

    # Last loop to check if any errors were found
    for i in decLst:
        # If, at any point, we have a -1, then an error occur
        if i == -1:
            # We will clear the list and create a one element list with -1
            decLst.clear()
            decLst.append(-1)
            break 

    return decLst,lst

'''
Description: Checks to see if a valid register was passed or not
Parameters: String that contains the register we're checking for
Return Type: Int; Returns the corresponding value from our register table or -1 if 
a register wasn't written correctly
'''
def registerSyntax(reg):
    # registers: Dict that contains the corresponding number each MIPS register is assigned to
    registers = {'$t0':8,'$t1':9,'$t2':10,'$t3':11,'$t4':12,'$t5':13,'$t6':14,'$t7':15,
                 '$s0':16,'$s1':17,'$s2':18,'$s3':19,'$s4':20,'$s5':21,'$s6':22,'$s7':23,'$t8':24, "$t9":25}
    for i in registers:
        # If we find a key that corresponds to our register, we will return the corresponding number the key is assigned to
        if(reg == i):
            return registers[i]
    # If we don't find the right register, then we return -1 to indicate an error was found
    return -1 

'''
Description: Checks for a valid R-Format instruction and converts 
each field in the instruction to its corresponding decimal value
Parameters: List containing the original instruction and the list for its decimal equivalent
Return Type: Decimal list which should have 6 elements that corresponds to each field of the instruction
'''
def rSyntax(wordLst, decLst):
    # R-Format Layout: OP, RS, RT, RD, SHAMT, FUNCT
    # rInstruct: Dict that contains the funct codes for R-Format instructions
    rInstruct = {'add':32, 'addu':33, 'sub':34,'subu':35,'and':36,'or':37,
                  'nor':39,'slt':42,'sltu':43, 'sll':0, 'srl':2,'jr':8} 
    # First Special Case: JR instruction (only has one register)
    if len(wordLst) == 2:
        decLst.append(registerSyntax(wordLst[1])) # Simply insert RS to list
        for i in range(3): 
            decLst.append(0) # Insert 0 for RT, RD, and SHAMT
    # Second Special Case: SLL and SRL instructions (only has two registers and shamt)
    elif wordLst[3][0] != '$':
        decLst.append(0)
        decLst.append(registerSyntax(wordLst[2])) # Insert RT first
        decLst.append(registerSyntax(wordLst[1])) # Insert RD next
        try:
            decLst.append(int(wordLst[3])) # Insert corresponding shamt
        except:
            decLst.append(-1)
    # General Case: Instruction with 3 registers
    else:
        decLst.append(registerSyntax(wordLst[2])) # Insert RS first
        decLst.append(registerSyntax(wordLst[3])) # Then insert RT 
        decLst.append(registerSyntax(wordLst[1])) # Insert RD last
        decLst.append(0) # Insert 0 to shamt

    op = wordLst[0]
     # Once all other fields are set up, check for valid funct code
    for i in rInstruct:
        # If right name was found in rInstruct dict, add the value to the list and return
        if op == i:
            decLst.append(rInstruct[i])
            return decLst
    # If there's no corresponding funct code, simply add -1 to funct
    decLst.append(-1)

'''
Description: Checks for a valid I-format instruction and converts 
each field in the instruction to its corresponding decimal value
Parameters: List containing the original instruction and the list for its decimal equivalent
Return Type: Decimal list which should have 6 elements that corresponds to each field of the instruction
'''
def iSyntax(wordLst, decLst):
    # I-Format Layout: OP RS RT IMM
    # First special case: Instructions with length of 3 (LUI, LW, SW)
    if len(wordLst) == 3:
        # LUI Case : Just add RT to decLst
        if decLst[0] == 15:
            decLst.append(registerSyntax(wordLst[1]))
            decLst.append(0)
            wordLst.append(wordLst[2])
        # LW and SW cases
        else:
            # First, check to make sure there are parentheses enclosing the source register
            try:
                immIndex = wordLst[2].find('(')
                sRegIndex = wordLst[2].find(')')
            # If not, then just -1 to the list 
            except:
                decLst.append(-1)
            else:
                # If there are parentheses, splice the string to separate the imm/sReg
                imm = wordLst[2][0:immIndex]
                sReg = wordLst[2][immIndex+1:sRegIndex]
                wordLst.append(imm)  # Insert imm separately to the wordLst to do an immCheck later
                decLst.append(registerSyntax(sReg)) # Insert RS into decLst
                decLst.append(registerSyntax(wordLst[1])) # Then, insert RT into decLst
    # Second special case: BEQ/BNE instructions
    elif decLst[0] == 4 or decLst[0] == 5:
        # List already has RS and RT in proper order
        for i in range(1,3):
            decLst.append(registerSyntax(wordLst[i])) # Insert RS, then RT   
    # General case: Instructions with RS, RT, and IMM
    else:
        # Go in oppposite direction to insert RS and RT properly to decList
        for i in range(2,0,-1):
            decLst.append(registerSyntax(wordLst[i])) # Insert RS first, then RT
    # After registers are set up, now check for a valid immediate
    immCheck(wordLst[3],decLst)

'''
Description: Checks if a user put in a valid immediate/converts into int
Parameters: String that represents the imm and the list containing the decimal fields
Return Type: List that contains the imm now
'''
def immCheck(numStr,decLst):
    # First, check to see if the number can be converted into an int
    try:
        num = int(numStr)
    except:
        # If not, just insert -1 into the list
        decLst.append(-1)
    else:
        # Now check if the instruction is a branch or J-Format instruction
        # If it is, then we need to divide the number by 4 to account for the offset
        if decLst[0] == 2 or decLst[0] == 3 or decLst[0] == 4 or decLst[0] == 5:
            num //= 4
        # If number was valid, then add to list
        decLst.append(num)

'''
Description: Main function for MIPS to hex conversion
Parameters: None
Return Type: Int 
'''
def forwardConvertStart(instruct):
    instructLst = []
    # Run a while loop until the user inputs a valid instruction
    # instructStr = input("Enter a MIPS Assembly Instruction: ")
    instructLst, ogLst = syntax(instruct)
    # Check to see if list found from syntax has only one element in it
    if len(instructLst) == 1:
        # If so, we encountered an error, so print out error message and try again
        return -1,-1,-1,-1
    # Now convert the decimal list into its hex equivalent
    bStr, hStr = convert(instructLst)
    return bStr, hStr, instructLst, ogLst
