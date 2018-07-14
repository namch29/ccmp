from ryu.base import app_manager
from ryu.controller import mac_to_port
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import arp
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import ipv6
from ryu.lib.packet import ether_types
from ryu.lib import mac, ip
from ryu.topology.api import get_switch, get_link
from ryu.app.wsgi import ControllerBase
from ryu.topology import event

from collections import defaultdict
from operator import itemgetter

import os
import random
import time
import ccmp_network_monitor

ten_nodes_path_file="data-10-nodes-result-paths.txt"
abilene_path_file="data-abilene-result-paths.txt"
bkup_1="backup_1.txt"

class ProjectCCMP(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    #_CONTEXTS = {"network monitor":ccmp_network_monitor.CcmpNetworkMonitor}
    def __init__(self, *args, **kwargs):
        super(ProjectCCMP, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.topology_api_app = self
        self.datapath_list = {}
        self.arp_table = {}
        self.switches = []
        self.hosts = {}
        self.multipath_group_ids = {}
        self.group_ids = []
        self.adjacency = defaultdict(dict)	#self.adjacency[s1.dpid][s2.dpid] = s1.port_no        self.adjacency[s2.dpid][s1.dpid] = s2.port_no
        self.bandwidths = defaultdict(lambda: defaultdict(lambda: DEFAULT_BW))
        self.paths = defaultdict(list)
        
        self.host_ip={	(13,19):["10.0.0.1","10.0.0.7"], (13,20):["10.0.0.1","10.0.0.8"], (13,21):["10.0.0.1","10.0.0.9"],
						(13,22):["10.0.0.1","10.0.0.10"], (13,23):["10.0.0.1","10.0.0.11"], (13,24):["10.0.0.1","10.0.0.12"], 
						
						(14,19):["10.0.0.2","10.0.0.7"], (14,20):["10.0.0.2","10.0.0.8"], (14,21):["10.0.0.2","10.0.0.9"],
						(14,22):["10.0.0.2","10.0.0.10"], (14,23):["10.0.0.2","10.0.0.11"], (14,24):["10.0.0.2","10.0.0.12"],
						
						(15,19):["10.0.0.3","10.0.0.7"], (15,20):["10.0.0.3","10.0.0.8"], (15,21):["10.0.0.3","10.0.0.9"],
						(15,22):["10.0.0.3","10.0.0.10"], (15,23):["10.0.0.3","10.0.0.11"], (15,24):["10.0.0.3","10.0.0.12"],
						
						(16,19):["10.0.0.4","10.0.0.7"], (16,20):["10.0.0.4","10.0.0.8"], (16,21):["10.0.0.4","10.0.0.9"],
						(16,22):["10.0.0.4","10.0.0.10"], (16,23):["10.0.0.4","10.0.0.11"], (16,24):["10.0.0.4","10.0.0.12"],
						
						(17,19):["10.0.0.5","10.0.0.7"], (17,20):["10.0.0.5","10.0.0.8"], (17,21):["10.0.0.5","10.0.0.9"],
						(17,22):["10.0.0.5","10.0.0.10"], (17,23):["10.0.0.5","10.0.0.11"], (17,24):["10.0.0.5","10.0.0.12"],	
						
						(18,19):["10.0.0.6","10.0.0.7"], (18,20):["10.0.0.6","10.0.0.8"], (18,21):["10.0.0.6","10.0.0.9"],
						(18,22):["10.0.0.6","10.0.0.10"], (18,23):["10.0.0.6","10.0.0.11"], (18,24):["10.0.0.6","10.0.0.12"]				
						}
       
        self.host_port={(13,19):[5,5], (13,20):[5,6],(13,21):[5,5],(13,22):[5,5],(13,23):[5,6],(13,24):[5,5],
						(14,19):[5,5], (14,20):[5,6],(14,21):[5,5],(14,22):[5,5],(14,23):[5,6],(14,24):[5,5],
						(15,19):[6,5], (15,20):[6,6],(15,21):[6,5],(15,22):[6,5],(15,23):[6,6],(15,24):[6,5],
						(16,19):[5,5], (16,20):[5,6],(16,21):[5,5],(16,22):[5,5],(16,23):[5,6],(16,24):[5,5],
						(17,19):[5,5], (17,20):[5,6],(17,21):[5,5],(17,22):[5,5],(17,23):[5,6],(17,24):[5,5],
						(18,19):[5,5], (18,20):[5,6],(18,21):[5,5],(18,22):[5,5],(18,23):[5,6],(18,24):[5,5]}
        
        
        #h1-eth0<->s13-eth5 (OK OK) 
		#h2-eth0<->s14-eth5 (OK OK) 
		#h3-eth0<->s15-eth6 (OK OK) 
		#h4-eth0<->s16-eth5 (OK OK) 
		#h5-eth0<->s17-eth5 (OK OK) 
		#h6-eth0<->s18-eth5 (OK OK) 
		#h7-eth0<->s19-eth5 (OK OK) 
		#h8-eth0<->s20-eth6 (OK OK) 
		#h9-eth0<->s21-eth5 (OK OK) 
		#h10-eth0<->s22-eth5 (OK OK) 
		#h11-eth0<->s23-eth6 (OK OK) 
		#h12-eth0<->s24-eth5 (OK OK) 	
        
        
        self.count=0
        self.isInstallFlows = False
        self.isReInstallFlows = False

    def get_paths(self, filePath):
		'''
		Get all paths from text file    
		'''
		try:		
			fo = open(filePath, "r")
			paths = defaultdict(list)
			number_of_flow = int(fo.readline())
			print "Number of demand: %s" % (number_of_flow)
			
			for i in xrange(0,number_of_flow):
				key_s = fo.readline().split()
				key = [(int(x)+1) for x in key_s]
							
				number_of_path = int(fo.readline())
				#print "Flow from %s" %(key_s[0]),"to %s" %(key_s[1])
				
				paths [key[0],key[1]]=[]
				for n in xrange(0,number_of_path):
					tmp = fo.readline().split(" ")
					del tmp[-1]
					del tmp [1]
					path = [(int(x) +1) for x in tmp[1:]]
					path.insert(0,tmp[0])
					#print path
					paths [key[0],key[1]].append(path)	
				#print "Available paths from ", key[0], " to ", key[1], " : ", paths.get((key[0],key[1]))
				
		except IOError:
			print "Error: could not find file or read data"
		else:	
			fo.close()
		return paths
		#print paths.get((src,dst))

    def add_ports_to_paths(self, paths, first_port, last_port):
        '''
        Add the ports that connects the switches for all paths
        '''
        paths_p = []
        print "paths:", paths, "first port:", first_port, "last port: ",last_port
        print "add_ports_to_paths------Adjacency:", self.adjacency
        #raw_input("Press Enter to continue...")
        for path in paths:
            p = {}
            print path
            in_port = first_port
            for s1, s2 in zip(path[:-1], path[1:]):
                out_port = self.adjacency[s1][s2]
                p[s1] = (in_port, out_port)
                in_port = self.adjacency[s2][s1]
            p[path[-1]] = (in_port, last_port)
            paths_p.append(p)
        
        return paths_p

    def generate_openflow_gid(self):
        '''
        Returns a random OpenFlow group id
        '''
        n = random.randint(0, 2**32)
        while n in self.group_ids:
            n = random.randint(0, 2**32)
        return n


    def install_paths(self, src, first_port, dst, last_port, ip_src, ip_dst, rev=False):
        
        computation_start = time.time()
        paths_weight = []
        
        try:
	        if rev == False:
				paths_weight = self.paths.get((src,dst))
				print "Lenght of paths_weght:", len(paths_weight)
	        
	        elif rev == True:
				print "!!!!!!!!!REVERSE PATH!!!!!!!!!!!!"
				paths_weight_r = self.paths.get((dst,src))
				for path_r in paths_weight_r:
					tmp =path_r[::-1]
					tmp.insert(0,tmp[len(tmp)-1])
					del tmp[len(tmp)-1]
					paths_weight.append(tmp)
				print "Lenght of paths_weght:", len(paths_weight)
	        
        except:
			print "\n***************"
			print "paths_weight:\t", paths_weight
			print "RETURNING................\n"
			return
        	
        pw=[]	#port weight
        paths=[]
                
        for i in xrange(0,len(paths_weight)):
			pw.append(float(paths_weight[i][0]))
			paths.append([int(x) for x in paths_weight[i][1:]])  
        
        print "Available paths from ", src, " to ", dst, " : "
        print "weight=",pw,"paths:",paths
        
        paths_with_ports = self.add_ports_to_paths(paths, first_port, last_port)
        
        print "paths with port", paths_with_ports
        
        switches_in_paths = set().union(*paths) 	#list of switches in all path
        print "swithes in paths",switches_in_paths
        
        for node in switches_in_paths:

            dp = self.datapath_list[node]
            ofp = dp.ofproto
            ofp_parser = dp.ofproto_parser

            ports = defaultdict(list)
            actions = []
            i = 0

            for path in paths_with_ports:
                if node in path:
				in_port = path[node][0]
				out_port = path[node][1]
				
				if len(ports[in_port])==0:
					ports[in_port].append((out_port, pw[i]))
				
				else:
					out_port_list=[]
					wght = []
					for (op,w) in ports[in_port]:
						out_port_list.append(op)
						wght.append(w)
					
					if out_port not in out_port_list:
						ports[in_port].append((out_port, pw[i]))
					
					else:
						index = out_port_list.index(out_port)
						new_weight = pw[i]+wght[index]
						del ports[in_port][index]
						ports[in_port].insert(index,(out_port,new_weight))
                i += 1
            for in_port in ports:

                match_ip = ofp_parser.OFPMatch(
                    eth_type=0x0800, 
                    ipv4_src=ip_src, 
                    ipv4_dst=ip_dst
                )
                match_arp = ofp_parser.OFPMatch(
                    eth_type=0x0806, 
                    arp_spa=ip_src, 
                    arp_tpa=ip_dst
                )

                out_ports = ports[in_port]
                print "node:",node," outport:", out_ports

                if len(out_ports) > 1:
                    group_id = None
                    group_new = False

                    if (node, src, dst) not in self.multipath_group_ids:
                        group_new = True
                        self.multipath_group_ids[
                            node, src, dst] = self.generate_openflow_gid()
                    group_id = self.multipath_group_ids[node, src, dst]
                    print group_id

                    buckets = []
                    # print "node at ",node," out ports : ",out_ports
                    for port, weight in out_ports:
                        bucket_weight = int(round(weight * 100))
                        bucket_action = [ofp_parser.OFPActionOutput(port)]
                        buckets.append(
                            ofp_parser.OFPBucket(
                                weight=bucket_weight,
                                watch_port=port,
                                watch_group=ofp.OFPG_ANY,
                                actions=bucket_action
                            )
                        )

                    if group_new:
                        req = ofp_parser.OFPGroupMod(
                            dp, ofp.OFPGC_ADD, ofp.OFPGT_SELECT, group_id,
                            buckets
                        )
                        dp.send_msg(req)
                    else:
                        req = ofp_parser.OFPGroupMod(
                            dp, ofp.OFPGC_MODIFY, ofp.OFPGT_SELECT,
                            group_id, buckets)
                        dp.send_msg(req)

                    actions = [ofp_parser.OFPActionGroup(group_id)]

                    self.add_flow(dp, 32768, match_ip, actions)
                    self.add_flow(dp, 1, match_arp, actions)

                elif len(out_ports) == 1:
                    actions = [ofp_parser.OFPActionOutput(out_ports[0][0])]

                    self.add_flow(dp, 32768, match_ip, actions)
                    self.add_flow(dp, 1, match_arp, actions)
        
        print "Path installation finished in ", time.time() - computation_start 
        print "==============================\n"
        #return paths_with_ports[0][src][1]

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        # print "Adding flow ", match, actions
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    def install_flows(self, path_file):
		self.paths = self.get_paths (path_file)
			
		for k,v in self.paths:
			#print k, self.host_port[(k,v)][0], v, self.host_port[(k,v)][1], self.host_ip[(k,v)][0], self.host_ip[(k,v)][1]
			src = k
			first_port = self.host_port[(k,v)][0]
			dst = v
			last_port = self.host_port[(k,v)][1] 
			ip_src =  self.host_ip[(k,v)][0]
			ip_dst = self.host_ip[(k,v)][1]
			#print self.paths[(k,v)]
			self.install_paths(src, first_port, dst, last_port, ip_src, ip_dst)
			self.install_paths(dst, last_port, src, first_port, ip_dst, ip_src, rev=True)
		print "All Flows were installed"
    
    def del_all_flow(self, datapath):
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		empty_match = parser.OFPMatch()
		mod = parser.OFPFlowMod(datapath=datapath,
                                command=ofproto.OFPFC_DELETE,
                                out_port=ofproto.OFPP_ANY,
                                out_group=ofproto.OFPG_ANY,
                                match=empty_match)
		datapath.send_msg(mod)
        
        
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        #print "Openflow protocol",ofproto
        parser = datapath.ofproto_parser
        

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        print "!!Tabble-miss Flow INSTALLED!!"
        

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
		#print self.isInstallFlows
		if (self.isInstallFlows==False):
			msg = ev.msg
			datapath = msg.datapath
			ofproto = datapath.ofproto
			parser = datapath.ofproto_parser
			in_port = msg.match['in_port']
	
			pkt = packet.Packet(msg.data)
			eth = pkt.get_protocol(ethernet.ethernet)
			arp_pkt = pkt.get_protocol(arp.arp)
	
	        # avoid broadcast from LLDP
			if eth.ethertype == ether_types.ETH_TYPE_LLDP:
				return
	
			if pkt.get_protocol(ipv6.ipv6):  # Drop the IPV6 Packets.
				match = parser.OFPMatch(eth_type=eth.ethertype)
				actions = []
				self.add_flow(datapath, 1, match, actions)
				return None
			self.isInstallFlows = True    
			if(arp_pkt):
				print "INSTALLING FLOWS>>>>>>>>"
				print self.isInstallFlows
				self.install_flows(abilene_path_file)
		else:
			pass
    
    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, ev):
        switch = ev.switch.dp
        ofp_parser = switch.ofproto_parser

        if switch.id not in self.switches:
            self.switches.append(switch.id)
            self.datapath_list[switch.id] = switch
            
    @set_ev_cls(event.EventSwitchLeave, MAIN_DISPATCHER)
    def switch_leave_handler(self, ev):
        print ev
        switch = ev.switch.dp.id
        
        if switch in self.switches:
            self.switches.remove(switch)
            del self.datapath_list[switch]
            del self.adjacency[switch]
        #self.reset_data()

    @set_ev_cls(event.EventLinkAdd, MAIN_DISPATCHER)
    def link_add_handler(self, ev):
        s1 = ev.link.src
        s2 = ev.link.dst
        #print "switch", s1.dpid, "port:",s1.port_no
        #print "switch", s2.dpid, "port:",s2.port_no
        self.adjacency[s1.dpid][s2.dpid] = s1.port_no
        self.adjacency[s2.dpid][s1.dpid] = s2.port_no
        #self.count+=1
        #print self.count
        #if self.count==46:
			#if self.isInstallFlows==False:
				#self.isInstallFlows ==True
				#self.install_flows(path_file)
				
        
    @set_ev_cls(event.EventLinkDelete, MAIN_DISPATCHER)
    def link_delete_handler(self, ev):
        
        s1 = ev.link.src
        s2 = ev.link.dst
        # Exception handling if switch already deleted
        #print "link is removed: s1",s1, "s2:", s2
        try:
            del self.adjacency[s1.dpid][s2.dpid]
            del self.adjacency[s2.dpid][s1.dpid]
        except KeyError:
            pass
        
        if self.isReInstallFlows==False:
			self.isReInstallFlows =True
			#for k in self.datapath_list:
				#self.del_all_flow(self.datapath_list [k])
			print "\n.............................Backup flows were insalling..................\n"
			#self.install_flows(bkup_1)
			print "================ Backup flows were installed!! =============================\n"
	
	
	
        
		
