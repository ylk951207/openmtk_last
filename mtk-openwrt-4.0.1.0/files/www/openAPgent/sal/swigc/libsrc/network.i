%module network
%{
extern int network_link_status_get(int port_idx);
extern int wireless_station_get(char *ifname, char *filename);
%}
extern int network_link_status_get(int port_idx);
extern int wireless_station_get(char *ifname, char *filename);
