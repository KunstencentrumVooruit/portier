PORTIER // PYTHON SCRIPT OM NOODDEUREN TE OPENEN
************************************************

Running as service
------------------

-> /etc/init.d/portier.sh

-> Script startte in eerste instantie niet op omdat /dev/ttyUSB0 & /dev/ttyUSB1 nog niet klaar waren.
	Oplossing: in portier.sh, dat getSMS.py opstart, kan je (bovenaan) meegeven waarop het script 
	moet wachten om opgestart te worden. De variabele $all zorgt ervoor dat het script helemaal 
	op het einde van de bootcyclus wordt opgestart
	(https://wiki.debian.org/LSBInitScripts)

Logrotate
---------

/var/log/portier.log {
  rotate 1
  daily
  compress
  missingok
  notifempty
}

/var/log/portier.log

GNOKII & GAMMU
--------------

* apt-get install gnokii usb-modeswitch
* sudo usb_modeswitch -v 0x12d1 -p 0x1521 -M \
 55534243123456780000000000000011060000000000000000000000000000  (haal juiste hex adressen uit lsusb!)
* gnokii config file:
>>  [global]
    model = AT
    port = /dev/ttyUSB0
    connection = serial  <<

*commando's*

-> gnokii -c gnokii --identify   (-c gnokii = config file)
-> gnokii -c gnokii --getsms SM 0 1 (SM = SIM geheugen)
-> echo TEST | gnokii -c gnokii --sendsms 0495221978

MOD-IO2
-------

i2cset -y 2 0x21 0x40 0x03
