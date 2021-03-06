
# Authors: Trung Le, Weijing Rao

# This Python program simulates a restricted subset of MIPS instructions
# and output 
# Settings: Multi-Cycle CPU, i.e lw takes 5 cycles, beq takes 3 cycles, others are 4 cycles

mem_space = 4096 # Memory addr starts from 2000 , ends at 3000.  Hence total space of 4096


def simulate(Instruction,InstructionHex,debugMode):
    print("***Starting simulation***")
    print("Settings:")
    Register = [0,0,0,0,0,0,0,0]    # initialize all values in registers to 0
    Memory = [0 for i in range(mem_space)] 
    PC = 0
    DIC = 0
    Cycle = 0
    threeCycles = 0 # frequency of how many instruction takes 3 cycles
    fourCycles = 0  #                                         4 cycles
    fiveCycles = 0  #                                         5 cycles
    pipelineCycles = 4 #number of pipelined cycles

    finished = False
    while(not(finished)):
    
        DIC += 1
        pipelineCycles += 1
        fetch = Instruction[PC]
        if (fetch[0:32] == '00010000000000001111111111111111'):
            print("Dead loop end program")
            Cycle += 3
            finished = True

        elif (fetch[0:6] == '000000' and fetch[26:32] == '100000'): # ADD
            if(debugMode):
                print("Cycles " + str(Cycle) + ":")
                print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "add $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
                print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] + Register[int(fetch[11:16],2)]

        elif(fetch[0:6] == '000000' and fetch[26:32] == '100010'): # SUB
            if(debugMode):
                print("Cycles " + str(Cycle) + ":")
                print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "sub $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
                print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] - Register[int(fetch[11:16],2)]

        elif(fetch[0:6] == '001000'):                               # ADDI
            imm = int(fetch[16:32],2) if fetch[16]=='0' else -(65535 -int(fetch[16:32],2)+1)
            if(debugMode):
                print("Cycles " + str(Cycle) + ":")
                print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "addi $" + str(int(fetch[11:16],2)) + ",$" +str(int(fetch[6:11],2)) + " " + str(imm) )
                print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Register[int(fetch[11:16],2)] = Register[int(fetch[6:11],2)] + imm

        elif(fetch[0:6] == '000100'):                               # BEQ
            imm = int(fetch[16:32],2) if fetch[16]=='0' else -(65535 -int(fetch[16:32],2)+1)
            if(debugMode):
                print("Cycles " + str(Cycle) + ":")
                print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "beq $" + str(int(fetch[6:11],2)) + ",$" +str(int(fetch[11:16],2)) + "," + str(imm) )
                print("Taking 3 cycles \n")
            Cycle += 3
            PC += 1
            threeCycles += 1
            PC = PC + imm if (Register[int(fetch[6:11],2)] == Register[int(fetch[11:16],2)]) else PC
            if (Register[int(fetch[6:11],2)] == Register[int(fetch[11:16],2)]):
                print("Branch Hazard detected. Added 1 null op")
                print("Flushed next Instruction: " + InstructionHex[PC + 1])
                pipelineCycles += 1
            tmpFetch = Instruction[PC-1]
            if((Register[int(fetch[6:11],2)] == Register[int(tmpFetch[6:11], 2)] or Register[int(fetch[11:16],2)] == Register[int(tmpFetch[6:11], 2)])):
                print("Computation Branch Compare Hazard Dected Stall 1")
                pipelineCycles +=1

        elif(fetch[0:6] == '000101'): # BNE
            imm = int(fetch[16:32],2) if fetch[16]=='0' else -(65535 -int(fetch[16:32],2)+1)
            if(debugMode):
                print("Cycles " + str(Cycle) + ":")
                print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "bne $" + str(int(fetch[6:11],2)) + ",$" +str(int(fetch[11:16],2)) + "," + str(imm) )
                print("Taking 3 cycles \n")
            PC += 1
            Cycle += 3
            threeCycles += 1
            PC = PC + imm if Register[int(fetch[6:11],2)] != Register[int(fetch[11:16],2)] else PC

        elif(fetch[0:6] == '000000' and fetch[26:32] == '101010'): # SLT
            if(debugMode):
                print("Cycles " + str(Cycle) + ":")
                print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "slt $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
                print("Taking 4 cycles \n")
            Cycle += 4
            PC += 1
            fourCycles += 1
            Register[int(fetch[16:21],2)] = 1 if Register[int(fetch[6:11],2)] < Register[int(fetch[11:16],2)] else 0

        elif(fetch[0:6] == '101011'):                               # SW
            #Sanity check for word-addressing 
            if ( int(fetch[30:32])%4 != 0 ):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", hex(int(fetch,2)))
                exit()
            imm = int(fetch[16:32],2)
            if(debugMode):
                print("Cycles " + str(Cycle) + ":")
                print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "sw $" + str(int(fetch[6:11],2)) + "," +str(imm + Register[int(fetch[6:11],2)] - 8192) + "(0x2000)" )
                print("Taking 4 cycles \n")
            PC += 1
            Cycle += 4
            fourCycles += 1
            Memory[imm + Register[int(fetch[6:11],2)] - 8192]= Register[int(fetch[11:16],2)] # Store word into memory

        elif(fetch[0:6] == '100011'):                               # LW
            #Sanity check for word-addressing 
            if ( int(fetch[30:32])%4 != 0 ):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", hex(int(fetch,2)))
                exit()
            imm = int(fetch[16:32],2)
            if(debugMode):
                print("Cycles " + str(Cycle) + ":")
                print("PC =" + str(PC*4) + " Instruction: 0x" +  InstructionHex[PC] + " :" + "lw $" + str(int(fetch[6:11],2)) + "," +str(imm + Register[int(fetch[6:11],2)] - 8192) + "(0x2000)" )
                print("Taking 5 cycles \n")
            PC += 1
            Cycle += 5
            fiveCycles += 1
            Register[int(fetch[11:16],2)] = Memory[imm + Register[int(fetch[6:11],2)] - 8192] # Load memory into register
            #LW USE Hazard. If the next instruction uses lw -> stall by once cycle
            tmpFetch = Instruction[PC]
            if((tmpFetch[0:6] == '000000' and tmpFetch[26:32] == '100000') or   #If next instruction is R type
                (tmpFetch[0:6] == '000000' and tmpFetch[26:32] == '100010') or        #sub
                (tmpFetch[0:6] == '000000' and tmpFetch[26:32] == '101010')):         #SLT

                if(int(fetch[11:16],2)== int(tmpFetch[6:11]) or int(fetch[11:16],2)== int(tmpFetch[11:16])):
                    print("LW Use Hazard Dected Stall 1")
                    pipelineCycles +=1

                
 
    print("***Finished simulation***")
    print("Total # of cycles: " + str(Cycle))
    print("Total # of pipeline cycles: " + str(pipelineCycles))
    print("Dynamic instructions count: " +str(DIC) + ". Break down:")
    print("                    " + str(threeCycles) + " instructions take 3 cycles" )
    print("                    " + str(fourCycles) + " instructions take 4 cycles" )
    print("                    " + str(fiveCycles) + " instructions take 5 cycles" )
    print("Registers: " + str(Register))
     
   


def main():
    print("Welcome to ECE366 sample MIPS_sim, choose the mode of running i_mem.txt: ")
    debugMode =True if  int(input("1 = debug mode         2 = normal execution\n"))== 1 else False

    I_file = open("I_file.txt","r")
    Instruction = []            # array containing all instructions to execute         
    InstructionHex = []
    for line in I_file:
        if (line == "\n" or line[0] =='#'):              # empty lines,comments ignored
            continue
        line = line.replace('\n','')
        InstructionHex.append(line)
        line = format(int(line,16),"032b")
        Instruction.append(line)
        
    
    simulate(Instruction,InstructionHex,debugMode)



if __name__ == "__main__":
    main()
