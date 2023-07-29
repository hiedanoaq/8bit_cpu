import MEMORY
#import time

class CPU:
    register_ = {
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

    def __init__(self, file):
        self.memory = MEMORY.Memory(256)
        self.memory.load_from_file(file)
        self.ram = MEMORY.Memory(256)
        self.register = [0x00] * 11
        self.mov_register_("sc", 0xff)
        self.flag = False  # jmpするかしないかのフラグ

    def system_call(self):  # system call
        op = self.register[self.register_["ax"]]
        if op == 0x00:  # put
            val = self.register[self.register_["bx"]]
            print(f"{val:02X}")
        elif op == 0x01:  # write
            print(chr(self.register[self.register_["bx"]]), end="")
        elif op == 0xff:  # dump
            self.ram.save_to_file("dump_ram.bin")
            self.memory.save_to_file("dump.bin")
        else:
            pass

    def ref_register_(self, arg):  # register参照
        return self.register[self.register_[arg]]

    def ref_register(self, arg):  # register参照
        return self.register[arg]

    def mov_register_(self, arg, val):
        self.register[self.register_[arg]] = val

    def mov_register(self, arg, val):
        self.register[arg] = val

    def ref_ram(self, arg):  # memory参照
        return self.ram.read(arg)

    def mov_ram(self, arg, val):
        self.ram.write(val, arg)

    def run(self):
        #loop = 0
        #while loop < 128:
        #start = time.time()
        while True:
            difference = 0
            address = self.ref_register_("ac")
            op = self.memory.read(address)
            operand = [self.memory.read(address + 1), self.memory.read(address + 2)]

            #print(f"{address:02X}")

            if op == 0x00:  # hlt
                break
            elif op == 0x01:  # mov reg, num
                self.mov_register(operand[0], operand[1])
            elif op == 0x02:  # mov reg, reg
                self.mov_register(operand[0], self.ref_register(operand[1]))
            elif op == 0x03:  # mov reg, add
                self.mov_register(operand[0], self.ref_ram(operand[1]))
            elif op == 0x04:  # mov add, reg
                self.mov_ram(operand[0], self.ref_register(operand[1]))
            elif op == 0x05:  # mov add, add
                self.mov_ram(operand[0], self.ref_ram(operand[1]))
            elif op == 0x06:  # and reg, reg
                self.mov_register_("ax", self.ref_register(operand[0]) & self.ref_register(operand[1]))
            elif op == 0x07:  # or reg, reg
                self.mov_register_("ax", self.ref_register(operand[0]) | self.ref_register(operand[1]))
            elif op == 0x08:  # not reg, reg
                self.mov_register_("ax", self.ref_register(operand[0]) ^ self.ref_register(operand[1]))
            elif op == 0x09:  # push reg
                self.mov_ram(self.ref_register_("sc"), self.ref_register(operand[0]))
                self.mov_register_("sc", self.ref_register_("sc") - 1)
            elif op == 0x0a:  # pop reg
                self.mov_register(operand[0], self.ref_ram(self.ref_register_("sc")))
                self.mov_register_("sc", self.ref_register_("sc") + 1)
            elif op == 0x0b:  # cmp reg, reg
                operator = self.ref_register_("ax")
                if operator == 0:
                    self.flag = self.ref_register(operand[0]) == self.ref_register(operand[1])
                elif operator == 1:
                    self.flag = self.ref_register(operand[0]) != self.ref_register(operand[1])
                elif operator == 2:
                    self.flag = self.ref_register(operand[0]) < self.ref_register(operand[1])
                elif operator == 3:
                    self.flag = self.ref_register(operand[0]) > self.ref_register(operand[1])
                else:
                    pass
            elif op == 0x0c:  # jmp add
                if self.flag:
                    self.mov_register_("ac", operand[0] - 3)
                else:
                    pass
            elif op == 0x0d:  # true
                self.flag = True
            elif op == 0x0e:  # syscall
                self.system_call()
            elif op == 0x0f:  # add reg, reg
                self.mov_register_("ax", self.ref_register(operand[0]) + self.ref_register(operand[1]))
            elif op == 0x10:  # sub reg, reg
                self.mov_register_("ax", self.ref_register(operand[0]) - self.ref_register(operand[1]))
            elif op == 0x11:  # mul reg, reg
                self.mov_register_("ax", self.ref_register(operand[0]) * self.ref_register(operand[1]))
            elif op == 0x12:  # div reg, reg
                self.mov_register_("ax", self.ref_register(operand[0]) // self.ref_register(operand[1]))
            elif op == 0x13:  # mod reg, reg
                self.mov_register_("ax", self.ref_register(operand[0]) % self.ref_register(operand[1]))
            elif op == 0x14:  # exit
                break
            elif op == 0x15:  # mov add, num
                self.mov_ram(operand[0], operand[1])
            elif op == 0x16:  # mov reg, radd
                self.mov_register(operand[0], self.ref_ram(self.ref_register(operand[1])))
            elif op == 0x17:  # mov radd, reg
                self.mov_ram(self.ref_register(operand[0]), self.ref_register(operand[1]))
            elif op == 0x18:  # mov radd, radd
                self.mov_ram(self.ref_register(operand[0]), self.ref_ram(self.ref_register(operand[1])))
            elif op == 0x19:  # mov radd, add
                self.mov_ram(self.ref_register(operand[0]), self.ref_ram(operand[1]))
            elif op == 0x1a:  # mov add, radd
                self.mov_ram(operand[0], self.ref_ram(self.ref_register(operand[1])))
            elif op == 0xff:  # @memory
                difference_ = operand[1] - operand[0]
                for index in range(difference_):
                    self.mov_ram(operand[0] + index, self.memory.read(address+3+index))
                difference = difference_
            else:
                pass
            
            self.mov_register_("ac", self.ref_register_("ac") + 3 + difference)
            #loop += 1
        #print(loop)
        #print(time.time() - start)

