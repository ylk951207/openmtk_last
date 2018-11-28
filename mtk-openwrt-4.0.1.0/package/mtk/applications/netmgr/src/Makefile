
# Definitions 
# ----------------------------------------------------------------------------

TARGET = netmgrd

SRC = $(wildcard *.c)
OBJ = $(SRC:.c=.o)

CFLAGS+=-g -Wall -O2

# Rules
# ----------------------------------------------------------------------------
all: ${TARGET}

.c.o:
	@echo "  CC      $@"
	$(CC) -c $(CFLAGS) $(INCLUDE) $<

netmgrd: $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $@	

#clean:
#	rm -rf *.o ${TARGET}

#.depend:
#	$(Q)$(MAKE) depend

