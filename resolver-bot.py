from waveapi import events
from waveapi import model
from waveapi import robot
import waveapi.document as doc
import re

def OnParticipantsChanged(properties, context):
	"""Invoked when any participants have been added/removed."""
	added = properties['participantsAdded']
	for p in added:
		Notify(context)

def OnRobotAdded(properties, context):
	"""Invoked when the robot has been added."""
	root_wavelet = context.GetRootWavelet()
	root_wavelet.CreateBlip().GetDocument().SetText("I'm alive!")

def OnBlipSubmit(properties, context):
	"""Invoked whenever a blip is submitted"""
	blip = context.GetBlipById(properties['blipId'])
	contents = blip.GetDocument().GetText()
	p = re.compile('\(up:P00001\)')
	proteinlist = p.finditer(contents)
	blip.CreateChild().GetDocument().SetText("You submitted a blip!")
	for protein in proteinlist:
		strip_contents = contents.replace(protein.group(0), 'P00001')
		blip.GetDocument().SetText(strip_contents)

def Notify(context):
	root_wavelet = context.GetRootWavelet()
	root_wavelet.CreateBlip().GetDocument().SetText("Hi everybody!")

if __name__ == '__main__':
	myRobot = robot.Robot('resolver-bot', 
		image_url='http://resolver-bot.appspot.com/icon.png',
		version='0.0.3',
		profile_url='http://resolver-bot.appspot.com/')
	myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
	myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
	myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmit)
	myRobot.Run()
