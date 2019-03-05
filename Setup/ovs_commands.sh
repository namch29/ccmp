ovs-dpctl del-flows

#Multipath
#add group
ovs-ofctl -O OpenFlow13 add-group s1 group_id=10,type=select,bucket=weight:5,output:2,bucket=weight:5,output:3 
ovs-ofctl -O OpenFlow13 add-group s4 group_id=40,type=select,bucket=weight:5,output:1,bucket=weight:5,output:2 

#ovs-ofctl -O OpenFlow13 add-group s1 group_id=11,type=reordering,bucket=output:1
#ovs-ofctl -O OpenFlow13 add-group s4 group_id=41,type=reordering,bucket=output:3


#s1
ovs-ofctl -O OpenFlow13 add-flow s1  in_port=1,ip,nw_src=10.0.0.1,nw_dst=10.0.0.2,actions=group:10
ovs-ofctl -O OpenFlow13 add-flow s1  in_port=2,ip,nw_src=10.0.0.2,nw_dst=10.0.0.1,actions=output:1
ovs-ofctl -O OpenFlow13 add-flow s1  in_port=3,ip,nw_src=10.0.0.2,nw_dst=10.0.0.1,actions=output:1


#s2
ovs-ofctl -O OpenFlow13 add-flow s2  in_port=1,ip,nw_src=10.0.0.1,nw_dst=10.0.0.2,actions=output:2
ovs-ofctl -O OpenFlow13 add-flow s2  in_port=2,ip,nw_src=10.0.0.2,nw_dst=10.0.0.1,actions=output:1


#s3
ovs-ofctl -O OpenFlow13 add-flow s3  in_port=1,ip,nw_src=10.0.0.1,nw_dst=10.0.0.2,actions=output:2
ovs-ofctl -O OpenFlow13 add-flow s3  in_port=2,ip,nw_src=10.0.0.2,nw_dst=10.0.0.1,actions=output:1


#s4
ovs-ofctl -O OpenFlow13 add-flow s4  in_port=1,ip,nw_src=10.0.0.1,nw_dst=10.0.0.2,actions=output:3
ovs-ofctl -O OpenFlow13 add-flow s4  in_port=2,ip,nw_src=10.0.0.1,nw_dst=10.0.0.2,actions=output:3
ovs-ofctl -O OpenFlow13 add-flow s4  in_port=3,ip,nw_src=10.0.0.2,nw_dst=10.0.0.1,actions=group:40


## Single Path
##s1
#ovs-ofctl -O OpenFlow13 add-flow s1  in_port=1,ip,nw_src=10.0.0.1,nw_dst=10.0.0.2,actions=output:2
#ovs-ofctl -O OpenFlow13 add-flow s1  in_port=2,ip,nw_src=10.0.0.2,nw_dst=10.0.0.1,actions=output:1

##s2
#ovs-ofctl -O OpenFlow13 add-flow s2  in_port=1,ip,nw_src=10.0.0.1,nw_dst=10.0.0.2,actions=output:2
#ovs-ofctl -O OpenFlow13 add-flow s2  in_port=2,ip,nw_src=10.0.0.2,nw_dst=10.0.0.1,actions=output:1
##s4
#ovs-ofctl -O OpenFlow13 add-flow s4  in_port=1,ip,nw_src=10.0.0.1,nw_dst=10.0.0.2,actions=output:3
#ovs-ofctl -O OpenFlow13 add-flow s4  in_port=3,ip,nw_src=10.0.0.2,nw_dst=10.0.0.1,actions=output:1
