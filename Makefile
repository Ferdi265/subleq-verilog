SOURCES = $(wildcard *.v)
TARGET = $(shell basename `realpath .`)

$(TARGET): $(SOURCES)
	iverilog -Wall -o $@ $^

.PHONY: clean
clean:
	rm -f $(TARGET)
