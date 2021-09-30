#This program is meant to test the PyEphem library for finding the positions of objects in the sky to take gyroscope readings from a Android phone and convert
#it into equatorial or galactic cooordinates, and then send them over a wired internet connection (using USB tethering with Wi-Fi turned off to reduce RF noise).

import ephem
#import android
#from os import system
import json
import socket

def generateCoordinates():
	"""Returns the gyroscope heading of the device."""
	# <DON'T Insert sketchy Termux command-line stuff here>
	return

def transformCoordinates(coordSystem="equatorial"):
	"""Does all the coordinate transforms to convert to a different coordinate system."""
	return

def transmit_coords(data):
	"""Transmits coordinates over a wired network connection."""
	return
