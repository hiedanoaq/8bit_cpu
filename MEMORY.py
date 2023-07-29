class Memory:
    def __init__(self, size, set_val=0):
        self.size = size
        self.memory = [set_val] * size

    def read(self, address):
        return self.memory[address]

    def write(self, val, address):
        self.memory[address] = val % 256

    def reads(self, address, num_bytes):
        return self.memory[address:address + num_bytes]

    def writes(self, vals, address):
        for i, val in enumerate(vals):
            self.memory[address + i] = val % 256

    def dump(self):
        for i in range(0, self.size, 16):
            print(f'{i:04X}:', end=' ')
            for j in range(16):
                if i + j < self.size:
                    print(f'{self.memory[i + j]:02X}', end=' ')
                else:
                    print('  ', end=' ')
                if j == 7:
                    print('', end=' ')
            print()

    def mov(self, src_address, dest_address, num_bytes):
        data = self.reads(src_address, num_bytes)
        self.writes(data, dest_address)

    def mov_between_memories(self, src_memory, src_address, dest_address, num_bytes):
        data = src_memory.reads(src_address, num_bytes)
        self.writes(data, dest_address)
    
    def save_to_file(self, filename):
        try:
            with open(filename, "wb") as file:
                # 16進数のデータをbytes型に変換してファイルに書き込む
                file.write(bytes(self.memory))
            #print(f"メモリデータをファイル '{filename}' に保存しました。")
        except IOError:
            #print(f"ファイル '{filename}' の保存に失敗しました。")
            pass
    
    def load_from_file(self, filename):
        try:
            with open(filename, "rb") as file:
                data = file.read()
                # 読み込んだバイナリデータを16進数のリストに変換してメモリに設定
                self.memory = [byte for byte in data]
            #print(f"ファイル '{filename}' からメモリデータを読み込みました。")
        except IOError:
            #print(f"ファイル '{filename}' の読み込みに失敗しました。")
            pass