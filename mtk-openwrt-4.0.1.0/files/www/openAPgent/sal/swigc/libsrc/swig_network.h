
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


/*
 * Wireless
 */


typedef union _MACHTTRANSMIT_SETTING {
  struct  {
    unsigned short  MCS:7;  // MCS
    unsigned short  BW:1;   //channel bandwidth 20MHz or 40 MHz
    unsigned short  ShortGI:1;
    unsigned short  STBC:2; //SPACE
    unsigned short  eTxBF:1;
    unsigned short  rsv:1;
    unsigned short  iTxBF:1;
    unsigned short  MODE:2; // Use definition MODE_xxx.
  } field;
  unsigned short      word;
} MACHTTRANSMIT_SETTING;

typedef struct _RT_802_11_MAC_ENTRY {
  unsigned char           ApIdx;
  unsigned char           Addr[6];
  unsigned char           Aid;
  unsigned char           Psm;     // 0:PWR_ACTIVE, 1:PWR_SAVE
  unsigned char           MimoPs;  // 0:MMPS_STATIC, 1:MMPS_DYNAMIC, 3:MMPS_Enabled
  char                    AvgRssi0;
  char                    AvgRssi1;
  char                    AvgRssi2;
  unsigned int            ConnectedTime;
  MACHTTRANSMIT_SETTING   TxRate;
  unsigned int            LastRxRate;
  short                   StreamSnr[3];
  short                   SoundingRespSnr[3];
#if 0
  short                   TxPER;
  short                   reserved;
#endif
} RT_802_11_MAC_ENTRY;

#define MAX_NUMBER_OF_MAC               116

typedef struct _RT_802_11_MAC_TABLE {
  unsigned long            Num;
  RT_802_11_MAC_ENTRY      Entry[MAX_NUMBER_OF_MAC]; //MAX_LEN_OF_MAC_TABLE = 32
} RT_802_11_MAC_TABLE;

#define WIRELESS_STATION_FILE_NAME  "/tmp/wireless_stations"
