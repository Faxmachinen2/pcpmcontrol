echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="a3c4", TAG+="uaccess"' > /usr/lib/udev/rules.d/70-pcpmcommand.rules
udevadm control --reload-rules
