#!/usr/bin/env python
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink, Intf
from mininet.log import setLogLevel
import os

if'__main__'==__name__:
	setLogLevel('info')
	net = Mininet(link=TCLink)
	value = 0
	os.system('mn -c')

	#Build Topology
	HA = net.addHost('HA')
	HB = net.addHost('HB')
	R1 = net.addHost('R1')
	R2 = net.addHost('R2')
	R3 = net.addHost('R3')
	R4 = net.addHost('R4')

	#Mendefinisikan bandwidth (/Mbps)
	bandwidth1={'bw':1}
	bandwidth2={'bw':0.5}

	bufsize = 100
	#Menghubungkan antar device
		#add link 
	net.addLink(R1, HA, max_queue_size=bufsize, intfName1 = 'R1-eth0', intfName2 = 'HA-eth0', cls=TCLink, **bandwidth1)
	net.addLink(R2, HA, max_queue_size=bufsize, intfName1 = 'R2-eth0', intfName2 = 'HA-eth1', cls=TCLink, **bandwidth1)
	net.addLink(R3, HB, max_queue_size=bufsize, intfName1 = 'R3-eth0', intfName2 = 'HB-eth0', cls=TCLink, **bandwidth1)
	net.addLink(R4, HB, max_queue_size=bufsize, intfName1 = 'R4-eth0', intfName2 = 'HB-eth1', cls=TCLink, **bandwidth1)
	net.addLink(R1, R3, max_queue_size=bufsize, intfName1 = 'R1-eth1', intfName2 = 'R3-eth1', cls=TCLink, **bandwidth2)
	net.addLink(R1, R4, max_queue_size=bufsize, intfName1 = 'R1-eth2', intfName2 = 'R4-eth1', cls=TCLink, **bandwidth1)
	net.addLink(R2, R4, max_queue_size=bufsize, intfName1 = 'R2-eth2', intfName2 = 'R4-eth2', cls=TCLink, **bandwidth2)
	net.addLink(R2, R3, max_queue_size=bufsize, intfName1 = 'R2-eth1', intfName2 = 'R3-eth2', cls=TCLink, **bandwidth1)
	net.build()

	#define NIC on each host
	HA.cmd("ifconfig HA-eth0 0")
	HA.cmd("ifconfig HA-eth1 0")
		
	HB.cmd("ifconfig HB-eth0 0")
	HB.cmd("ifconfig HB-eth1 0")
		
	R1.cmd("ifconfig R1-eth0 0")
	R1.cmd("ifconfig R1-eth1 0")
	R1.cmd("ifconfig R1-eth2 0")
		
	R2.cmd("ifconfig R2-eth0 0")
	R2.cmd("ifconfig R2-eth1 0")
	R2.cmd("ifconfig R2-eth2 0")
		
	R3.cmd("ifconfig R3-eth0 0")
	R3.cmd("ifconfig R3-eth1 0")
	R3.cmd("ifconfig R3-eth2 0")
		
	R4.cmd("ifconfig R4-eth0 0")
	R4.cmd("ifconfig R4-eth1 0")
	R4.cmd("ifconfig R4-eth2 0")
		
	R1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	R2.cmd("echo 2 > /proc/sys/net/ipv4/ip_forward")
	R3.cmd("echo 3 > /proc/sys/net/ipv4/ip_forward")
	R4.cmd("echo 4 > /proc/sys/net/ipv4/ip_forward")
		
	#inisialisasi IP Address pada Interface setiap perangkat
	HA.cmd("ifconfig HA-eth0 101.128.1.1 netmask 255.255.255.0")
	HA.cmd("ifconfig HA-eth1 101.128.2.1 netmask 255.255.255.0")
	
	HB.cmd("ifconfig HB-eth0 101.128.3.1 netmask 255.255.255.0")
	HB.cmd("ifconfig HB-eth1 101.128.4.1 netmask 255.255.255.0")
	
	R1.cmd("ifconfig R1-eth0 101.128.1.2 netmask 255.255.255.0")
	R1.cmd("ifconfig R1-eth1 101.128.5.1 netmask 255.255.255.0")
	R1.cmd("ifconfig R1-eth2 101.128.7.1 netmask 255.255.255.0")
	
	R2.cmd("ifconfig R2-eth0 101.128.2.2 netmask 255.255.255.0")
	R2.cmd("ifconfig R2-eth1 101.128.8.1 netmask 255.255.255.0")
	R2.cmd("ifconfig R2-eth2 101.128.6.1 netmask 255.255.255.0")
	
	R3.cmd("ifconfig R3-eth0 101.128.3.2 netmask 255.255.255.0")
	R3.cmd("ifconfig R3-eth1 101.128.5.2 netmask 255.255.255.0")
	R3.cmd("ifconfig R3-eth2 101.128.8.2 netmask 255.255.255.0")
	
	R4.cmd("ifconfig R4-eth0 101.128.4.2 netmask 255.255.255.0")
	R4.cmd("ifconfig R4-eth1 101.128.7.2 netmask 255.255.255.0")
	R4.cmd("ifconfig R4-eth2 101.128.6.2 netmask 255.255.255.0")
	
	#Routing setiap perangkat yang bertetangga
	HA.cmd("ip rule add from 101.128.1.1 table 1")
	HA.cmd("ip rule add from 101.128.2.1 table 2")
	
	HA.cmd("ip route add 101.128.1.0/24 dev HA-eth0 scope link table 1")
	HA.cmd("ip route add default 101.128.1.2 dev HA-eth0 table 1")
	
	HA.cmd("ip route add 101.128.2.0/24 dev HA-eth1 scope link table 2")
	HA.cmd("ip route add default via 101.128.2.2 dev HA-eth1 table 2")
	
	HA.cmd("ip route add default scope global nexthop via 101.128.1.2 dev HA-eth0")
	
	HB.cmd("ip rule add from 101.128.3.1 table 1")
	HB.cmd("ip rule add from 101.128.4.1 table 2")
	
	HB.cmd("ip route add 101.128.3.0/24 dev HB-eth0 scope link table 1")
	HB.cmd("ip route add default via 101.128.3.2 dev HB-eth0 table 1")
	
	HB.cmd("ip route add 101.128.4.0/24 dev HB-eth1 scope link table 2")
	HB.cmd("ip route add default via 101.128.4.2 dev HB-eth1 table 2")
	
	HB.cmd("ip route add default scope global nexthop via 101.128.3.2 dev HB-eth0")


	
	#Membuat routing static
	R1.cmd("route add -net 101.128.3.0/24 gw 101.128.5.2")
	R1.cmd("route add -net 101.128.4.0/24 gw 101.128.7.2")
	R1.cmd("route add -net 101.128.6.0/24 gw 101.128.7.2")
	R1.cmd("route add -net 101.128.8.0/24 gw 101.128.5.2")
	R1.cmd("route add -net 101.128.2.0/24 gw 101.128.5.2")
	
	R2.cmd("route add -net 101.128.3.0/24 gw 101.128.8.2")
	R2.cmd("route add -net 101.128.4.0/24 gw 101.128.6.2")
	R2.cmd("route add -net 101.128.5.0/24 gw 101.128.8.2")
	R2.cmd("route add -net 101.128.7.0/24 gw 101.128.6.2")
	R2.cmd("route add -net 101.128.1.0/24 gw 101.128.6.2")
	
	R3.cmd("route add -net 101.128.1.0/24 gw 101.128.5.1")
	R3.cmd("route add -net 101.128.2.0/24 gw 101.128.8.1")
	R3.cmd("route add -net 101.128.6.0/24 gw 101.128.8.1")
	R3.cmd("route add -net 101.128.7.0/24 gw 101.128.5.1")
	R3.cmd("route add -net 101.128.4.0/24 gw 101.128.5.1")
	
	R4.cmd("route add -net 101.128.1.0/24 gw 101.128.7.1")
	R4.cmd("route add -net 101.128.2.0/24 gw 101.128.6.1")
	R4.cmd("route add -net 101.128.5.0/24 gw 101.128.7.1")
	R4.cmd("route add -net 101.128.8.0/24 gw 101.128.6.1")
	R4.cmd("route add -net 101.128.3.0/24 gw 101.128.6.1")
	

	# run background traffic
	HB.cmd("iperf -s &") #Buat server
	HA.cmd("iperf -t 101.128.3.1 -t 100 &") #Buat client
	
	
	CLI(net)
	net.stop()
