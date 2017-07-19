| **ip commands**                                           | **comments**                                                                       |
|-----------------------------------------------------------|------------------------------------------------------------------------------------|
| `ip a` or `ip addr`                                       | Display ip address and property information                                        |
| `ip a show dev <device>`                                  | Show information about the particular `<device>`                                   |
| `ip link` (`ls up`)                                       | Show state of all interfaces / only interfaces that are up                         |
| `ip link set <device> <up/down>`                          | Take the interface up or down                                                      |
| `ip -s link` (`show dev <device>`)                        | Show the statistics for all the links / particular device                          |
| `ip route`                                                | Show the routing information                                                       |
| `ip route add <host_ip/default> via <gw_ip> dev <device>` | Set routing for a particular host_ip using particular gw over particular interface |
| `ip route get <host_ip>`                                  | Show the route taken to reach this host                                            |
| `ip neigh` (`add/del/change`) `<host_ip> dev <device>`    | Show all the neighbors that it has connected to                                    |
| `ping -I <dev> <host_ip>`                                 | Ping the host via particular interface                                             |
| `dhcpcd -U <dev>`                                         | Dump the dhcp lease info                                                                                   |
| `iwconfig <dev>`                                          | Show only the wireless interfaces and its properties                                                       |
| `iwlist <dev> scan essid <essid>`                         | Use wireless interface for performing scan (optionally, pass the essid you want to scan)                   |

