import os

class Packager:
	def __init__(self, parentComp):
		self.parentComp = parentComp
		self.target = None

		self.fileOps = {}
		self.customPars = {}

		self.SetFinalPath()
		self.SetFinalFileName()

	def GeneratePackage(self):
		self.target = self.parentComp.par.Targetcomp.eval()
		self.fileOps = {}
		self.customPars = {}

		if hasattr(self.target, 'PreBuild'):
			self.log('Executing pre-build hook')
			self.target.PreBuild()

		self.build()

		if hasattr(self.target, 'PostBuild'):
			self.log('Executing post-build hook')
			self.target.PostBuild()

	def build(self):
		outDir = self.parentComp.par.Finalpath.eval()
		filePath = os.path.join(outDir, self.parentComp.par.Finalfilename.eval())
		
		if self.parentComp.par.Resetcustompars:
			self.log('Emptying custom parameters')
			self.emptyCustomPars()

		if self.parentComp.par.Unlinkexternalfiles:
			self.log('Unlinking external files:')
			self.unlinkExternalFiles()

		if not os.path.exists(outDir):
			os.makedirs(outDir)

		self.target.save(filePath)
		self.log(f'Wrote file {filePath}')
		
		if self.parentComp.par.Resetcustompars:
			self.log('Restoring custom parameters')
			self.restoreCustomPars()

		if self.parentComp.par.Unlinkexternalfiles:
			self.log('Relinking external files:')
			self.relinkExternalFiles()

	def unlinkExternalFiles(self):
		for extFileOp in self.target.findChildren(type=DAT, parName='file'):
			print(f'\t{extFileOp.path}')
			self.fileOps[extFileOp.name] = (extFileOp.par.file.eval(), extFileOp.par.syncfile.eval())
			extFileOp.par.syncfile = False
			extFileOp.par.file = ''

	def relinkExternalFiles(self):
		for extFileOp in self.target.findChildren(type=DAT, parName='file'):
			print(f'\t{extFileOp.path}')
			extFileOp.par.file = self.fileOps[extFileOp.name][0]
			extFileOp.par.syncfile = self.fileOps[extFileOp.name][1]

	def emptyCustomPars(self):
		for par in self.parentComp.par.Targetcomp.eval().customPars:
			if (not par.readOnly or
					(par.readOnly and par.mode == ParMode.CONSTANT) or
					(par.readOnly and par.isPython)):
				self.customPars[par.name] = par.val
				par.val = par.default
	
	def restoreCustomPars(self):
		for name, value in self.customPars.items():
			self.target.par[name] = value
	
	'''
	UTILS
	'''
	
	def SetFinalPath(self):
		if self.parentComp.par.Outputfolder != '':
			self.parentComp.par.Finalpath = os.path.abspath(self.parentComp.par.Outputfolder.eval())

	def SetFinalFileName(self):
		baseName = self.parentComp.par.Customname or self.parentComp.par.Targetcomp.val or ''
		version = f'_v{self.parentComp.par.Version}' if (self.parentComp.par.Versioning and self.parentComp.par.Version != '') else ''
		
		self.parentComp.par.Finalfilename = baseName + version + '.tox'
	
	def log(self, message):
		print(f'Packager - {message}')