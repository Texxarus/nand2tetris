import os
import sys

#file_input = open(os.path.dirname(os.path.abspath(__file__)) + '\\StackArithmetic\\' + input_name + '\\' + input_name + '.vm', 'r')
#file_output= open(os.path.dirname(os.path.abspath(__file__)) + '\\StackArithmetic\\' + input_name + '\\' + input_name + '.asm', 'w')
file_input = open(sys.argv[1], 'r')
file_output = open (sys.argv[1].split(".")[0] + '.asm', 'w')
C_Arithmetic = {"add":"+", "sub":"-", "and":"&", "or":"|"}
C_Logical = {"eq":"JEQ", "gt":"JGT", "lt":"JLT"}
C_MemAcc = ["pop", "push"]
cmd, mem, num = ["", "", ""]
input_name = os.path.basename(sys.argv[1])

Seg_sym = {"local":"LCL", "argument":"ARG", "this":"THIS", "that":"THAT"}
count = 0
for line in file_input:
    cmd, mem, num = ["", "", ""]
    if "//" in line:
        line = line[:line.index('/')]

    code_line = line.strip()
    if code_line == "":
        #print("something")
        continue
    #print(code_line)    

    list_arg = code_line.split()
    if len(list_arg) == 3:
        cmd, mem, num = list_arg
    else:   
        cmd = list_arg[0]
    #print(cmd, mem, num, "\n")
    #return cmd, mem, num

    file_output.write(" // " + code_line + "\n")

    if cmd in C_MemAcc:
        if mem == "constant":
            file_output.write(" @" + num + "\n D=A \n @SP \n A=M \n M=D \n @SP \n M=M+1 \n")
        elif cmd == "pop":
            if mem in Seg_sym:
                #first solution
                #file_output.write(" @" + num + "\n D=A \n @" + Seg_sym[mem] + "\n D=D+M \n @R13 \n M=D \n"
                #                + " @SP \n A=M-1 \n D=M \n @R13 \n A=M \n M=D \n @SP \n M=M-1 \n")

                #second solution
                file_output.write(" @" + num + "\n D=A \n @" + Seg_sym[mem] + "\n D=D+M \n"
                                + " @SP \n A=M-1 \n D=D+M \n A=D-M \n M=D-A \n @SP \n M=M-1 \n")
            elif mem == "static":
                file_output.write(" @SP \n A=M-1 \n D=M \n @" + input_name.split('.')[0] + "." + num + "\n M=D \n @SP \n M=M-1 \n" )
            elif mem == "temp":
                file_output.write(" @SP \n A=M-1 \n D=M \n @" + str(5+int(num)) + "\n M=D \n @SP \n M=M-1 \n" )
            elif mem == "pointer":
                if num == "0":
                    file_output.write(" @SP \n A=M-1 \n D=M \n @THIS \n M=D \n @SP \n M=M-1 \n")
                if num == "1":
                    file_output.write(" @SP \n A=M-1 \n D=M \n @THAT \n M=D \n @SP \n M=M-1 \n")

        elif cmd == "push":
            if mem in Seg_sym:
                file_output.write(" @" + num + "\n D=A \n @" + Seg_sym[mem] + "\n A=D+M \n D=M \n"
                                + " @SP \n A=M \n M=D \n @SP \n M=M+1 \n")
            elif mem == "static":
                file_output.write(" @" + input_name.split('.')[0] + "." + num + "\n D=M \n"
                                + " @SP \n A=M \n M=D \n @SP \n M=M+1 \n" )
            elif mem == "temp":
                file_output.write(" @" + str(5+int(num)) + "\n D=M \n"
                                + " @SP \n A=M \n M=D \n @SP \n M=M+1 \n" )
            elif mem == "pointer":
                if num == "0":
                    file_output.write(" @THIS \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1 \n")
                if num == "1":
                    file_output.write(" @THAT \n D=M \n @SP \n A=M \n M=D \n @SP \n M=M+1 \n")

    else:
        if cmd in C_Arithmetic:
            file_output.write(" @SP \n A=M-1 \n D=M \n A=A-1 \n M=M" + C_Arithmetic[cmd] + "D \n @SP \n M=M-1 \n")
        elif cmd == "neg":
            file_output.write(" @SP \n A=M-1 \n M=-M \n")
        elif cmd == "not":
            #file_output.write(" @SP \n A=M-1 \n A=A-1 \n D=!M \n @SP \n A=M \n M=D \n @SP \n M=M+1 \n")
            file_output.write(" @SP \n A=M-1 \n M=!M \n")
        elif cmd in C_Logical:
            #First subtract the 2 top elements in the stack, store the result in the stack and D register
            file_output.write(" @SP \n A=M-1 \n D=M \n A=A-1 \n MD=M-D \n @SP \n M=M-1 \n")
            file_output.write(" @TRUE" + str(count) + "\n D;" + C_Logical[cmd] +  "\n")
            file_output.write(" @SP \n A=M-1 \n M=0 \n @NEXT" + str(count) + "\n 0;JMP \n") 
            file_output.write("(TRUE" + str(count) + ") \n @SP \n A=M-1 \n M=-1 \n") 
            file_output.write("(NEXT" + str(count) + ") \n") 
            count = count + 1
    
