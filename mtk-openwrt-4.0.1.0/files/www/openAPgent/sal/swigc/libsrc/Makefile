
# Beautify output
# ----------------------------------------------------------------------------
ifdef V
ifeq ("$(origin V)", "command line")
BUILD_VERBOSE = $(V)
endif
endif
ifndef BUILD_VERBOSE
BUILD_VERBOSE = 0
endif

ifeq ($(BUILD_VERBOSE),1)
Q =
else
Q = @
endif



# Definitions 
# ----------------------------------------------------------------------------

WORK_DIR=../../../../../../
TARGET_BUILD_DIR=${WORK_DIR}/build_dir/target-aarch64_cortex-a53+neon-vfpv4_glibc-2.24

PATH:=${PATH}:${WORK_DIR}/staging_dir/toolchain-aarch64_cortex-a53+neon-vfpv4_gcc-5.4.0_glibc-2.24/bin

#CC = gcc
#LD = ld
CC = aarch64-openwrt-linux-gcc
LD = aarch64-openwrt-linux-ld

TARGETS = sys_usage network

SYS_USAGE_SRCS = sys_usage.c sys_usage_wrap.c
SYS_USAGE_OBJS = sys_usage.o sys_usage_wrap.o
SYS_USAGE_LIB = _sys_usage.so


NETWORK_SRCS = network.c network_wrap.c
NETWORK_OBJS = network.o network_wrap.o
NETWORK_LIB = _network.so

LIBS = ${SYS_USAGE_LIB} ${NETWORK_LIB}
WRAP_SRCS = sys_usage_wrap.c network_wrap.c
PYTHON_SRCS = network.py sys_usage.py


RELEASE_DIR=${WORK_DIR}/files/www/openAPgent/common/libs


# Rules
# ----------------------------------------------------------------------------
all: ${TARGETS}

CFLAGS = -I/usr/local/include/python2.7 \
		-I${TARGET_BUILD_DIR}/linux-mediatek_mt7622/linux-4.4.124/drivers/net/ethernet/raeth \
		-fPIC

sys_usage:
	swig -python sys_usage.i
	${CC} -c ${SYS_USAGE_SRCS} ${CFLAGS} 
	${LD} -shared ${SYS_USAGE_OBJS} -o ${SYS_USAGE_LIB} 


network:
	swig -python network.i
	${CC} -c ${NETWORK_SRCS} ${CFLAGS} 
	${LD} -shared ${NETWORK_OBJS} -o ${NETWORK_LIB} 


release:
	cp ${LIBS} ${RELEASE_DIR}
	cp ${PYTHON_SRCS} ${RELEASE_DIR}


clean:
	rm -rf ${LIBS}
	rm -rf ${WRAP_SRCS} ${PYTHON_SRCS} *.pyc *.o
