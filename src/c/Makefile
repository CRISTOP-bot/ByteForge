CC ?= cc
CFLAGS ?= -std=c11 -O2 -Wall -Wextra -Werror

byteforge: byteforge.c
	$(CC) $(CFLAGS) $< -o $@
clean:
	rm -f byteforge
.PHONY: clean
