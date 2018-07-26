#! /bin/sh

MTK_IMAGE_NAME=mtk-openwrt-4.0.1.0/bin/targets/mediatek/mt7622-glibc/lede-mediatek-mt7622-MTK-AC2600-RFB1-squashfs-sysupgrade.bin
VERSION_FILE=mtk-openwrt-4.0.1.0/files/etc/openwrt_release

#Change /tmp directory owner during openwrt compile.
#'root' user cannot build openwrt, but some packages have to make a directory in /tmp. 
change_tmp_owner()
{
#    echo $1
    sudo chown $1:$1 /tmp
}


case $1 in
openwrt)
    echo "Compile openwrt"
   
    change_tmp_owner $(whoami)

    cd mtk-openwrt-4.0.1.0
    make V=s
    
    change_tmp_owner root
    ;;
bootloader)
    echo "Compile bootloader"
    ;;
openwrt-release)
    grep DISTRIB_RELEASE ${VERSION_FILE}  | awk -F"'" '{print $2}' > .mtk_version
    version=$(cat .mtk_version)
    sudo cp ${MTK_IMAGE_NAME} /tftpboot/mtk4010_mt7622_AC2600_${version}.bin
    ;;
esac
