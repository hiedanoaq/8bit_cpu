start:
true
jmp main

fib:
mov cx, 0
mov bx, 1
true
jmp L5

L6:
mov ax, 0
syscall
mov dx, bx
add bx, cx
mov bx, ax
mov cx, dx

L5:
mov ax, 2
mov dx, 255
cmp bx, dx
jmp L6
true
jmp end

main:
true
jmp fib

end:
mov ax, 0xff
syscall
exit