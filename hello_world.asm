@memory [0x00-0x0f] 48 65 6c 6c 6f 2c 20 57 6f 72 6c 64 21 00 00 00

start:
true
jmp main

print:
mov bx, ax
mov cx, 0
mov dx, 0
true
jmp L3

L4:
push bx
push cx
mov bx, ex
mov ax, 0x01
syscall
pop cx
mov bx, dx
mov ax, 0x00
syscall
pop bx

LE3:
mov fx, 1
add dx, fx
mov dx, ax

L3:
add bx, cx
mov ex, [ax]
mov ax, 1
mov fx, 0x00
cmp ex, fx
jmp L4

L8:
true
jmp end

main:
mov ax, 0x00
true
jmp print

end:
mov ax, 0xff
syscall
exit