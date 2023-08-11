import os

# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
# 
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.

def onValueChange(par, val, prev):
	if (par.name == 'Targetcomp' or
			par.name == 'Versioning' or
			par.name == 'Version' or
			par.name == 'Customname'):
		parent().SetFinalFileName()
	elif par.name == 'Outputfolder':
		parent().SetFinalPath()

def onPulse(par):
	if par.name == 'Package':
		parent().GeneratePackage()