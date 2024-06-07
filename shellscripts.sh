# Shell script to run dumpcap to capture traffic
#!/bin/bash

# Capture traffic from interface wlan0 and save to a file
dumpcap -i wlan0 -w capture.pcap -b files:10 -b filesize:1000000

# Shell script to merge pcap files
#!/bin/bash

# Merge multiple pcap files into one
mergecap -w merged_capture.pcap capture_*.pcap

# Shell script to convert pcap to CSV
#!/bin/bash

# Export data to CSV
tshark -r merged_capture.pcap -T fields -e frame.time -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e _ws.col.Protocol -e tcp.len -e tcp.stream -e _ws.col.Info -E header=y -E separator=, -E quote=d > network_traffic.csv
