/*
 * netmgr.h -
 */
#ifndef _WP_NETMGR_H
#define _WP_NETMGR_H
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <syslog.h>
#include <asm/types.h>

#define MAX_IFNAME_LEN  20

/* apclient's command socket */
#define NETMGR_APCLIENT_MESSAGE_PORT	8008



/**
 * rtnetlink 
 */
struct rtnl_handle
{
    int         fd;
    struct sockaddr_nl  local;
    struct sockaddr_nl  peer;
    __u32           seq;
    __u32           dump;
};


/**
 * Network Manager global variable
 */
struct netmgr_globals {
	
	/* bitmap of the rtnetlink multicast groups the socket will be a member of. */
	int rtnl_subscriptions;

	struct rtnl_handle rth;

#define NETMGR_MSG_SERVER_PORT	8007
	int serv_sock;
};



/**
 * Log 
 */
#if 0
#define NMG_LOG(level, format, args...)       printf(format, ## args)
#else
#define NMG_LOG(level, format, args...)             		\
do {                                       	 				\
	openlog ("netmgr", LOG_PID|LOG_NDELAY, LOG_DAEMON);    	\
	syslog (level, format, ## args);    					\
	closelog ();    										\
} while (0)
#endif




#endif /* _WP_NETMGR_H */
