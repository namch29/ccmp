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

# Cisco Reference bandwidth = 1 Gbps
REFERENCE_BW = 10000000

DEFAULT_BW = 10000000

MAX_PATHS = 2

read_file_path="data-10-nodes-result-paths.txt"

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

    def get_paths(self, filePath, src, dst):
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
		return paths.get((src,dst))
		print paths.get((src,dst))

    def add_ports_to_paths(self, paths, first_port, last_port):
        '''
        Add the ports that connects the switches for all paths
        '''
        paths_p = []
        print "paths:", paths, "first port:", first_port, "last port: ",last_port
        print self.adjacency
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
        
        if rev == False:
			paths_weight = self.get_paths(read_file_path, src, dst)
        
        else:
			paths_weight_r = self.get_paths(read_file_path, dst,src)
			paths_weight =[]
			for path_r in paths_weight_r:
				tmp =path_r[::-1]
				tmp.insert(0,tmp[len(tmp)-1])
				del tmp[len(tmp)-1]
				paths_weight.append(tmp)
				
        
        pw=[]	#port weight
        paths=[]
        
        
        for i in xrange(0,len(paths_weight)):
			pw.append(float(paths_weight[i][0]))
			paths.append([int(x) for x in paths_weight[i][1:]])  
        
        print "Available paths from ", src, " to ", dst, " : "
        print "weight=",pw,"paths:",paths
        #print len (flows)

        #pw = []
        #for path in paths:
            #pw.append(self.get_path_cost(path))
            #print path, "cost = ", pw[len(pw) - 1]
        #sum_of_pw = sum(pw) * 1.0
        
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
                print " node:",node," outport:", out_ports
                 

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
        return paths_with_ports[0][src][1]

		
    
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

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        print "switch_features_handler is called"
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        #print "Openflow protocol",ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        
        
    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, MAIN_DISPATCHER)
    def port_desc_stats_reply_handler(self, ev):
        switch = ev.msg.datapath
        for p in ev.msg.body:
            self.bandwidths[switch.id][p.port_no] = p.curr_speed

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        arp_pkt = pkt.get_protocol(arp.arp)

        # avoid broadcast from LLDP
        if eth.ethertype == 35020:
            return

        if pkt.get_protocol(ipv6.ipv6):  # Drop the IPV6 Packets.
            match = parser.OFPMatch(eth_type=eth.ethertype)
            actions = []
            self.add_flow(datapath, 1, match, actions)
            return None

        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        print "PACKET-IN"
        #for k,v in self.adjacency.iteritems():
			#print "key:",k,"value:",v
     

        if src not in self.hosts:
            self.hosts[src] = (dpid, in_port)

        
        out_port = ofproto.OFPP_FLOOD

        if arp_pkt:
            # print dpid, pkt
            src_ip = arp_pkt.src_ip
            dst_ip = arp_pkt.dst_ip
            if arp_pkt.opcode == arp.ARP_REPLY:
                print "ARP_REPLY"
                self.arp_table[src_ip] = src
                h1 = self.hosts[src]
                h2 = self.hosts[dst]
                print h1[0]
                print h2[0]
                out_port = self.install_paths(h1[0], h1[1], h2[0], h2[1], dst_ip, src_ip, rev = True) # CONTINUE HERE: need  install reverse path
                self.install_paths(h2[0], h2[1], h1[0], h1[1], src_ip, dst_ip) # reverse
            elif arp_pkt.opcode == arp.ARP_REQUEST:
                print "ARP_REQUEST"
                
                if dst_ip in self.arp_table:
                    self.arp_table[src_ip] = src
                    dst_mac = self.arp_table[dst_ip]
                    h1 = self.hosts[src]
                    h2 = self.hosts[dst_mac]
                    print h1[0]
                    print h2[0]
                    #paths = self.get_paths(read_file_path, h1[0], h2[0])
                    #print paths
                    out_port = self.install_paths(h1[0], h1[1], h2[0], h2[1], src_ip, dst_ip)
                    self.install_paths(h2[0], h2[1], h1[0], h1[1], dst_ip, src_ip,rev = True) # reverse

        # print pkt

        actions = [parser.OFPActionOutput(out_port)]

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,
            actions=actions, data=data)
        datapath.send_msg(out)

    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, ev):
        switch = ev.switch.dp
        ofp_parser = switch.ofproto_parser

        if switch.id not in self.switches:
            self.switches.append(switch.id)
            self.datapath_list[switch.id] = switch

            # Request port/link descriptions, useful for obtaining bandwidth
            req = ofp_parser.OFPPortDescStatsRequest(switch)
            switch.send_msg(req)

    @set_ev_cls(event.EventSwitchLeave, MAIN_DISPATCHER)
    def switch_leave_handler(self, ev):
        print ev
        switch = ev.switch.dp.id
        if switch in self.switches:
            self.switches.remove(switch)
            del self.datapath_list[switch]
            del self.adjacency[switch]

    @set_ev_cls(event.EventLinkAdd, MAIN_DISPATCHER)
    def link_add_handler(self, ev):
        s1 = ev.link.src
        s2 = ev.link.dst
        #print "switch", s1.dpid, "port:",s1.port_no
        #print "switch", s2.dpid, "port:",s2.port_no
        self.adjacency[s1.dpid][s2.dpid] = s1.port_no
        self.adjacency[s2.dpid][s1.dpid] = s2.port_no
        
        
        

    @set_ev_cls(event.EventLinkDelete, MAIN_DISPATCHER)
    def link_delete_handler(self, ev):
        s1 = ev.link.src
        s2 = ev.link.dst
        # Exception handling if switch already deleted
        try:
            del self.adjacency[s1.dpid][s2.dpid]
            del self.adjacency[s2.dpid][s1.dpid]
        except KeyError:
            pass

