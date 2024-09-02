#!/bin/sh

cpuSpeed="$(cpupower frequency-info | grep -i 'current CPU frequency' | grep -i 'Ghz\|Mhz')"
cputemp="$(awk '{printf "%.f\n", int($1)/1000}' /sys/devices/pci0000:00/0000:00:18.3/hwmon/hwmon2/temp1_input)"
cpuload="$echo ""$[100-$(vmstat 1 2|tail -1|awk '{print $15}')]"%""

prefix="  current CPU frequency: "
suffix=" (asserted by call to kernel)"

speed=${cpuSpeed#"$prefix"}
speed=${speed%"$suffix"}
temp=${cputemp}

echo "CPU ${cpuload} @ ${speed} (${temp}°C)"
