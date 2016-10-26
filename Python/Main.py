import sys
import time
import math
import numpy as np
import OSC_communication as osc
import Movuino_Streamer as mov


def main(args = None):

	# Initialize streaming thread
	streamer= mov.DataStreamer()

	# Initializa data collection and run the thread
	streamer.start_newCollection() 

	osc_clientPD = osc.OSCclient('127.0.0.1', 7000) # Init client communication on specific Ip and port
	osc_clientPr = osc.OSCclient('127.0.0.1', 5000) # Init client communication on specific Ip and port

	
	rawData = np.zeros((1,2)) # reset data collection array
	oldPx = 0
	oldPy = 0
	oldVx = 0
	oldVy = 0
	oldAx = 0
	oldAy = 0

	while True:
		timer1 = time.time()
		time.sleep(0.05)
		#time.sleep(1)

		# Return current data received
		ax = float(streamer.get_lastData()[1])
		ay = float(streamer.get_lastData()[2])

		rawData = np.concatenate((rawData, [[ax,ay]]), axis=0)
		if (rawData.shape[0] > 5):
			rawData = rawData[1:,:]
		meanData = np.mean(rawData,axis=0) # compute mean average to smooth data

		ax = meanData[0]
		ay = meanData[1]

		ax /= float(32768)
		ay /= float(32768)

		x_ = ax
		y_ = ay
		d_ = math.sqrt(x_**2 + y_**2)

		osc_clientPr.sendOSCMessage('x', x_)
		osc_clientPr.sendOSCMessage('y', y_)
		osc_clientPD.sendOSCMessage('distance', d_)

		oldPx = ((ax * 0.05 + oldAx)*0.05 + oldVx)*0.05
		oldPy = ((ay * 0.05 + oldAy)*0.05 + oldVy)*0.05
		oldVx = (ax * 0.05 + oldAx)*0.05
		oldVy = (ay * 0.05 + oldAy)*0.05
		oldAx = ax * 0.05
		oldAy = ay * 0.05

		print "---------------"

	# Return all data received since last collection initialization
	print streamer.get_dataCollection()

	osc_server.closeServer() # ERROR MESSAGE but close the OSC server without killing the app
	streamer.stop() # Stop streaming
	streamer.join() # Close thread

if __name__ == '__main__':
    sys.exit(main())