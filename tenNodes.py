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
                      ip='192.168.15.107',
                      protocol='tcp',
                      port=6633)
	
	
	#Add hosts
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    
    info( '*** Add switches\n')
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')

    info( '*** Add links\n')
    #core links
    s1s2 = {'bw':100}
    net.addLink(s1, s2, cls=TCLink , **s1s2)
    s1s3 = {'bw':100}
    net.addLink(s1, s3, cls=TCLink , **s1s3)
    s1s4 = {'bw':100}
    net.addLink(s1, s4, cls=TCLink , **s1s4)
    s2s3 = {'bw':100}
    net.addLink(s2, s3, cls=TCLink , **s2s3)
    s2s4 = {'bw':100}
    net.addLink(s2, s4, cls=TCLink , **s2s4)
    s3s4 = {'bw':100}
    net.addLink(s3, s4, cls=TCLink , **s3s4)
    s3s5 = {'bw':100}
    net.addLink(s3, s5, cls=TCLink , **s3s5)
    s3s6 = {'bw':100}
    net.addLink(s3, s6, cls=TCLink , **s3s6)
    s4s5 = {'bw':100}
    net.addLink(s4, s5, cls=TCLink , **s4s5)
    s4s6 = {'bw':100}
    net.addLink(s4, s6, cls=TCLink , **s4s6)
    s5s6 = {'bw':100}
    net.addLink(s5, s6, cls=TCLink , **s5s6)
    
    #edge links
    s7s1 = {'bw':200}
    net.addLink(s7, s1, cls=TCLink , **s7s1)
    s7s5 = {'bw':200}
    net.addLink(s7, s5, cls=TCLink , **s7s5)
    s7s3 = {'bw':200}
    net.addLink(s7, s3, cls=TCLink , **s7s3)
    s8s1 = {'bw':200}
    net.addLink(s8, s1, cls=TCLink , **s8s1)
    s8s3 = {'bw':200}
    net.addLink(s8, s3, cls=TCLink , **s8s3)
    s8s5 = {'bw':200}
    net.addLink(s8, s5, cls=TCLink , **s8s5)
    s9s2 = {'bw':200}
    net.addLink(s9, s2, cls=TCLink , **s9s2)
    s10s2 = {'bw':200}
    net.addLink(s10, s2, cls=TCLink , **s10s2)
    s4s10 = {'bw':200}
    net.addLink(s4, s10, cls=TCLink , **s4s10)
    s4s9 = {'bw':200}
    net.addLink(s4, s9, cls=TCLink , **s4s9)
    s9s6 = {'bw':200}
    net.addLink(s9, s6, cls=TCLink , **s9s6)
    s10s6 = {'bw':200}
    net.addLink(s10, s6, cls=TCLink , **s10s6)

    #7-->9: 	h1,h2--> h5,h6
    #7-->10:	h1,h2--> h7,h8
    #8-->9:		h3,h4--> h5,h6
	#8-->10:	h3,h4--> h7,h8
	
    h1s7 = {'bw':1000}
    net.addLink(h1, s7, cls=TCLink , **h1s7)
    h2s7 = {'bw':1000}
    net.addLink(h2, s7, cls=TCLink , **h2s7)
    
    h3s8 = {'bw':1000}
    net.addLink(h3, s8, cls=TCLink , **h3s8)
    h4s8 = {'bw':1000}
    net.addLink(h4, s8, cls=TCLink , **h4s8)
    
    h5s9 = {'bw':1000}
    net.addLink(h5, s9, cls=TCLink , **h5s9)
    h6s9 = {'bw':1000}
    net.addLink(h6, s9, cls=TCLink , **h6s9)
    
    h7s10 = {'bw':1000}
    net.addLink(h7, s10, cls=TCLink , **h7s10)
    h8s10 = {'bw':1000}
    net.addLink(h8, s10, cls=TCLink , **h8s10)

     
    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s7').start([c0])
    net.get('s2').start([c0])
    net.get('s4').start([c0])
    net.get('s9').start([c0])
    net.get('s6').start([c0])
    net.get('s1').start([c0])
    net.get('s8').start([c0])
    net.get('s10').start([c0])
    net.get('s3').start([c0])
    net.get('s5').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

