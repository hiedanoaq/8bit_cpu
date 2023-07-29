start:
true
jmp main

prime:
mov [0x00], 2
mov [0x40], 1
mov [0x41], 3
true
jmp L9

L10:
mov [0x42], 1
mov [0x43], 0
true
jmp L11

L12:
L13:
mov ax, [0x41]
mov bx, [0x43]
mov bx, [bx]
mod ax, bx
mov bx, ax
mov cx, 0
mov ax, 1
cmp bx, cx
jmp LE11

L14:
mov ax, 0
mov [0x42], ax
true
jmp L18

LE11:
mov ax, [0x43]
mov bx, 1
add ax, bx
mov [0x43], ax

L11:
mov ax, 3
mov bx, [0x40]
mov cx, [0x43]
cmp bx, cx
jmp L12

L18:
mov ax, 1
mov bx, [0x42]
mov cx, 1
cmp bx, cx
jmp LE9

L19:
mov ax, 0
mov bx, [0x41]
syscall
mov ax, [0x40]
mov [ax], [0x41]
mov ax, [0x40]
mov bx, 1
add ax, bx
mov [0x40], ax


LE9:
mov ax, [0x41]
mov bx, 1
add ax, bx
mov [0x41], ax

L9:
mov ax, 2
mov bx, [0x41]
mov cx, 255
cmp bx, cx
jmp L10

L23:
true
jmp end

main:
true
jmp prime

end:
mov ax, 255
syscall
exit