
from kano_wand.kano_wand import Shop, PATTERN
import time

shop = Shop()
while True:
	wands = shop.scan()
	if len(wands):
		print(wands[0]._dev.rssi)
	else:
		print("Out of range")
