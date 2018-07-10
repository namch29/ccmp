from __future__ import division
import copy
from operator import attrgetter

from ryu import cfg
from ryu.base import app_manager
from ryu.base.app_manager import lookup_service_brick
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import hub

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

from DemandEstimation import demand_estimation

DISCOVERY_PERIOD = 10   # For discovering topology.
MONITOR_PERIOD = 5   # For monitoring traffic
MAX_CAPACITY = 1000000   # Max capacity of link, Kbit/s

class CcmpNetworkMonitor(app_manager.RyuApp):
	"""
		CCmpNetworkMonitor is a Ryu app for collecting traffic information based on Hedera project.
	"""
	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

	def __init__(self, *args, **kwargs):
		super(CcmpNetworkMonitor, self).__init__(*args, **kwargs)
		#self.name = 'monitor'
		self.datapaths = {}
		self.flow_stats = {}
		self.flow_speed = {}
		self.stats = {}
		# Create four data structures for Hedera specially.
		self.hostsList = []
		self.flows = []   			# Record flows that need to be rescheduled. (hmc)
		self.statRecord = []
		
		# Start to green thread to monitor traffic and calculating
		# free bandwidth of links respectively.
		self.monitor_thread = hub.spawn(self._monitor)
		self.weight = "bw"
		self.isNewFile=True
		

	def _monitor(self):
		"""
			Main entry method of monitoring traffic.
		"""
		while True:
			# Refresh data.
			self.stats['flow'] = {}
			self.statRecord = []
			self.flows = []
			#print "Lenght of datapaths", len(self.datapaths)
			for dp in self.datapaths.values():
				self._request_stats(dp)
			print "Monitoring"
			hub.sleep(MONITOR_PERIOD)
			
			if self.stats['flow']:
				self.show_stat('flow')
				hub.sleep(1)
	
	
	def _request_stats(self, datapath):
		"""
			Sending request msg to datapath
		"""
		#print "requesting stats"
		self.logger.debug('send stats request: %016x', datapath.id)
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		
		req = parser.OFPFlowStatsRequest(datapath)
		datapath.send_msg(req)

	def _get_time(self, sec, nsec):
		return sec + nsec / 1000000000.0

	def _get_period(self, n_sec, n_nsec, p_sec, p_nsec):
		return self._get_time(n_sec, n_nsec) - self._get_time(p_sec, p_nsec)
	
	def _get_speed(self, now, pre, period):
		if period:
			return (now - pre) / (period)
		else:
			return 0
			
	def _demandEstimator(self, flows, hostsList):
		'''
			Estimate flows' demands.
		'''
		estimated_flows = demand_estimation(flows, hostsList)
		
	def _save_stats(self, _dict, key, value, length=5):
		if key not in _dict:
			_dict[key] = []
		_dict[key].append(value)
		if len(_dict[key]) > length:
			_dict[key].pop(0)
	
	
	@set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
	def _flow_stats_reply_handler(self, ev):
		"""
			Save flow stats reply information into self.flow_stats.
			Calculate flow speed and Save it.
			(old) self.flow_stats = {dpid:{(in_port, ipv4_dst, out-port):[(packet_count, byte_count, duration_sec,  duration_nsec),],},}
			(old) self.flow_speed = {dpid:{(in_port, ipv4_dst, out-port):[speed,],},}
			(new) self.flow_stats = {dpid:{(priority, ipv4_src, ipv4_dst):[(packet_count, byte_count, duration_sec,  duration_nsec),],},}
			(new) self.flow_speed = {dpid:{(priority, ipv4_src, ipv4_dst):[speed,],},}
			Because the proactive flow entrys don't have 'in_port' and 'out-port' field.
			Note: table-miss, LLDP and ARP flow entries are not what we need, just filter them.
		"""
		body = ev.msg.body
		dpid = ev.msg.datapath.id
		self.statRecord.append(dpid)
		self.stats['flow'][dpid] = body
		self.flow_stats.setdefault(dpid, {})
		self.flow_speed.setdefault(dpid, {})
		for stat in sorted([flow for flow in body if ((flow.priority not in [0, 65535]) and (flow.match.get('ipv4_src')) and (flow.match.get('ipv4_dst')) )],
						   key=lambda flow: (flow.priority, flow.match.get('ipv4_src'), flow.match.get('ipv4_dst'))):
			key = (stat.priority, stat.match.get('ipv4_src'), stat.match.get('ipv4_dst'))
			value = (stat.packet_count, stat.byte_count,
					 stat.duration_sec, stat.duration_nsec)
			self._save_stats(self.flow_stats[dpid], key, value, 5)
			#print self.flow_stats[dpid]
			#print stat.instructions
			# Get flow's speed and Save it.
			pre = 0
			period = MONITOR_PERIOD
			tmp = self.flow_stats[dpid][key]
			if len(tmp) > 1:
				pre = tmp[-2][1]
				period = self._get_period(tmp[-1][2], tmp[-1][3], tmp[-2][2], tmp[-2][3])
			speed = self._get_speed(self.flow_stats[dpid][key][-1][1], pre, period)
			self._save_stats(self.flow_speed[dpid], key, speed, 5)

		
		# Record flows that need to be rescheduled. (hmc)
			if str(dpid).startswith('3'):
				flowDemand = speed * 8.0 / (MAX_CAPACITY * 1000)
				src = stat.match['ipv4_src']
				dst = stat.match['ipv4_dst']
				if flowDemand > 0.1:
					if src not in self.hostsList:
						self.hostsList.append(src)
					if dst not in self.hostsList:
						self.hostsList.append(dst)
					self.flows.append({'src': src, 'dst': dst, 'demand': flowDemand,
						'converged':False, 'receiver_limited': False,
						'match': stat.match, 'priority': stat.priority})
			else:
				pass
				
		# Estimate flows' demands if all the flow_stat replies are received.
		if len(self.statRecord) == len(self.datapaths) and self.flows:
			flows = sorted([flow for flow in self.flows], key=lambda flow: (flow['src'], flow['dst']))
			hostsList = sorted(self.hostsList)
			self._demandEstimator(flows, hostsList)
			print "Demand was calculated!!"
		else:
			pass

	@set_ev_cls(ofp_event.EventOFPStateChange,
				[MAIN_DISPATCHER, DEAD_DISPATCHER])
	def _state_change_handler(self, ev):
		"""
			Record datapath information.
		"""
		datapath = ev.datapath
		if ev.state == MAIN_DISPATCHER:
			if not datapath.id in self.datapaths:
				self.logger.debug('register datapath: %016x', datapath.id)
				self.datapaths[datapath.id] = datapath
		elif ev.state == DEAD_DISPATCHER:
			if datapath.id in self.datapaths:
				self.logger.debug('unregister datapath: %016x', datapath.id)
				del self.datapaths[datapath.id]
		else:
			pass
	
	def save_stat_to_file(self, _type):
		'''
			Show statistics information according to data type.
			_type: 'port' / 'flow'
		'''
		bodys = self.stats[_type]
		
		if self.isNewFile==True:
			self.isNewFile =False
			method = "w"
			
		else:
			method = "a"
		f = open("workfile",method)
		
		 	
		if _type == 'flow':
			max_speed = 0
			u_time= time.time()
			f.write('\nTime:%8d:' %u_time) 
			f.write('\ndatapath  '
				'priority        ip_src        ip_dst  '
				'  packets        bytes  flow-speed(Mb/s)')
			f.write('\n--------  '
				'--------  ------------  ------------  '
				'---------  -----------  ----------------')
			for dpid in sorted(bodys.keys()):

				for stat in sorted([flow for flow in bodys[dpid] if ((flow.priority not in [0, 65535]) and (flow.match.get('ipv4_src')) and (flow.match.get('ipv4_dst')))],
						   key=lambda flow: (flow.priority, flow.match.get('ipv4_src'), flow.match.get('ipv4_dst'))):
					f.write('\n%8d  %8s  %12s  %12s  %9d  %11d  %16.1f' % (
						dpid,
						stat.priority, stat.match.get('ipv4_src'), stat.match.get('ipv4_dst'),
						stat.packet_count, stat.byte_count,
						abs(self.flow_speed[dpid][(stat.priority, stat.match.get('ipv4_src'), stat.match.get('ipv4_dst'))][-1])*8/1000000.0))
					
			f.write("\n========================================================================================")
		f.close()	
		
	def show_stat(self, _type):
		'''
			Show statistics information according to data type.
			_type: 'port' / 'flow'
		'''
		bodys = self.stats[_type]
		
		self.save_stat_to_file(_type)
		if _type == 'flow':
			print('\ndatapath  '
				'priority        ip_src        ip_dst  '
				'  packets        bytes  flow-speed(Mb/s)')
			print('--------  '
				'--------  ------------  ------------  '
				'---------  -----------  ----------------')
			for dpid in sorted(bodys.keys()):

				for stat in sorted([flow for flow in bodys[dpid] if ((flow.priority not in [0, 65535]) and (flow.match.get('ipv4_src')) and (flow.match.get('ipv4_dst')))],
						   key=lambda flow: (flow.priority, flow.match.get('ipv4_src'), flow.match.get('ipv4_dst'))):
					print('%8d  %8s  %12s  %12s  %9d  %11d  %16.1f' % (
						dpid,
						stat.priority, stat.match.get('ipv4_src'), stat.match.get('ipv4_dst'),
						stat.packet_count, stat.byte_count,
						abs(self.flow_speed[dpid][(stat.priority, stat.match.get('ipv4_src'), stat.match.get('ipv4_dst'))][-1])*8/1000000.0))
			print
			
	

	
	
