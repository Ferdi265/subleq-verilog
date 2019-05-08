SOURCES = $(wildcard *.v)
TARGET = $(shell basename `realpath .`)

$(TARGET): $(SOURCES)
	iverilog -o $@ $^

.PHONY: clean
clean:
	rm -f $(TARGET)
