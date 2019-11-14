# digital-terrain-mapping-wifi

Release Date: Jul 2019<br />


Code liberally taken from https://github.com/noobiedog/peanuts and https://github.com/Cyb3rHacks/Snoopy-ng-2018-UPDATED-

Changes:
* Removed bluetooth support
* Removed GPS capabilities
* Added channel hopping capabilities, channels are collected from the 'iwlist channel' command
  * You can customize how much time to wait between switching channels
  
To Do:
* Send data to a server in order to sync data from multiple devices scanning for signals
* Get the haslayer(Dot11) function working

+ Tested on: Linux 18.04.2 Ubuntu<br />

## Build Plan

### Dependencies
- Python 2.7+
	- NOTE: regarding scapy, haslayer(Dot11) does not function in Python 3 for unknown reasons, will test this more later!	
- Scapy
- aircrack-ng

### Installing from source
```bash
git clone https://github.com/zhaalex/digital-terrain-mapping-wifi.git
cd digital-terrain-mapping-wifi
pip install -r requirements.txt
```
### Sample Commands/How to Use

First, get the network interface you want to use with the command:
```bash
iwconfig
```

Select the interface you want, in this case, wlp3s0 (the one connected to wifi)<br />

Sample Output from 'iwconfig':
```bash
wlp3s0    IEEE 802.11  ESSID:"TEST_WIFI"  
          Mode:Managed  Frequency:5.32 GHz  Access Point: AA:AA:AA:AA:AA:AA  
          Bit Rate=162 Mb/s   Tx-Power=15 dBm   
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:on
          Link Quality=60/70  Signal level=-50 dBm  
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:2  Invalid misc:24   Missed beacon:0

eno1      no wireless extensions.

lo        no wireless extensions.
```

Sample Command:
```bash
python wifi_tracker.py -i wlp3s0 > output.txt
```

The only output from the program is: what channel we are sniffing on, and the MAC address of the devices. <br />

I haven't built in a dedicated file formatter, so for now, we are piping the output to output.txt.  To end the program, press the button combinations 'ctrl + c'.  In the cases that the program fails to stop properly, you may need to manually end monitor mode on your computer by using the following terminal command (notice how monitor mode added the 'mon' to the end of the wireless suffix: wlp3s0 -> wlp3s0mon): 
```bash
sudo airmon-ng stop wlp3s0mon
```














