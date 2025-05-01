r8 = system - puts
r9 = puts-got
r10 = binsh - puts

Notes:
	We can chain gadgets 14 and 0 to do rax = rdi


Gadget Chain:
3,
2,


zero out rcx - 6, 5, 14, 0, 2


Gadget 0:
	rax = pop();
	RSP += 8
	ret()

Gadget 1
	rbx += r9
	ret()

Gadget 2:
	rcx = *(u64 *) rbx;
	ret()

Gadget 3:
	rax = r8;
	rbx = r9;
	rcx = r10;

Gadget 4;
	rcx ^= rdi
	rbx ^= rdi;
	ret();

Gadget 5:
	push(rax)
	rsp -= 8
	ret()

Gadget 6:
	rax = 0
	rsi = 0
	ret()

Gadget 7:
	rax -= 8
	idiv(rdi)
	rax = quotient
	rdx = rem
	ret()

Gadget 8:
	rdi += r8
	ret()

Gadget 9:
	ret()

Gadget 10:
	rbx *= rax
	ret()

Gadget 11:
	swap(r8, r9)
	ret()

Gadget 12:
	rcx = rsi
	rcx += r10

Gadget 13:
	rdi ^= rcx
	rsi ^= rcx

Gadget 14:
	rbx = pop()
	RSP += 8
	push(rdi)
	RSP -= 9
	push(rbx)
	RSP -= 9

Gadget 15:
	rbp = pop()
	RSP += 8
	rsi = pop()
	RSP += 8;


