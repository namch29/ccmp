For abilene topology
1) run abilene: 
      sudo python abilene.py
2) run ryu:
      ryu-manager --observe-links ccmp_abilene_1307.py
     
3) Check multipath:
      mininet: iperf h1 h7
      sudo ovs-ofctl -O OpenFlow13 dump-ports s13
      sudo ovs-ofctl -O OpenFlow13 dump-flows s13
      sudo ovs-ofctl -O OpenFlow13 dump-groups s13
