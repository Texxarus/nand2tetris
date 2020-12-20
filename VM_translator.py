file_input = open('C:\\nand2tetris\\nand2tetris\\projects\\07\\StackArithmetic\\SimpleAdd\\SimpleAdd.vm', 'r')
file_output= open('C:\\nand2tetris\\nand2tetris\\projects\\07\\StackArithmetic\\SimpleAdd\\SimpleAdd.asm', 'w')

C_Arithmetic = {"add":"+", "sub":"-", "and":"&", "or":"|"}
C_Logical = ["eq", "gt", "lt", "not", "neg"]
C_MemAcc = ["pop", "push"]
cmd, mem, num = ["", "", ""]

for line in file_input:
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

    if cmd in C_MemAcc:
        if mem == "constant":
            file_output.write(" @" + num + "\n D=A \n @SP \n A=M \n M=D \n @SP \n M=M+1 \n")

        else:
            print("not local")
    else:
        if cmd in C_Arithmetic:
            file_output.write(" @SP \n A=M-1 \n D=M \n A=A-1 \n M=D" + C_Arithmetic[cmd] + "M \n @SP \n M=M-1 \n")
        else
    



    