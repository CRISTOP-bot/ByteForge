; ByteForge x86-64 NASM primitive, System V AMD64 ABI.
; size_t bf_choose(const uint32_t *token_ids, const uint64_t *counts, size_t n)
; Returns the array index with greatest frequency; ties choose lower token ID.
; Returns -1 when n == 0. This routine is a safe, standalone inference primitive.
global bf_choose
section .text
bf_choose:
    test rdx, rdx
    jz .empty
    xor r8d, r8d             ; current index
    xor r9d, r9d             ; best index
    mov r10, [rsi]           ; best frequency
.loop:
    cmp r8, rdx
    jae .done
    mov rax, [rsi + r8*8]
    cmp rax, r10
    ja .update
    jb .next
    mov ecx, [rdi + r8*4]
    mov r11d, [rdi + r9*4]
    cmp ecx, r11d
    jb .update
.next:
    inc r8
    jmp .loop
.update:
    mov r10, rax
    mov r9, r8
    jmp .next
.done:
    mov rax, r9
    ret
.empty:
    mov rax, -1
    ret
