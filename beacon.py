from scapy.all import *
from time import sleep
from multiprocessing import Process

crawl = {"comment" : ["gilgil", "hyejin", "minwoo", "kyeongsu", "dohoon"], "interface":"wlan1"}
br = "ff:ff:ff:ff:ff:ff"

class makebeacon:
	dot11 = Dot11(addr1=br, addr2 = str(RandMAC()), addr3=str(RandMAC()))
	beacon11 = Dot11Beacon(cap="ESS+privacy") #option : ESS or ESS+privacy

	def __init__(self, count, interface):
		self.count = count
		self.interface = interface

	def sendbeacon(self):
		essid = Dot11Elt(ID="SSID", info=crawl["comment"][self.count])

		sr = Dot11Elt(ID="Rates", info="\x01\x08\x82\x84\x8b\x96\x0c\x12\x18\x24")
		#ds = Dot11Elt(ID="DSset", info="\x03")
		#tim = Dot11Elt(ID="TIM", info="\x00\x01\x00\x00")
		#rsn = Dot11Elt(ID='RSNinfo', info=(
		#'\x01\x00'                 #RSN Version 1
		#'\x00\x0f\xac\x02'         #Group Cipher Suite : 00-0f-ac TKIP
		#'\x02\x00'                 #2 Pairwise Cipher Suites (next two lines)
		#'\x00\x0f\xac\x04'         #AES Cipher
		#'\x00\x0f\xac\x02'         #TKIP Cipher
		#'\x01\x00'                 #1 Authentication Key Managment Suite (line below)
		#'\x00\x0f\xac\x02'         #Pre-Shared Key
		#'\x00\x00'))
		#sendp(RadioTap()/self.dot11/self.beacon11/essid/sr/ds/tim/rsn, iface=self.interface, loop=0,verbose=False)
		sendp(RadioTap()/self.dot11/self.beacon11/essid/sr, iface=self.interface, loop=0,verbose=False)
class Multibeacon(Process):

	def __init__(self, beaconobj):
		Process.__init__(self)
		self.beaconobj = beaconobj

	def run(self):
		self.beaconobj.sendbeacon()
		sleep(slptime)


if __name__ == "__main__":
	slptime = input("write sleep time: ")

	beaconlist = []
	p_list = []

	for i in range(len(crawl["comment"])):
		beaconlist.append(makebeacon(i, crawl["interface"]))

	print("sending packets")
	while(1):
		for i in range(len(beaconlist)):
#			beaconlist[i].sendbeacon()
#			sleep(slptime)
			p = Multibeacon(beaconlist[i])
			p.start()
		for p in p_list:
			p.join()
