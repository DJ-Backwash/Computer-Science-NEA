# Notes for me so i don't forget

# On program exit any memory locations will be saved and overwritten in a file called "memory.txt"
# and are able to be loaded from in a new program
#
# The syntax for the assembly is the same as the one used by AQA however commas are not
# neccesary, they will be ignored by the program. 
# 2 new instructions were added to assist with debugging and use of programs:
#
#   OUT:
#       this will add whatever you give it to the output log, if multiple things are 
#       added they will placed in a list.
#
#   PRT:
#       this will immediately output whatever is fed into it when the line is read and 
#       was implemented to assist with debugging.

# code
registers = None

def refresh_reg():
    global registers
    # When the program closes reset Registers and Memory
    registers = {}
    reg_names = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12"]
    for reg in reg_names:
        registers[reg] = 0
    with open("registers.txt", "w") as f:
        f.write(str(registers))
    

def run_code(FrontEnd, filename = "mycode.txt", mode = 0): # name of the file containing your assembly code, if no 
#                                 name is passed then it will be automatically loaded 
#                                 from "mycode.txt" to use your own file name edit the 
#                                 "print(run())" at the end of this file.

    #grab file and place each line in its own spot in a list
    global contents, print_log, read_head, cmp, registers, memory, labels, looping
    contents = []
    try:
        with open(filename, 'r') as f:
            for i in f:
                contents.append(i.strip("\n").replace(",", ""))
    
    except: # if there is no file detected it will create one
        with open("mycode.txt", 'w') as f:
            f.write("\nHALT")
            print("Please write your code in 'mycode.txt'")

    #variable initialisation
    print_log = None
    read_head = 0
    cmp = []

    #create "registers"
    refresh_reg()

    #initialise memory, feel free to add values to memory.txt
    try:
        with open("memory.txt", 'r') as f:
            memory = eval(f.read())
    except:
        memory = {}

    #build label dictionary
    labels = {}
    for i in range(len(contents)):
        if contents[i][-1] == ":":
            labels[contents[i][:-1]] = i

    #main sequence
    if mode == 0:
        looping = None
        while looping != "HALT":
            looping = execute(FrontEnd)
        FrontEnd.console_out(f"HALT reached", "Success")

def execute(FrontEnd):
    global line, contents, print_log, read_head, cmp, registers, memory, labels, looping

    del_cmp = True # this line is explained lower
    
    #current line
    line = contents[read_head]

    #split line into list of parts
    parts = line.split(" ")

    match parts[0]:
        case "OUT": # Rn
            n1 = int(registers[parts[1]])
            #print_log.append(n1)
            print_log = n1

        case "MOV": # Rd <operand2>
            if parts[2][0] == "#": # instant addressing
                n1 = int(parts[2][1:])

            else: # direct addressing
                n1 = registers[parts[2]]

            registers[parts[1]] = int(n1)
        
        case "ADD": # Rd Rn <operand2>
            n1 = registers[parts[2]]

            if parts[3][0] == "#": # instant addressing
                n2 = int(parts[3][1:])

            else: # direct addressing
                n2 = registers[parts[3]]
            
            registers[parts[1]] = n1 + n2

        case "SUB": # Rd Rn <operand2>
            n1 = registers[parts[2]]

            if parts[3][0] == "#": # instant addressing
                n2 = int(parts[3][1:])

            else: # direct addressing
                n2 = registers[parts[3]]
            
            registers[parts[1]] = n1 - n2

        case "LSL": # Rd Rn <operand2>
            n1 = registers[parts[2]]

            if parts[3][0] == "#": # instant addressing
                n2 = int(parts[3][1:])

            else: # direct addressing
                n2 = registers[parts[3]]
            
            registers[parts[1]] = n1 << n2

        case "LSR": # Rd Rn <operand2>
            n1 = registers[parts[2]]

            if parts[3][0] == "#": # instant addressing
                n2 = int(parts[3][1:])

            else: # direct addressing
                n2 = registers[parts[3]]
            
            registers[parts[1]] = n1 >> n2

        case "AND": # Rd Rn <operand2>
            n1 = bin(registers[parts[2]])[-1]

            if parts[3][0] == "#": # instant addressing
                n2 = int(parts[3][-1])

            else: # direct addressing
                n2 = bin(registers[parts[3]])[-1]
            
            registers[parts[1]] = n1 and n2

        case "ORR": # Rd Rn <operand2>
            n1 = bin(registers[parts[2]])[-1]

            if parts[3][0] == "#": # instant addressing
                n2 = int(parts[3][-1])

            else: # direct addressing
                n2 = bin(registers[parts[3]])[-1]
            
            registers[parts[1]] = n1 or n2

        case "EOR": # Rd Rn <operand2>
            n1 = bin(registers[parts[2]])[-1]

            if parts[3][0] == "#": # instant addressing
                n2 = int(parts[3][-1])

            else: # direct addressing
                n2 = bin(registers[parts[3]])[-1]
            
            registers[parts[1]] = n1 != n2

        case "MVN": # Rd <operand2>
            if parts[2][0] == "#": # instant addressing
                n1 = int(parts[2][-1])

            else: # direct addressing
                n1 = bin(registers[parts[2]])[-1]
            
            registers[parts[1]] = not n1

        case "PRT": # <operand>; intended for bugfixing, final outputs should use "OUT"
            if parts[1][0] == "#": # instant addressing
                print(int(parts[1][1:]))

            else: # direct addressing
                print(registers[parts[1]])

        #branches
        case "B": # <label>
            read_head = labels[parts[1]]

        case "CMP": # Rn <operand2>
            del_cmp = False
            cmp.append(registers[parts[1]])

            if parts[2][0] == "#": # instant addressing
                cmp.append(int(parts[2][1:]))

            else: # direct addressing
                cmp.append(registers[parts[2]])

        case "BEQ": # <label>
            del_cmp = False
            if cmp[0] == cmp[1]:
                read_head = labels[parts[1]]

        case "BNE": # <label>
            del_cmp = False
            if cmp[0] != cmp[1]:
                read_head = labels[parts[1]]

        case "BLT": # <label>
            del_cmp = False
            if cmp[0] < cmp[1]:
                read_head = labels[parts[1]]

        case "BGT": # <label>
            del_cmp = False
            if cmp[0] < cmp[1]:
                read_head = labels[parts[1]]

        case "STR": # Rd <memory ref>
            memory[parts[2]] = registers[parts[1]]

        case "LDR": # Rd <memory ref>
            registers[parts[1]] = memory[parts[2]]
            
        case "HALT": # Stop!!!
            return "HALT"

        case _: #its a label, don't do anything
            pass

    if del_cmp == True: # effectively, this stores the comparison variables until a line that does not contain a branch is reached
        cmp = []
    
    read_head += 1
    
    # Update register file
    with open("registers.txt", "w") as f:
        f.write(str(registers))


    with open("memory.txt", 'w') as f:
        f.write(str(memory))
    FrontEnd.draw_registers()

    if print_log != None:
        FrontEnd.console_out(print_log, "Out")
        print_log = None
    return read_head
