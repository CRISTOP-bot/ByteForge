# x86-64 assembly primitive

`choose.asm` exports `bf_choose(token_ids, counts, n)` using the System V AMD64 calling convention. It returns the index of the largest frequency and breaks ties by lower token ID. For `n == 0` it returns `-1`.

This is a genuine NASM routine, not the complete parser or language model. No NASM or linker is present in the current environment; CI assembles it and a C harness tests its ABI and behavior. Do not treat source presence as proof of a successful assembly.

Build in CI with: `nasm -f elf64 choose.asm -o choose.o`.
