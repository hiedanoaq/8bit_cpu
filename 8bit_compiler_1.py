import MEMORY

class Compiler:
    register = {
        "R0": 0x00,
        "R1": 0x01,
        "R2": 0x02,
        "R3": 0x03,
        "R4": 0x04,
        "R5": 0x05,
        "R6": 0x06,
        "R7": 0x07,
        "R8": 0x08,
        "R9": 0x09,
        "R10": 0x0a,
        "ax": 0x00,
        "bx": 0x01,
        "cx": 0x02,
        "dx": 0x03,
        "ex": 0x04,
        "fx": 0x05,
        "ac": 0x06,
        "bp": 0x07,
        "ic": 0x08,
        "pc": 0x09,
        "sc": 0x0a
    }
    num_ = list("0123456789")

    def __init__(self, file):
        self.file = file
        self.asm_code = []
        self.memory = MEMORY.Memory(256, 0x00)
        self.label = {}
        self.call = {}
        self.code = []
        self.code_length = 0
        self.address_count = 0

    def reg(self, arg):
        return self.register[arg]

    def num(self, arg):
        return int(arg, 0)

    def add(self, arg):
        return int(arg[1:-1], 0)

    def radd(self, arg):
        return self.register[arg[1:-1]]

    def is_num(self, arg):
        return arg[0] in self.num_

    def is_reg(self, arg):
        return arg in self.register

    def is_add(self, arg):
        return (arg[:1] + arg[-1:]) == "[]" and (arg[1] in self.num_)

    def is_radd(self, arg):
        return (arg[:1] + arg[-1:]) == "[]" and (arg[1:-1] in self.register)

    def compile(self):
        with open(self.file, "r", encoding='utf-8') as f:
            self.asm_code = f.read().split("\n")

        for line, line_code in enumerate(self.asm_code):
            #print(self.memory.reads(self.address_count-3, 3))
            #print("L" + str(line) + ":" + line_code)
            difference = 0
            line_code = line_code.replace(",", "").split(" ")

            if line_code[0][-1:] == ":":
                self.label[line_code[0][:-1]] = self.address_count
                difference = -3
            elif line_code[0] == "hlt":
                self.memory.writes([0x00, 0x00, 0x00], self.address_count)
            elif line_code[0] == "mov":
                if self.is_reg(line_code[1]):
                    if self.is_num(line_code[2]):
                        self.memory.writes([0x01, self.reg(line_code[1]), self.num(line_code[2])], self.address_count)
                    elif self.is_reg(line_code[2]):
                        self.memory.writes([0x02, self.reg(line_code[1]), self.reg(line_code[2])], self.address_count)
                    elif self.is_add(line_code[2]):
                        self.memory.writes([0x03, self.reg(line_code[1]), self.add(line_code[2])], self.address_count)
                    elif self.is_radd(line_code[2]):
                        self.memory.writes([0x16, self.reg(line_code[1]), self.radd(line_code[2])], self.address_count)
                    else:
                        print("ERR:" + self.file + ":L" + str(line + 1) + " : " + self.asm_code[line])
                        difference = -3
                elif self.is_add(line_code[1]):
                    if self.is_reg(line_code[2]):
                        self.memory.writes([0x04, self.add(line_code[1]), self.reg(line_code[2])], self.address_count)
                    elif self.is_add(line_code[2]):
                        self.memory.writes([0x05, self.add(line_code[1]), self.add(line_code[2])], self.address_count)
                    elif self.is_num(line_code[2]):
                        self.memory.writes([0x15, self.add(line_code[1]), self.num(line_code[2])], self.address_count)
                    elif self.is_radd(line_code[2]):
                        self.memory.writes([0x1a, self.add(line_code[1]), self.radd(line_code[2])], self.address_count)
                    else:
                        print("ERR:" + self.file + ":L" + str(line + 1) + " : " + self.asm_code[line])
                        difference = -3
                elif self.is_radd(line_code[1]):
                    if self.is_reg(line_code[2]):
                        self.memory.writes([0x17, self.radd(line_code[1]), self.reg(line_code[2])], self.address_count)
                    elif self.is_radd(line_code[2]):
                        self.memory.writes([0x18, self.radd(line_code[1]), self.radd(line_code[2])], self.address_count)
                    elif self.is_add(line_code[2]):
                        self.memory.writes([0x19, self.radd(line_code[1]), self.add(line_code[2])], self.address_count)
                    else:
                        print("ERR:" + self.file + ":L" + str(line + 1) + " : " + self.asm_code[line])
                        difference = -3
                else:
                    print("ERR:" + self.file + ":L" + str(line + 1) + " : " + self.asm_code[line])
                    difference = -3
            elif line_code[0] == "and":
                self.memory.writes([0x06, self.reg(line_code[1]), self.reg(line_code[2])], self.address_count)
            elif line_code[0] == "or":
                self.memory.writes([0x07, self.reg(line_code[1]), self.reg(line_code[2])], self.address_count)
            elif line_code[0] == "not":
                self.memory.writes([0x08, self.reg(line_code[1]), self.reg(line_code[2])], self.address_count)
            elif line_code[0] == "push":
                self.memory.writes([0x09, self.reg(line_code[1]), 0x00], self.address_count)
            elif line_code[0] == "pop":
                self.memory.writes([0x0a, self.reg(line_code[1]), 0x00], self.address_count)
            elif line_code[0] == "cmp":
                self.memory.writes([0x0b, self.reg(line_code[1]), self.reg(line_code[2])], self.address_count)
            elif line_code[0] == "jmp":
                self.memory.writes([0x0c, 0x00, 0x00], self.address_count)
                self.call[self.address_count + 1] = line_code[1]
            elif line_code[0] == "true":
                self.memory.writes([0x0d, 0x00, 0x00], self.address_count)
            elif line_code[0] == "syscall":
                self.memory.writes([0x0e, 0x00, 0x00], self.address_count)
            elif line_code[0] == "add":
                self.memory.writes([0x0f, self.reg(line_code[1]), self.reg(line_code[2])], self.address_count)
            elif line_code[0] == "sub":
                self.memory.writes([0x10, self.reg(line_code[1]), self.reg(line_code[2])], self.address_count)
            elif line_code[0] == "mul":
                self.memory.writes([0x11, self.reg(line_code[1]), self.reg(line_code[2])], self.address_count)
            elif line_code[0] == "div":
                self.memory.writes([0x12, self.reg(line_code[1]), self.reg(line_code[2])], self.address_count)
            elif line_code[0] == "mod":
                self.memory.writes([0x13, self.reg(line_code[1]), self.reg(line_code[2])], self.address_count)
            elif line_code[0] == "exit":
                self.memory.writes([0x14, 0x00, 0x00], self.address_count)
            elif line_code[0] == "@memory":
                data_range = line_code[1][1:-1].split("-")
                data_length = int(data_range[1], 0) - int(data_range[0], 0)
                self.memory.writes([0xff, self.num(data_range[0]), self.num(data_range[1])], self.address_count)
                for i in range(data_length):
                    self.memory.write(int(line_code[2 + i], 16), self.address_count + 3 + i)
                difference = data_length
            else:
                print("ERR:" + self.file + ":L" + str(line + 1) + " : " + self.asm_code[line])
                difference = -3

            self.address_count += 3 + difference

        for key in self.call.keys():
            self.memory.write(self.label[self.call[key]], key)

        self.memory.save_to_file(self.file + ".exe")
        
        #print(self.label)
