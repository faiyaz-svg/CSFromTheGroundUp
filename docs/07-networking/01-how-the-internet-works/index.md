# How the internet works

A cheat sheet for the chapter: what travels, how it is addressed, which layer does what, and how names become addresses.

Lessons:

1. [Packets, routers and the internet](01-packets-routers-and-the-internet.md)
2. [IP addresses, subnets and NAT](02-ip-addresses-subnets-and-nat.md)
3. [Network layers, TCP and UDP](03-network-layers-tcp-and-udp.md)
4. [Ports and sockets](04-ports-and-sockets.md)
5. [DNS and domains](05-dns-and-domains.md)

## Key terms

| Term | Meaning |
|---|---|
| Packet | A small chunk of data with a header holding source and destination addresses |
| Router, hop | A machine that forwards packets toward their destination; one forwarding step |
| Default gateway | The router a device uses for anything outside its own subnet |
| TTL / hop limit | A counter lowered at each router; at 0 the packet is dropped (how traceroute works) |
| Latency, bandwidth | Delay before the first byte; bytes per second once flowing |
| IPv4, IPv6 | 32-bit and 128-bit addresses |
| CIDR, subnet mask | `address/prefix` notation for a block; the same split written as `255.255.255.0` |
| Private address | RFC 1918 ranges, not routed on the internet |
| NAT | The router rewrites private addresses and ports to its public ones and keeps a table |
| DHCP | Gives a device an address, mask, gateway and DNS server automatically |
| Loopback | `127.0.0.1` / `localhost`; traffic never leaves the machine |
| Encapsulation | Each layer adds its own header around the data from the layer above |
| TCP, UDP | Reliable ordered byte stream with a handshake; unreliable single messages |
| Port, socket | 16-bit number naming a program; IP address plus port plus protocol |
| 4-tuple | Source address and port, destination address and port: identifies a connection |
| Stub, recursive, authoritative | The OS client; the server that walks the tree; the server that owns the records |
| TTL (DNS) | Seconds an answer may be cached |

## Layers

| TCP/IP layer | OSI layers | Unit | Examples |
|---|---|---|---|
| Application | 5, 6, 7 | message | HTTP, DNS, SSH, TLS |
| Transport | 4 | segment or datagram | TCP, UDP |
| Internet | 3 | packet | IP, ICMP |
| Link | 1, 2 | frame | Ethernet, Wi-Fi |

## Private ranges and special addresses

| Range | Use |
|---|---|
| 10.0.0.0/8 | Private (RFC 1918) |
| 172.16.0.0/12 | Private, `172.16.0.0` to `172.31.255.255` |
| 192.168.0.0/16 | Private, most home routers |
| 127.0.0.0/8 | Loopback |
| 0.0.0.0 | "All interfaces" when binding a server |
| 203.0.113.0/24, 198.51.100.0/24 | Documentation examples |

## CIDR quick table (IPv4)

A /$p$ block holds $2^{32-p}$ addresses; usable hosts are two fewer (network and broadcast). Some cloud providers reserve more.

| Prefix | Mask | Addresses | Usable hosts |
|---|---|---|---|
| /8 | 255.0.0.0 | 16,777,216 | 16,777,214 |
| /12 | 255.240.0.0 | 1,048,576 | 1,048,574 |
| /16 | 255.255.0.0 | 65,536 | 65,534 |
| /20 | 255.255.240.0 | 4,096 | 4,094 |
| /22 | 255.255.252.0 | 1,024 | 1,022 |
| /24 | 255.255.255.0 | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64 | 62 |
| /27 | 255.255.255.224 | 32 | 30 |
| /28 | 255.255.255.240 | 16 | 14 |
| /29 | 255.255.255.248 | 8 | 6 |
| /30 | 255.255.255.252 | 4 | 2 |

## Common ports

From the [IANA registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml), as of 2026. Ports 0 to 1023 are well-known, 1024 to 49151 registered, 49152 to 65535 dynamic.

| Port | Service |
|---|---|
| 21 | FTP (control) |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP (mail between servers) |
| 53 | DNS (UDP, and TCP for large answers) |
| 67, 68 | DHCP (server, client) |
| 80 | HTTP |
| 110 | POP3 |
| 123 | NTP |
| 143 | IMAP |
| 443 | HTTPS |
| 445 | SMB (Windows file sharing) |
| 465, 587 | Mail submission (TLS, STARTTLS) |
| 993 | IMAP over TLS |
| 3306 | MySQL |
| 3389 | Remote Desktop |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 8080 | HTTP alternate |
| 27017 | MongoDB |

## Commands

| Task | Windows (PowerShell) | WSL or Linux (unverified here) |
|---|---|---|
| Show addresses | `ipconfig` | `ip addr` |
| Show routes, gateway | `ipconfig`, `route print` | `ip route` |
| Path to a host | `tracert -d example.com` | `traceroute -n example.com` |
| Round trip time | `ping -n 4 example.com` | `ping -c 4 example.com` |
| Resolve a name | `nslookup example.com` | `dig example.com` |
| Resolve a record type | `nslookup -type=MX gmail.com` | `dig MX gmail.com` |
| Ask one server | `nslookup example.com 1.1.1.1` | `dig @1.1.1.1 example.com` |
| Listening ports and owners | `netstat -ano -p tcp` | `ss -ltnp` |
| Flush the DNS cache | `ipconfig /flushdns` | depends on the resolver |
| Public address | `curl -s https://ifconfig.me` | same |

## Rules of thumb

- `* * *` in a traceroute is not an outage if later hops answer.
- A device sends to the default gateway for any address outside its subnet.
- TCP gives order and delivery, not encryption. UDP gives neither.
- Binding to `127.0.0.1` keeps a server local; `0.0.0.0` exposes it to the network.
- "Address already in use": another socket listens on that port. Find it with `netstat -ano` or `ss -ltnp`.
- A DNS change is visible only after cached copies expire, so wait one old TTL (longer for name server changes).
- A CNAME can't share a name with other records.
