#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.topo import Topo


def myNetwork():
	
   	info('*** Abilene Topology\n')
   	net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')
	
	info( '*** Adding controller\n' )
	c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)
    
	#c0=net.addController(name='c0',
                      #controller=Controller,
                      #ip='127.0.0.1',
                      #protocol='tcp',
                      #port=6633)
    #info( '*** Add hosts\n') 
	h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
	h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
	h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
	h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
	h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
	h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
	
	h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
	h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
	h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
	h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)
	h11 = net.addHost('h11', cls=Host, ip='10.0.0.11', defaultRoute=None)
	h12 = net.addHost('h12', cls=Host, ip='10.0.0.12', defaultRoute=None)
	
	#info( '*** Add switches\n')
	s1 = net.addSwitch('s1', 	cls=OVSKernelSwitch)
	s2 = net.addSwitch('s2', 	cls=OVSKernelSwitch)
	s3 = net.addSwitch('s3', 	cls=OVSKernelSwitch)
	s4 = net.addSwitch('s4', 	cls=OVSKernelSwitch)
	s5 = net.addSwitch('s5', 	cls=OVSKernelSwitch)
	s6 = net.addSwitch('s6', 	cls=OVSKernelSwitch)
	s7 = net.addSwitch('s7', 	cls=OVSKernelSwitch)
	s8 = net.addSwitch('s8', 	cls=OVSKernelSwitch)
	s9 = net.addSwitch('s9', 	cls=OVSKernelSwitch)
	s10 = net.addSwitch('s10', cls=OVSKernelSwitch)
	s11 = net.addSwitch('s11', cls=OVSKernelSwitch)
	s12 = net.addSwitch('s12', cls=OVSKernelSwitch)
	
	s13 = net.addSwitch('s13', cls=OVSKernelSwitch)
	s14 = net.addSwitch('s14', cls=OVSKernelSwitch)
	s15 = net.addSwitch('s15', cls=OVSKernelSwitch)
	s16 = net.addSwitch('s16', cls=OVSKernelSwitch)
	s17 = net.addSwitch('s17', cls=OVSKernelSwitch)
	s18 = net.addSwitch('s18', cls=OVSKernelSwitch)
	s19 = net.addSwitch('s19', cls=OVSKernelSwitch)
	s20 = net.addSwitch('s20', cls=OVSKernelSwitch)
	s21 = net.addSwitch('s21', cls=OVSKernelSwitch)
	s22 = net.addSwitch('s22', cls=OVSKernelSwitch)
	s23 = net.addSwitch('s23', cls=OVSKernelSwitch)
	s24 = net.addSwitch('s24', cls=OVSKernelSwitch)
	
	
	
	#info( '*** Add links\n')
	#core links
	coreBW = 992
	net.addLink(s1, s2, 	cls=TCLink, bw=coreBW)
	
	net.addLink(s2, s5, 	cls=TCLink, bw=coreBW)
	net.addLink(s2, s6, 	cls=TCLink, bw=coreBW)
	net.addLink(s2, s12, 	cls=TCLink, bw=coreBW)
	
	net.addLink(s3, s6, 	cls=TCLink, bw=coreBW)
	net.addLink(s3, s9, 	cls=TCLink, bw=coreBW)
	
	net.addLink(s4, s7, 	cls=TCLink, bw=coreBW)
	net.addLink(s4, s10, 	cls=TCLink, bw=coreBW)
	net.addLink(s4, s11, 	cls=TCLink, bw=coreBW)
	
	net.addLink(s5, s7, 	cls=TCLink, bw=coreBW)
	net.addLink(s5, s8, 	cls=TCLink, bw=coreBW)
	
	net.addLink(s6, s7, 	cls=TCLink, bw=coreBW)
	
	net.addLink(s8, s10, 	cls=TCLink, bw=coreBW)
	
	net.addLink(s9, s12, 	cls=TCLink, bw=coreBW)
	
	net.addLink(s10, s11, 	cls=TCLink, bw=coreBW)
	
	
	
	#edge links
	edgeBW = 992
	net.addLink(s13, s1, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s14, s2, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s15, s3, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s16, s4, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s17, s5, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s18, s6, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s7, s19, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s8, s20, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s9, s21, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s10, s22, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s11, s23, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s12, s24, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s13, s3, 	cls=TCLink, bw=edgeBW)
	net.addLink(s13, s4, 	cls=TCLink, bw=edgeBW)
	net.addLink(s13, s5, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s14, s4, 	cls=TCLink, bw=edgeBW)
	net.addLink(s14, s5, 	cls=TCLink, bw=edgeBW)
	net.addLink(s14, s6, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s15, s1, 	cls=TCLink, bw=edgeBW)
	net.addLink(s15, s2, 	cls=TCLink, bw=edgeBW)
	net.addLink(s15, s5, 	cls=TCLink, bw=edgeBW)
	net.addLink(s15, s6, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s16, s1, 	cls=TCLink, bw=edgeBW)
	net.addLink(s16, s2, 	cls=TCLink, bw=edgeBW)
	net.addLink(s16, s3, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s17, s2, 	cls=TCLink, bw=edgeBW)
	net.addLink(s17, s3, 	cls=TCLink, bw=edgeBW)	
	net.addLink(s17, s4, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s18, s3, 	cls=TCLink, bw=edgeBW)
	net.addLink(s18, s4, 	cls=TCLink, bw=edgeBW)
	net.addLink(s18, s5, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s8, s19, 	cls=TCLink, bw=edgeBW)
	net.addLink(s9, s19, 	cls=TCLink, bw=edgeBW)
	net.addLink(s10, s19, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s9, s20, 	cls=TCLink, bw=edgeBW)
	net.addLink(s10, s20, 	cls=TCLink, bw=edgeBW)
	net.addLink(s11, s20, 	cls=TCLink, bw=edgeBW)
	net.addLink(s7, s20, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s10, s21, 	cls=TCLink, bw=edgeBW)
	net.addLink(s11, s21, 	cls=TCLink, bw=edgeBW)
	net.addLink(s12, s21, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s7, s22, 	cls=TCLink, bw=edgeBW)
	net.addLink(s8, s22, 	cls=TCLink, bw=edgeBW)
	net.addLink(s9, s22, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s8, s23, 	cls=TCLink, bw=edgeBW)
	net.addLink(s9, s23, 	cls=TCLink, bw=edgeBW)
	net.addLink(s10, s23, 	cls=TCLink, bw=edgeBW)
	net.addLink(s12, s23, 	cls=TCLink, bw=edgeBW)
	
	net.addLink(s7, s24, 	cls=TCLink, bw=edgeBW)
	net.addLink(s8, s24, 	cls=TCLink, bw=edgeBW)
	net.addLink(s11, s24, 	cls=TCLink, bw=edgeBW)
	
	
	#12	18	h1-->h7
	#13	19	h1-->h8
	#14	20	h1-->h9
	#15	21	h1-->h10
	#16	22	h1-->h11
	#17	23	h1-->h12
	
	net.addLink(h1, s13)
	net.addLink(h2, s14)
	net.addLink(h3, s15)
	net.addLink(h4, s16)
	net.addLink(h5, s17)
	net.addLink(h6, s18)
	
	net.addLink(h7, s19)
	net.addLink(h8, s20)
	net.addLink(h9, s21)
	net.addLink(h10, s22)
	net.addLink(h11, s23)
	net.addLink(h12, s24)
	
	info( '*** Starting network\n')
	net.build()
	info( '*** Starting controllers\n')
	for controller in net.controllers:
		controller.start()

	info( '*** Starting switches\n')
	net.get('s1').start([c0])
	net.get('s2').start([c0])
	net.get('s3').start([c0])
	net.get('s4').start([c0])
	net.get('s5').start([c0])
	net.get('s6').start([c0])
	net.get('s7').start([c0])
	net.get('s8').start([c0])
	net.get('s9').start([c0])
	net.get('s10').start([c0])
	net.get('s11').start([c0])
	net.get('s12').start([c0])
	net.get('s13').start([c0])
	net.get('s14').start([c0])
	net.get('s15').start([c0])
	net.get('s16').start([c0])
	net.get('s17').start([c0])
	net.get('s18').start([c0])
	net.get('s19').start([c0])
	net.get('s20').start([c0])
	net.get('s21').start([c0])
	net.get('s22').start([c0])
	net.get('s23').start([c0])
	net.get('s24').start([c0])

	info( '*** Post configure switches and hosts\n')

	CLI(net)
	net.stop()
    
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
