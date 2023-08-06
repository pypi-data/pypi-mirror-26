# SciFiCam 
# Copyright (C) 2017  Mihails Delmans

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import threading
import owncloud
from time import sleep

'''
OwnCloudThread

Handles syncronisation to an OwnCloud server
'''

class OwnCloudThread(threading.Thread):
	def __init__(self, camera, ocAddress, ocLogin, ocPass, ocLocalDir, ocRemoteDir = "SciFiCam"):
		super(OwnCloudThread, self).__init__()
		self.camera = camera
		self.camera._issueMessage("Initialising client for {0}".format(ocAddress), level = 2)
		
		self.client		= owncloud.Client(ocAddress)
		
		camera._issueMessage("Logging in as {0}".format(ocLogin), level = 2)
		
		self.client.login(ocLogin, ocPass)
		
		self.remoteDir	= ocRemoteDir
		self.localDir	= ocLocalDir
		fileInfo = self.client.file_info(self.remoteDir)
		if not fileInfo:
			self.client.mkdir(self.remoteDir)

		self._stop_event 	= threading.Event()
		camera._issueMessage("OwnCloud is setup".format(ocLogin), level = 2)
	
	'''
	updateDir() checs for mismatches between loacl and remote directories and updates accordingly.
	'''
	def updateDir(self, remoteDir, localDir):
		remoteFiles = [ str(os.path.basename( os.path.normpath(file.path) )) for file in self.client.list(remoteDir)]

		for fileName in os.listdir(localDir):
			
			localPath = os.path.join(localDir, fileName)
			remotePath = os.path.join(remoteDir, fileName)
			
			if not fileName in remoteFiles and not fileName.endswith('.part'):
				self.camera._issueMessage("Uploading {0} to {1}".format(localPath, remotePath), level = 2)

				if os.path.isdir(localPath):
					self.client.mkdir( remotePath )
				else:
					self.client.put_file( remotePath, localPath )
	
			elif os.path.isdir(localPath):
				self.updateDir(remotePath, localPath)


	def run(self):
		while not self._stop_event.wait(3):
			self.updateDir(self.remoteDir, self.localDir)
			sleep(3)
