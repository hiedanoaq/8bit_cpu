The English version is below the Japanese version.

# 8bit_cpu
### 概要
8bitのcpuシミュレーターです。  
規格は自作ですので互換性はありません。  

### ファイル
* **実行ファイル**
 * MEMORY.py        メモリ用のプログラム
 * compiler.py      コンパイル用のプログラム
 * cpu.py           実行用のプログラム
* **規格ファイル**
 * mnemonic.txt     ニーモニック(命令)の規格
 * register.txt     レジスタの種類
 * cmp_operator.txt cmp(比較命令)の種類
 * system_call.txt  システムコールの種類
* **テストコード**
 * prime.asm        0~254までの素数を出力する。(2が出力されないと思うけど許して。アセンブリ書き換えるの面倒だったんです。)
 * hello.asm        Hello, World!\nと出力する
 * fib.asm          0~254までのフィボナッチ数列を出力する。

### 説明(のようなもの)
演算結果は、axレジスタに返されます。  
比較命令の比較演算子の指定は、axレジスタで行います。  
システムコールの番号の指定も、axレジスタで行います。  

ちなみに、8bitなので本来レジスタはa, b, c, dというふうに一文字なのですが、間違ってax, bx, cx, dxというふうになっています。  
あと、ac, bc, ic, pc, scレジスタが有りますが、ノリで追加したので使われないレジスタ，よくわからんレジスタがあります。  
ax, bx, cx, dx, ex 汎用レジスタ(axは、演算結果の戻り値が入る)  
ac アドレスカウンタ(現在読み込んでいるプログラムの位置)  
bc ベースカウンタ(なんのために追加したか覚えていない。多分関数の呼び出し元のアドレス)  
ic わからん  
pc わからん  
sc スタックカウンタ(現在のスタックの位置)  

説明は今のところこんなもんですかね？必要があれば追記します。  
以上です。  

### Overview
This is an 8bit cpu simulator.  
The standard is not compatible since it is self-made.  

### File
* **Executable file**
 * MEMORY.py Program for memory
 * compiler.py Program for compiling
 * cpu.py Program for execution
* **Standard files**
 * mnemonic.txt mnemonic (instruction) standard
 * register.txt Types of registers
 * cmp_operator.txt Type of cmp (compare instruction)
 * system_call.txt Type of system call
* **test code**
 * prime.asm Output prime numbers from 0~254. (I don't think 2 is output, but forgive me. It was too much trouble to rewrite the assembly.)
 * hello.asm Outputs "Hello, World!\n
 * fib.asm Outputs the Fibonacci sequence from 0~254.

### Explanation (sort of)
The result of the operation is returned in the ax register.  
The specification of the comparison operator for the comparison instruction is done in the ax register.  
The specification of the number of the system call is also done in the ax register.  

Incidentally, since the registers are 8-bit, they originally have a single letter, such as a, b, c, d, but they are mistakenly called the ax, bx, cx, dx registers.  
There are also ac, bc, ic, pc, and sc registers, but some registers are not used because they were added on a whim, and some registers I don't understand.  
ax, bx, cx, dx, ex General-purpose registers (ax contains the return value of the calculation result)  
ac Address counter (position of the program currently being read)  
bc base counter (I don't remember what I added it for. Maybe the address of the function caller)  
ic I don't know  
pc I don't know  
sc Stack counter (current stack position)  

Is this what the description is for now? I will add more if necessary.  
That is all.  

Site used : [deepl](https://www.deepl.com/)
