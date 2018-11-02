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

compile_openwrt()
{
    echo "\nCompile openwrt(mtk-openwrt-4.0.1.0)\n"
   
    change_tmp_owner $(whoami)

    cd mtk-openwrt-4.0.1.0
    make -j 12
    
    change_tmp_owner root
}


case $1 in
openwrt-build)
    # Compile for the official version
    cp mtk-openwrt-4.0.1.0/files/www/openAPgent/common/env.py env.py~
    sed -e s/CAPC_SERVER_IP=\'192.168.1.182\'/CAPC_SERVER_IP=\'capc.withusp.com\'/g env.py~  > \
        mtk-openwrt-4.0.1.0/files/www/openAPgent/common/env.py
    echo "++++++++++++++ Modify mtk-openwrt-4.0.1.0/files/www/openAPgent/common/env.py +++++++++++++++"
    compile_openwrt
    ;;
openwrt)
    # Compile for the development version
		cp mtk-openwrt-4.0.1.0/files/www/openAPgent/common/env.py env.py~
		sed -e s/CAPC_SERVER_IP=\'capc.withusp.com\'/CAPC_SERVER_IP=\'192.168.1.182\'/g env.py~  > \
				mtk-openwrt-4.0.1.0/files/www/openAPgent/common/env.py
    echo "++++++++++++++ Modify mtk-openwrt-4.0.1.0/files/www/openAPgent/common/env.py +++++++++++++++"

    compile_openwrt
    ;;
bootloader)
    echo "Compile bootloader"
    ;;
openwrt-release)
    grep DISTRIB_RELEASE ${VERSION_FILE} | awk -F"'" '{print $2}' > .mtk_version
		#suffix='_$(date +%m%d)'
		suffix=''
    version=$(cat .mtk_version)
    sudo cp ${MTK_IMAGE_NAME} /tftpboot/mtk4010_mt7622_AC2600_${version}${suffix}.bin
    ;;
esac
