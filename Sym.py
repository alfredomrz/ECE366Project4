def simulate(Instruction,Memory):
    print("ECE366 Fall 2018 ISA Design: Simulator")
    print()
    PC = 0              # Program-counter
    DIC = 0
    Reg = [0,0,0,0,0,0,0,0]     # 4 registers, init to all 0
    print("******** Simulation starts *********")
    finished = False

    while(not(finished)):
        fetch = Instruction[PC]
        DIC += 1
        if (fetch[0:7] == '001000'):    #addi
            print("*ADDN*")
            #Reg[3] = Reg[3] - 1
            PC += 1
        elif(fetch[0:32] == '00010000000000001111111111111111'):
            finished = True

    print("******** Simulation finished *********")


def main():
    I_file = open("I_file.txt","r")
    #data_file = open("d_mem.txt","r")
    Memory = []
    Nlines = 0          # How many instrs total in input.txt  
    Instruction = []    # all instructions will be stored here
    InstructionHex = []

    for line in I_file:
        if (line == "\n" or line[0] =='#'):              # empty lines,comments ignored
            continue
        line = line.replace('\n','')
        InstructionHex.append(line)
        line = format(int(line,16),"032b")
        Instruction.append(line)

    print(Instruction[0])
    print(Instruction[1])
    """
    for line in data_file:  # Read in data memory
        if (line == "\n" or line[0] =='#'):              # empty lines,comments ignored
            continue
        Memory.append(int(line,2))
    """
        
    simulate(Instruction, Memory)

    
    I_file.close()
    #data_file.close()
    
if __name__ == "__main__":
    main()
