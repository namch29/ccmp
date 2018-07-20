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


class tenNodesTopo(Topo):

    "Abilene Topology"

    def __init__(self):
		"Create Abilene Topology"

		Topo.__init__(self)

		#info( '*** Add hosts\n') 
		h1 = self.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
		h2 = self.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
		h3 = self.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
		h4 = self.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
		h5 = self.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
		h6 = self.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
		h7 = self.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
		h8 = self.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
		h9 = self.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
		h10 = self.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)
		h11 = self.addHost('h11', cls=Host, ip='10.0.0.11', defaultRoute=None)
		h12 = self.addHost('h12', cls=Host, ip='10.0.0.12', defaultRoute=None)
	    
		#info( '*** Add switches\n')
		
		s1 = self.addSwitch('s1', 	cls=OVSKernelSwitch)
		s2 = self.addSwitch('s2', 	cls=OVSKernelSwitch)
		s3 = self.addSwitch('s3', 	cls=OVSKernelSwitch)
		s4 = self.addSwitch('s4', 	cls=OVSKernelSwitch)
		s5 = self.addSwitch('s5', 	cls=OVSKernelSwitch)
		s6 = self.addSwitch('s6', 	cls=OVSKernelSwitch)
		s7 = self.addSwitch('s7', 	cls=OVSKernelSwitch)
		s8 = self.addSwitch('s8', 	cls=OVSKernelSwitch)
		s9 = self.addSwitch('s9', 	cls=OVSKernelSwitch)
		s10 = self.addSwitch('s10', cls=OVSKernelSwitch)
		s11 = self.addSwitch('s11', cls=OVSKernelSwitch)
		s12 = self.addSwitch('s12', cls=OVSKernelSwitch)
		
		s13 = self.addSwitch('s13', cls=OVSKernelSwitch)
		s14 = self.addSwitch('s14', cls=OVSKernelSwitch)
		s15 = self.addSwitch('s15', cls=OVSKernelSwitch)
		s16 = self.addSwitch('s16', cls=OVSKernelSwitch)
		s17 = self.addSwitch('s17', cls=OVSKernelSwitch)
		s18 = self.addSwitch('s18', cls=OVSKernelSwitch)
		s19 = self.addSwitch('s19', cls=OVSKernelSwitch)
		s20 = self.addSwitch('s20', cls=OVSKernelSwitch)
		s21 = self.addSwitch('s21', cls=OVSKernelSwitch)
		s22 = self.addSwitch('s22', cls=OVSKernelSwitch)
		s23 = self.addSwitch('s23', cls=OVSKernelSwitch)
		s24 = self.addSwitch('s24', cls=OVSKernelSwitch)
	
		
	
		#info( '*** Add links\n')
		#core links
		coreBW = 992
		self.addLink(s1, s2, 	cls=TCLink, bw=coreBW)
		
		self.addLink(s2, s5, 	cls=TCLink, bw=coreBW)
		self.addLink(s2, s6, 	cls=TCLink, bw=coreBW)
		self.addLink(s2, s12, 	cls=TCLink, bw=coreBW)
		
		self.addLink(s3, s6, 	cls=TCLink, bw=coreBW)
		self.addLink(s3, s9, 	cls=TCLink, bw=coreBW)
		
		self.addLink(s4, s7, 	cls=TCLink, bw=coreBW)
		self.addLink(s4, s10, 	cls=TCLink, bw=coreBW)
		self.addLink(s4, s11, 	cls=TCLink, bw=coreBW)
		
		self.addLink(s5, s7, 	cls=TCLink, bw=coreBW)
		self.addLink(s5, s8, 	cls=TCLink, bw=coreBW)
		
		self.addLink(s6, s7, 	cls=TCLink, bw=coreBW)
		
		self.addLink(s8, s10, 	cls=TCLink, bw=coreBW)
		
		self.addLink(s9, s12, 	cls=TCLink, bw=coreBW)
		
		self.addLink(s10, s11, 	cls=TCLink, bw=coreBW)
		
	
		
		#edge links
		edgeBW = 992
		self.addLink(s13, s1, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s14, s2, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s15, s3, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s16, s4, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s17, s5, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s18, s6, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s7, s19, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s8, s20, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s9, s21, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s10, s22, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s11, s23, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s12, s24, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s13, s3, 	cls=TCLink, bw=edgeBW)
		self.addLink(s13, s4, 	cls=TCLink, bw=edgeBW)
		self.addLink(s13, s5, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s14, s4, 	cls=TCLink, bw=edgeBW)
		self.addLink(s14, s5, 	cls=TCLink, bw=edgeBW)
		self.addLink(s14, s6, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s15, s1, 	cls=TCLink, bw=edgeBW)
		self.addLink(s15, s2, 	cls=TCLink, bw=edgeBW)
		self.addLink(s15, s5, 	cls=TCLink, bw=edgeBW)
		self.addLink(s15, s6, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s16, s1, 	cls=TCLink, bw=edgeBW)
		self.addLink(s16, s2, 	cls=TCLink, bw=edgeBW)
		self.addLink(s16, s3, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s17, s2, 	cls=TCLink, bw=edgeBW)
		self.addLink(s17, s3, 	cls=TCLink, bw=edgeBW)	
		self.addLink(s17, s4, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s18, s3, 	cls=TCLink, bw=edgeBW)
		self.addLink(s18, s4, 	cls=TCLink, bw=edgeBW)
		self.addLink(s18, s5, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s8, s19, 	cls=TCLink, bw=edgeBW)
		self.addLink(s9, s19, 	cls=TCLink, bw=edgeBW)
		self.addLink(s10, s19, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s9, s20, 	cls=TCLink, bw=edgeBW)
		self.addLink(s10, s20, 	cls=TCLink, bw=edgeBW)
		self.addLink(s11, s20, 	cls=TCLink, bw=edgeBW)
		self.addLink(s7, s20, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s10, s21, 	cls=TCLink, bw=edgeBW)
		self.addLink(s11, s21, 	cls=TCLink, bw=edgeBW)
		self.addLink(s12, s21, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s7, s22, 	cls=TCLink, bw=edgeBW)
		self.addLink(s8, s22, 	cls=TCLink, bw=edgeBW)
		self.addLink(s9, s22, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s8, s23, 	cls=TCLink, bw=edgeBW)
		self.addLink(s9, s23, 	cls=TCLink, bw=edgeBW)
		self.addLink(s10, s23, 	cls=TCLink, bw=edgeBW)
		self.addLink(s12, s23, 	cls=TCLink, bw=edgeBW)
		
		self.addLink(s7, s24, 	cls=TCLink, bw=edgeBW)
		self.addLink(s8, s24, 	cls=TCLink, bw=edgeBW)
		self.addLink(s11, s24, 	cls=TCLink, bw=edgeBW)
		
		
	    #12	18	
		#12	19	
		#12	20	
		#12	21	
		#12	22	
		#12	23
			
		#13	18	
		#13	19	
		#13	20	
		#13	21	
		#13	22	
		#13	23
			
		#14	18	
		#14	19	
		#14	20	
		#14	21	
		#14	22	
		#14	23	
		
		#15	18	
		#15	19	
		#15	20	
		#15	21	
		#15	22	
		#15	23	
		
		#16	18	
		#16	19	
		#16	20	
		#16	21	
		#16	22	
		#16	23	
		
		#17	18	
		#17	19	
		#17	20	
		#17	21	
		#17	22	
		#17	23	
		
		inputBW = 992
		self.addLink(h1, s13, 	cls=TCLink, bw=inputBW)
		self.addLink(h2, s14, 	cls=TCLink, bw=inputBW)
		self.addLink(h3, s15, 	cls=TCLink, bw=inputBW)
		self.addLink(h4, s16, 	cls=TCLink, bw=inputBW)
		self.addLink(h5, s17, 	cls=TCLink, bw=inputBW)
		self.addLink(h6, s18, 	cls=TCLink, bw=inputBW)
		
		self.addLink(h7, s19, 	cls=TCLink, bw=inputBW)
		self.addLink(h8, s20, 	cls=TCLink, bw=inputBW)
		self.addLink(h9, s21, 	cls=TCLink, bw=inputBW)
		self.addLink(h10, s22, 	cls=TCLink, bw=inputBW)
		self.addLink(h11, s23, 	cls=TCLink, bw=inputBW)
		self.addLink(h12, s24, 	cls=TCLink, bw=inputBW)
        
topos = { 'abilene': (lambda: tenNodesTopo() ) }
