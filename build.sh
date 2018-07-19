#! /bin/sh


case $1 in
openwrt)
    echo "Compile openwrt"
    cd mtk-openwrt-4.0.1.0
    make V=s
    ;;
bootloader)
    echo "Compile bootloader"
    ;;
esac
