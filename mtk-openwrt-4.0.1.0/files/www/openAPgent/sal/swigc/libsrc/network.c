#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <linux/if.h>
#include <linux/wireless.h>

#include "ra_ioctl.h"
#include "swig_network.h"


int nl_sock;

/*
 * Initialize netlink socket
 */
void
network_nl_sock_init(void)
{
  nl_sock = socket(AF_INET, SOCK_DGRAM, 0);
  if (nl_sock < 0) {
    perror("socket");
    exit(0);
  }
}

/*
 * Get link status
 */
void
network_link_status_set(struct ra_switch_ioctl_data *data,
                            struct network_link_status_t *lsp,
                            int port_idx)
{
    if (data == NULL)
        return;

    printf ("= input = port index:%d\n", port_idx);
    printf ("= Input = link_status : %d, speed: %d, duplex: %d\n",
             data->link_status, data->speed, data->duplex);

    snprintf (lsp->ifname, MAX_IFNAME_LEN, "Port %d", port_idx);
    lsp->link_status = data->link_status;
    if (lsp->link_status > 0)
    {
        lsp->speed = data->speed;
        lsp->duplex = data->duplex;
    }
    else
    {
        lsp->speed = 0;
        lsp->duplex = 0;
    }
    return;
}

int
network_link_status_ioctl(struct network_link_status_t *lsp,
                              int port_idx)
{
	struct ifreq ifr;
	struct ra_switch_ioctl_data data;

	data.port = port_idx;
	data.cmd = SW_IOCTL_GET_PHY_STATUS;
	strncpy(ifr.ifr_name, IFR_NAME, 5);
    ifr.ifr_data = &data;

	if (-1 == ioctl(nl_sock, RAETH_SW_IOCTL, &ifr)) {
		perror("ioctl");
            close(nl_sock);
		return -1;
	}
	network_link_status_set(&data, lsp, port_idx);
	printf ("network_link_status_ioctl success for %s\n", ifr.ifr_name);

	return 0;
}

int
network_link_status_get(int port_idx)
{
    struct network_link_status_t link_status, *lsp;

    lsp = &link_status;
    memset (lsp, 0, sizeof (struct network_link_status_t));

    /* Initialize netlink socket */
    network_nl_sock_init();

    if (network_link_status_ioctl(lsp, port_idx) < 0) {
        close (nl_sock);
        return -1;
    }

    printf ("= Port Name : %s, link_status : %d, speed: %d, duplex: %d =\n",
            lsp->ifname, lsp->link_status, lsp->speed, lsp->duplex);

    close (nl_sock);

    return lsp->link_status;
}

/*
 * Get Wireless stations
 */
int
wireless_make_station_file(RT_802_11_MAC_TABLE *table, char *filename)
{
    int i;
    FILE *fp;
    char *phyMode[4] = {"CCK", "OFDM", "MM", "GF"};

    fp = fopen (filename, "w+");
    if (fp == NULL)
        return -1;

    printf ("Write wireless station to file (num:%d)\n", table->Num);

    for (i = 0; i < table->Num; i++) {
        RT_802_11_MAC_ENTRY *pe = &(table->Entry[i]);

        fprintf(fp, "%-15s:%02X:%02X:%02X:%02X:%02X:%02X\n", "macAddr",
                pe->Addr[0], pe->Addr[1], pe->Addr[2], pe->Addr[3], pe->Addr[4], pe->Addr[5]);
        fprintf(fp, "%-15s:%d\n", "TxRate_MCS ", pe->TxRate.field.MCS);
        fprintf(fp, "%-15s:%d\n", "TxRate_BW", pe->TxRate.field.BW? 40: 20);
        fprintf(fp, "%-15s:%s\n", "TxRate_GI", pe->TxRate.field.ShortGI? "Short": "Long");
        fprintf(fp, "%-15s:%s\n", "TxRate_PhyMode", phyMode[pe->TxRate.field.MODE]);
        fprintf(fp, "%-15s:%s\n", "TxRate_STBC", pe->TxRate.field.STBC? "STBC": " ");
        fprintf(fp, "%-15s:%d\n", "AvgRssi0", (int)(pe->AvgRssi0));
        fprintf(fp, "%-15s:%d\n", "AvgRssi1", (int)(pe->AvgRssi1));
        fprintf(fp, "%-15s:%d\n", "AvgRssi2", (int)(pe->AvgRssi2));
        fprintf(fp, "%-15s:%d\n\n", "connectTime", pe->ConnectedTime);
    }

    fclose(fp);
    return 0;
}

int
wireless_station_ioctl(char *ifname, char *filename)
{
	struct iwreq iwr;
	RT_802_11_MAC_TABLE table = {0};
#define RTPRIV_IOCTL_GET_MAC_TABLE_STRUCT  (SIOCIWFIRSTPRIV + 0x1F)

    if (ifname == NULL)
        return -1;

    printf ("ifname: %s\n", ifname);
    strncpy(iwr.ifr_name, ifname, IFNAMSIZ);
    iwr.u.data.pointer = (caddr_t) &table;

    if (ioctl(nl_sock, RTPRIV_IOCTL_GET_MAC_TABLE_STRUCT, &iwr) < 0) {
        printf("ioctl() error : %s\n", strerror(errno));
        return -1;
    }

    if (wireless_make_station_file(&table, filename) < 0) {
        printf ("Cannot generate wireless file\n");
        return -1;
    }

	return 0;
}

int
wireless_station_get(char *ifname, char *filename)
{
    /* Initialize netlink socket */
    network_nl_sock_init();

    if (wireless_station_ioctl(ifname, filename) < 0) {
        close (nl_sock);
        return -1;
    }

    close (nl_sock);
    return 0;
}

