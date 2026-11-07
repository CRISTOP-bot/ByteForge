CXX ?= c++
CXXFLAGS ?= -std=c++17 -O2 -Wall -Wextra -Werror

byteforge: byteforge.cpp
	$(CXX) $(CXXFLAGS) $< -o $@
clean:
	rm -f byteforge
.PHONY: clean
