/*
 * netmgr_main.c -
 */
#include <signal.h>
#include <time.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <linux/netlink.h>
#include <linux/rtnetlink.h>
#include <linux/if.h>


#include "netmgr.h"


/* #undef NETMGR_SERVER_SOCK_SUPPORT */


/* Globals pointer. */
struct netmgr_globals *nmg = NULL;

#define GET_NUMFDS(N,S)                         N = (S >= N)? S + 1: N



/************************ RTNETLINK HELPERS ************************/
/*
 * The following code is extracted from :
 * ----------------------------------------------
 * libnetlink.c RTnetlink service routines.
 *
 *      This program is free software; you can redistribute it and/or
 *      modify it under the terms of the GNU General Public License
 *      as published by the Free Software Foundation; either version
 *      2 of the License, or (at your option) any later version.
 *
 * Authors: Alexey Kuznetsov, <kuznet@ms2.inr.ac.ru>
 * -----------------------------------------------
 */

void 
netmgr_rtnl_close(struct rtnl_handle *rth)
{
	if (rth->fd > 0)
    	close(rth->fd);
	rth->fd = -1;
}

int 
netmgr_rtnl_open(struct rtnl_handle *rth, unsigned subscriptions)
{
    int addr_len;

    memset(rth, 0, sizeof(struct rtnl_handle));

    rth->fd = socket(PF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
    if (rth->fd < 0) {
        NMG_LOG(LOG_ERR, "Cannot open netlink socket");
        return -1;
    }

    memset(&rth->local, 0, sizeof(rth->local));
    rth->local.nl_family = AF_NETLINK;
    rth->local.nl_groups = subscriptions;

    if (bind(rth->fd, (struct sockaddr*)&rth->local, sizeof(rth->local)) < 0) {
        NMG_LOG(LOG_ERR, "Cannot bind netlink socket");
        return -1;
    }
    addr_len = sizeof(rth->local);
    if (getsockname(rth->fd, (struct sockaddr*)&rth->local,
            (socklen_t *) &addr_len) < 0) {
        NMG_LOG(LOG_ERR, "Cannot getsockname");
        return -1;
    }
    if (addr_len != sizeof(rth->local)) {
        NMG_LOG(LOG_ERR,  "Wrong address length %d\n", addr_len);
        return -1;
    }
    if (rth->local.nl_family != AF_NETLINK) {
        NMG_LOG(LOG_ERR,  "Wrong address family %d\n", rth->local.nl_family);
        return -1;
    }
    rth->seq = time(NULL);
    return 0;
}

int 
netmgr_parse_rtattr(struct rtattr *tb[], int max, struct rtattr *rta, int len)
{
	while (RTA_OK(rta, len)) {
		if (rta->rta_type <= max)
			tb[rta->rta_type] = rta;
		rta = RTA_NEXT(rta,len);
	}
	
	if (len)
		NMG_LOG(LOG_ERR,  "!!!Deficit %d, rta_len=%d\n", len, rta->rta_len);
	return 0;
}


const char *
netmgr_get_netlink_type_string(unsigned int type)
{
	switch (type)
	{
		case RTM_NEWLINK:
			return "RTM_NEWLINK";
		case RTM_DELLINK:
			return "RTM_DELLINK";
		case RTM_NEWADDR:
			return "RTM_NEWADDR";
		case RTM_DELADDR:
			return "RTM_DELADDR";
		case RTM_NEWROUTE:
			return "RTM_NEWROUTE";
		case RTM_DELROUTE:
			return "RTM_DELROUTE";
		default:
			return "Unknown";
	}
}


/* ---------------------------------------------------------------- */
/*
 */
int
netmgr_rtnl_link_change (struct sockaddr_nl *snl, struct nlmsghdr *h)
{
	int len;
	char *name;
	struct ifinfomsg *ifi;
	struct rtattr *tb [IFLA_MAX + 1];
	
	ifi = NLMSG_DATA (h);

	len = h->nlmsg_len - NLMSG_LENGTH (sizeof (struct ifinfomsg));
	if (len < 0)
	{
		NMG_LOG(LOG_ERR, "no length\n");
  		return -1;
	}
	
	/* Looking up interface name. */
	memset (tb, 0, sizeof tb);
	netmgr_parse_rtattr (tb, IFLA_MAX, IFLA_RTA (ifi), len);
	if (tb[IFLA_IFNAME] == NULL)
	  return -1;
	name = (char *)RTA_DATA(tb[IFLA_IFNAME]);

	if(name)
	{
		if (h->nlmsg_type == RTM_NEWLINK)
			NMG_LOG(LOG_INFO,  "Add new %s Link!!\n", name);
		else
			NMG_LOG(LOG_INFO,  "Delete %s link!!\n", name);
	}
	return 0;

}


int
netmgr_sock_open(int port, int server_flag)
{
	int sock;
	struct sockaddr_in addr;
	
	sock = socket(AF_INET, SOCK_STREAM, 0);
	if (sock < 0)
	{
		NMG_LOG(LOG_ERR, "apclient socket() failed, %s\n", strerror(errno));
		return -1;
	}

	memset (&addr, 0x00, sizeof (struct sockaddr_in));
	addr.sin_family = AF_INET;
	addr.sin_port = htons(port);
	addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

	if (server_flag)
	{
		if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
		{
			NMG_LOG(LOG_ERR, "bind() failed, %s(port:%d)", 
					strerror(errno), NETMGR_APCLIENT_MESSAGE_PORT);
			close(sock);
			return -1;
		}

		if (listen (sock, 10) < 0)
		{
			NMG_LOG(LOG_ERR, "listen() failed, %s(port:%d)", 
					strerror(errno), NETMGR_APCLIENT_MESSAGE_PORT);
			close(sock);
			return -1;
		}
	}
	else
	{
		if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
		{
			NMG_LOG(LOG_ERR, "connect() failed, %s(port:%d)", 
					strerror(errno), NETMGR_APCLIENT_MESSAGE_PORT);
			close(sock);
			return -1;
		}
	}

	NMG_LOG(LOG_INFO, "%s socket init success(sock:%d) for port(%d)\n", 
			server_flag?"Server":"Client", sock, port);
	
	return sock;

}


int
netmgr_notify_if_addr_change(char *name, struct in_addr *inaddr)
{
	int n;
	char buffer[64] = {0};
	int apclient_sock;

	if (! inaddr)
		NMG_LOG(LOG_WARNING, "%s[%d] inaddr is null\n", __FUNCTION__, __LINE__);

	apclient_sock = netmgr_sock_open(NETMGR_APCLIENT_MESSAGE_PORT, 0);
	if (apclient_sock < 0)
	{
		NMG_LOG(LOG_ERR, "Can't initialize apclient socket\n");
		return -1;
	}
	
	snprintf (buffer, sizeof (buffer), "netmgr:%s %s",name?name:"unknown", inet_ntoa(*inaddr));

	n = write(apclient_sock, buffer, strlen(buffer));
	if (n < 0)
	{
		NMG_LOG(LOG_ERR, "write() failed, %s", strerror(errno));
		close (apclient_sock);
		return -1;
	}
	NMG_LOG(LOG_INFO, "%s[%d] write %d length\n", __FUNCTION__, __LINE__, n);

	close(apclient_sock);

	return 0;
}

int 
netmgr_rtnl_if_addr_change (struct sockaddr_nl *snl, struct nlmsghdr *h, void *jarg)
{
	int len;
	struct ifaddrmsg *ifa;
	struct rtattr *tb [IFA_MAX + 1];
	void *addr = NULL;
	void *broad = NULL;
	int secondary = 0;
	char *label = NULL;
	char *name = NULL;

	ifa = NLMSG_DATA (h);

	if (ifa->ifa_family != AF_INET)
		return 0;

	if (h->nlmsg_type != RTM_NEWADDR && h->nlmsg_type != RTM_DELADDR)
		return 0;

	len = h->nlmsg_len - NLMSG_LENGTH(sizeof (struct ifaddrmsg));
	if (len < 0) {
		return -1;
	}

	memset (tb, 0, sizeof tb);
	
	netmgr_parse_rtattr (tb, IFA_MAX, IFA_RTA (ifa), len);

	/* if index check */
#if 0
	if (ifa->ifa_index != (unsigned int)jarg)
		return 0;
#endif
	if (tb[IFA_ADDRESS] == NULL)
		tb[IFA_ADDRESS] = tb[IFA_LOCAL];

	if (tb[IFA_ADDRESS])
		addr = RTA_DATA (tb[IFA_ADDRESS]);
	else
		addr = NULL;

	if (tb[IFA_BROADCAST])
		broad = RTA_DATA(tb[IFA_BROADCAST]);
	else
		broad = NULL;

	/* Flags. */
	if (ifa->ifa_flags & IFA_F_SECONDARY)
		secondary = 1;

#if 0
	/* Label */
	if (tb[IFA_LABEL]) {
		label = (char *) RTA_DATA (tb[IFA_LABEL]);
		if (label)
		{
			if (strcmp (label, (char *)jarg))
				return 0;
		}
		else
			fprintf(stderr, "no label\n");
	}
#endif

	if (tb[IFLA_IFNAME])
	{
		name = (char *)RTA_DATA(tb[IFLA_IFNAME]);
		if (name)
			NMG_LOG(LOG_DEBUG,  "ifname: %s\n", name);
	}

	/* Callback */
	if (h->nlmsg_type == RTM_DELADDR)
	{
		NMG_LOG(LOG_INFO, "IP-CHANGED: Delete ip address for %s\n", 
				name?name:"unkown");
	}
	else
	{
		struct in_addr *inaddr = addr;
		NMG_LOG(LOG_INFO, "IP-CHANGED: Add new ip address for %s(%s)\n", 
			name?name:"unknown", inet_ntoa(*inaddr));
#if 0
		netmgr_notify_if_addr_change(name, inaddr);
#else
        char cmdstr[128] = {0};
        snprintf(cmdstr, 128, "cd /www/openAPgent;python -m utils/netmgr_notifier %s", name);
        system (cmdstr);
#endif
	}

	return 0;
}


/* ---------------------------------------------------------------- */
/*
 * We must watch the rtnelink socket for events.
 * This routine handles those events (i.e., call this when rth.fd
 * is ready to read).
 */

int 
netmgr_rtnl_recv(struct rtnl_handle *rtnl,
              void *jarg)
{
	int status;
	struct nlmsghdr *h;
	struct sockaddr_nl nladdr;
	struct iovec iov;
	char   buf[8192];
	struct msghdr msg = {
		(void*)&nladdr, sizeof(nladdr),
		&iov,   1,
		NULL,   0,
		0
	};

	memset(&nladdr, 0, sizeof(nladdr));
	nladdr.nl_family = AF_NETLINK;
	nladdr.nl_pid = 0;
	nladdr.nl_groups = 0;

	iov.iov_base = buf;

	do {
		iov.iov_len = sizeof(buf);
		status = recvmsg(rtnl->fd, &msg, 0);

		if (status < 0) {
			if (errno == EINTR)
				continue;
			perror("OVERRUN");
				continue;
		}
		if (status == 0) {
			NMG_LOG(LOG_ERR, "EOF on netlink\n");
			return -1;
		}
		if (msg.msg_namelen != sizeof(nladdr)) {
			NMG_LOG(LOG_ERR, "Sender address length == %d\n", msg.msg_namelen);
			return -1;
		}

		for (h = (struct nlmsghdr*)buf; status >= sizeof(*h); ) {
			int len = h->nlmsg_len;
			int l = len - sizeof(*h);

			if (l<0 || len>status) {
				if (msg.msg_flags & MSG_TRUNC) {
					NMG_LOG(LOG_ERR, "Truncated message\n");
					return -1;
				}
				NMG_LOG(LOG_ERR, "!!!malformed message: len=%d\n", len);
				return -1;
			}


			NMG_LOG(LOG_DEBUG, "Receive %s(0x%x) message\n", 
				netmgr_get_netlink_type_string(h->nlmsg_type), h->nlmsg_type);

			/*
			 * netlink message heandler 
			 */
			switch (h->nlmsg_type) {
				case RTM_NEWLINK:
				case RTM_DELLINK:
					netmgr_rtnl_link_change(&nladdr, h);
					break;
				case RTM_NEWADDR:
				case RTM_DELADDR:
					netmgr_rtnl_if_addr_change (&nladdr, h, jarg);
					break;
				default:
					break;
			}
									
			status -= NLMSG_ALIGN(len);
			h = (struct nlmsghdr*)((char*)h + NLMSG_ALIGN(len));
		}
		
		if (msg.msg_flags & MSG_TRUNC) {
			NMG_LOG(LOG_ERR, "Message truncated\n");
			continue;
		}
		if (status) {
			NMG_LOG(LOG_ERR, "!!!Remnant of size %d\n", status);
			return -1;
		}
	} while (0);

	return 0;
}


int
netmgr_server_handler()
{
	int csock, readn;
	socklen_t len;
	struct sockaddr_in addr;
	char buffer[256];
	
	csock = accept(nmg->serv_sock, (struct sockaddr *) &addr, &len);
	if (csock < 0)
	{
		NMG_LOG(LOG_ERR, "accept socket error: %s", strerror (errno));
		return -1;
	}

	readn = read(csock, buffer, sizeof (buffer) - 1);
	if (readn < 0) 
	{
		NMG_LOG(LOG_ERR, "readn socket error: %s", strerror (errno));
		close (csock);
		return -1;
	}

	NMG_LOG(LOG_INFO, "Read message (%s:%d) at socket(%d)\n", buffer, readn, csock);

	close (csock);
	return 0;
}


static inline int
netmgr_wait_for_event(struct rtnl_handle * rth)
{
#if 0
	struct timeval    tv; /* Select timeout */
#endif
	int  numfds = 0;
	int       ret;
	fd_set    rfds;       /* File descriptors for select */

	/* Forever */
	while(1)
	{
		/* Guess what ? We must re-generate rfds each time */
		FD_ZERO(&rfds);
		
		FD_SET(rth->fd, &rfds);
		GET_NUMFDS(numfds, rth->fd);
		
#ifdef NETMGR_SERVER_SOCK_SUPPORT
		FD_SET(nmg->serv_sock, &rfds);
		GET_NUMFDS(numfds, nmg->serv_sock);
#endif /* NETMGR_SERVER_SOCK_SUPPORT */

		/* Wait until something happens */
		ret = select(numfds, &rfds, NULL, NULL, NULL);

		/* Check if there was an error */
		if(ret < 0)
		{
			if(errno == EAGAIN || errno == EINTR)
				continue;
			NMG_LOG(LOG_ERR, "Unhandled signal - exiting...\n");
			break;
		}

		/* Check if there was a timeout */
		if(ret == 0)
		{
			continue;
		}

		/* Check for interface discovery events. */
		if(FD_ISSET(rth->fd, &rfds))
			netmgr_rtnl_recv(rth, NULL);

#ifdef NETMGR_SERVER_SOCK_SUPPORT
		if(FD_ISSET(nmg->serv_sock, &rfds))
			netmgr_server_handler();
#endif /* NETMGR_SERVER_SOCK_SUPPORT */

	}

	return(0);
}


/**
 * Initialize network manager
 */
int
netmgr_init()
{
	/* Allocation global variable */
	nmg = malloc (sizeof(struct netmgr_globals));
	if (nmg == NULL)
		return -1;

	memset (nmg, 0x00, sizeof (struct netmgr_globals));

	nmg->rth.fd = -1;

	nmg->rtnl_subscriptions = RTMGRP_IPV4_IFADDR;
	//nmg->rtnl_subscriptions = (RTMGRP_IPV4_IFADDR|RTMGRP_LINK);

#ifdef NETMGR_SERVER_SOCK_SUPPORT
	/* open notifier server socket */
	nmg->serv_sock = netmgr_sock_open(NETMGR_MSG_SERVER_PORT, 1);
	if (nmg->serv_sock < 0)
	{
		NMG_LOG(LOG_INFO, "Initialize netmgr serv_sock\n");
		return -1;
	}
#endif /* NETMGR_SERVER_SOCK_SUPPORT */
	
	NMG_LOG(LOG_INFO, "Initialize netmgr (rtnl_subscriptions: %d)\n",
			nmg->rtnl_subscriptions);

	return 0;
}

/**
 * Deinitialize network manager 
 */
void
netmgr_close()
{
	/* Cleanup - only if you are pedantic */
	netmgr_rtnl_close(&nmg->rth);
}


int 
main(int argc, char **argv)
{
	/* Signal Init */
	signal (SIGTERM, SIG_DFL);
	signal (SIGINT,  SIG_DFL);
	signal (SIGHUP,  SIG_DFL);
	signal (SIGPIPE, SIG_IGN);
	signal (SIGCHLD, SIG_DFL);

	/* Daemonize */

	/* netmgr initialize */
	if (netmgr_init() < 0)
	{
		NMG_LOG(LOG_ERR, "netmgr_initialize failed\n");
		return -1;
	}

	while (1) {
		if (! access ("/tmp/provisioning-done", F_OK))
			break;
		sleep(3);
	}

	while (1)
	{
		/* Open netlink channel */
		if(netmgr_rtnl_open(&nmg->rth, nmg->rtnl_subscriptions) < 0)
		{
			NMG_LOG(LOG_ERR, "Can't initialize rtnetlink socket\n");
			netmgr_close();
			continue;
		}

		NMG_LOG(LOG_INFO, "Waiting for Wireless Events from interfaces...\n");
		
		/* Do what we have to do */
		netmgr_wait_for_event(&nmg->rth);

		netmgr_close();
	}

	if (nmg)
		free (nmg);
	
	return 0;
}
