#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <linux/if.h>

#include "ra_ioctl.h"

#define MAX_IFNAME_LEN      20
#define IFR_NAME "eth0"

#define WAN_LAN_1_INDEX 0
#define WAN_LAN_2_INDEX 1
#define WAN_LAN_3_INDEX 2
#define WAN_LAN_4_INDEX 3
#define WAN_PORT_INDEX  4

enum {
    NETWORK_GET_LINK_STATUS = 1,
};

struct network_link_status_t{
    char ifname[MAX_IFNAME_LEN];
    int link_status;
    int speed;
    int duplex;
};

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
}

/*
 * Get link status
 */
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
	printf ("ioctl success for %s\n", ifr.ifr_name);

	network_link_status_set(&data, lsp, port_idx);

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

    if (network_link_status_ioctl(lsp, port_idx) < 0)
        return -1;

    printf ("= Port Name : %s, link_status : %d, speed: %d, duplex: %d =\n",
            lsp->ifname, lsp->link_status, lsp->speed, lsp->duplex);

    close (nl_sock);

    return lsp->link_status;
}
