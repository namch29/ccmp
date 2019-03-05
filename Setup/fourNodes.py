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

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)
	
	
	#Add hosts
    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', mac ='0A:00:00:02:00:00',defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', mac ='0A:00:01:02:00:00', defaultRoute=None)
    
    #Add switches
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)


    info( '*** Add links\n')
    edge_bw=80
    core_bw = 30
    net.addLink(s1, h1, cls=TCLink , bw=edge_bw)
    net.addLink(s1, s2, cls=TCLink , bw=core_bw)
    net.addLink(s1, s3, cls=TCLink , bw=core_bw)
    net.addLink(s2, s4, cls=TCLink , bw=core_bw)
    net.addLink(s3, s4, cls=TCLink , bw=core_bw)
    net.addLink(s4, h2, cls=TCLink , bw=edge_bw)
     
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
    
    info( '*** Post configure switches and hosts\n')

    # Add arp cache entries for hosts
    h1.cmd( 'arp -s 10.0.0.2 0A:00:01:02:00:00 -i h1-eth0' )
    h2.cmd( 'arp -s 10.0.0.1 0A:00:00:02:00:00 -i h2-eth0' )
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

