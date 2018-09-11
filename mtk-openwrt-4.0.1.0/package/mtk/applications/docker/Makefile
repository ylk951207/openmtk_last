#
# Copyright (C) 2018 Withus Planet
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=docker
PKG_RELEASE:=1

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/package.mk

define Package/docker
  SECTION:=Withus Planet Properties
  CATEGORY:=Withus Planet Properties
  TITLE:=docker
  SUBMENU:=Applications
endef

define Package/docker/description
  Docker binary from Raspberry Pi
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) ./src/* $(PKG_BUILD_DIR)/
endef

define Package/docker/install
	$(INSTALL_DIR) $(1)/root
	$(INSTALL_DIR) $(1)/root/makeContainer
	$(INSTALL_DIR) $(1)/root/makeContainer/chrony
	$(INSTALL_DIR) $(1)/root/makeContainer/dnsmasq
	$(INSTALL_DIR) $(1)/root/makeContainer/net-snmp
	$(INSTALL_DIR) $(1)/root/makeContainer/net-snmp/net-snmp-5.7.3
	$(INSTALL_DIR) $(1)/root/makeContainer/net-snmp/net-snmp-5.7.3/bin
	$(INSTALL_DIR) $(1)/root/makeContainer/net-snmp/net-snmp-5.7.3/sbin
	$(INSTALL_DIR) $(1)/root/makeContainer/net-snmp/net-snmp-5.7.3/mibs
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_DIR) $(1)/etc/docker
	$(INSTALL_BIN) ./files/Dockerfile $(1)/root
	$(INSTALL_BIN) ./files/hello-world.sh $(1)/root
	$(INSTALL_BIN) ./files/build-hello.sh $(1)/root
	$(INSTALL_BIN) ./files/run-hello.sh $(1)/root
	$(INSTALL_BIN) ./files/docker* $(1)/usr/bin
	$(INSTALL_BIN) ./files/daemon.json $(1)/etc/docker
	$(INSTALL_BIN) ./files/makeContainer/chrony/run_chrony.sh $(1)/usr/sbin
	$(INSTALL_BIN) ./files/makeContainer/dnsmasq/run_dnsmasq.sh $(1)/usr/sbin
	$(INSTALL_BIN) ./files/makeContainer/chrony/* $(1)/root/makeContainer/chrony
	$(INSTALL_BIN) ./files/makeContainer/dnsmasq/* $(1)/root/makeContainer/dnsmasq
	$(INSTALL_BIN) ./files/makeContainer/net-snmp/run_snmpd.sh $(1)/usr/sbin
	$(INSTALL_BIN) ./files/makeContainer/net-snmp/*.sh $(1)/root/makeContainer/net-snmp
	$(INSTALL_BIN) ./files/makeContainer/net-snmp/dockerfile* $(1)/root/makeContainer/net-snmp
	$(INSTALL_BIN) ./files/makeContainer/net-snmp/snmpd.* $(1)/root/makeContainer/net-snmp
	$(INSTALL_BIN) ./files/makeContainer/net-snmp/net-snmp-5.7.3/snmp* $(1)/root/makeContainer/net-snmp/net-snmp-5.7.3/bin
	$(INSTALL_BIN) ./files/makeContainer/net-snmp/net-snmp-5.7.3/mibs/* $(1)/root/makeContainer/net-snmp/net-snmp-5.7.3/mibs
	$(INSTALL_BIN) ./files/makeContainer/net-snmp/net-snmp-5.7.3/sbin/* $(1)/root/makeContainer/net-snmp/net-snmp-5.7.3/sbin
endef

$(eval $(call BuildPackage,docker))

