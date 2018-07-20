I. Uninstall OVS
  apt-get remove openvswitch-common openvswitch-datapath-dkms openvswitch-controller openvswitch-pki openvswitch-switch

II. Build Open VSwitch từ source code.

1. Cài đặt các dependencies

    apt install gcc autoconf automake libtool make -y  

3. Clone mã nguồn từ Git

    git clone https://github.com/openvswitch/ovs  

2. Bootstrap Openvswitch (Neu down .tar thi khong can buoc nay)

   cd ovs  
  ./boot.sh

2. Configure

  ./configure --prefix=/usr --localstatedir=/var --sysconfdir=/etc

3. Install

  make  
  make install  

4. Enable module openvswitch

  modprobe openvswitch  

5. Start OvS

  /usr/share/openvswitch/scripts/ovs-ctl start

6. Let's Check
  ovs-vsctl show
  
  Example:
        c2cf3eb0-7da1-457c-8664-99264d79afc7
          Manager "ptcp:6640"
          ovs_version: "2.9.2"

==================================================================
Plot from iperf results:
1) Get desired data from file: 
    cat result |grep KBytes |tr - " " |awk '{print $4,$11}'| head -n20 > plotdata
2) Plot using GNUPLOT

==================================================================
Run Sflow-rt:
1) Run:     ./start.sh
2) sudo mn --custom extras/sflow.py --custom abileneTopo.py --topo abilene --controller remote --mac