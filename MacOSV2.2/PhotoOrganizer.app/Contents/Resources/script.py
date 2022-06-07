import os,sys
import shutil
import time

import qrcode
import cv2
import webbrowser

from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from PyQt5.QtWidgets import QMessageBox



def createqr(data, name):
	# output file name
	filename = f"{name}.JPG"
	# generate qr code
	img = qrcode.make(data)
	# save img to a file
	img.save(filename)

def readqr(fname):
	# preprocessing using opencv
	# print(fname)
	im = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
	blur = cv2.GaussianBlur(im, (5, 5), 0)
	ret, bw_im = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	# scanning the image using pyzbar
	qrscan = decode(bw_im, symbols=[ZBarSymbol.QRCODE])

	if(len(qrscan)>0):
		return qrscan[0].data.decode()
	else:
		return False	



# class ThreadClass(QtCore.QThread):
# 	def __init__(self, parent =None):
# 		super().__init__(parent)
# 	def run(self):
# 		while 1:
# 			for x in range(100):
# 				print(x)
# 				self.emit(QtCore.SIGNAL('val'),x)
# 				self.pBar.setValue(x)

# def updateProgressBar(self,value):
# 	self.pBar.setValue(value)



def mainFunc(self,dName):
	try:
		# new_name = os.path.abspath(os.getcwd())
		# name_of_dir = os.path.dirname(dName)
		# print(name_of_dir)
		# dir_files = shutil.copytree(dName,"TEMPFOLDER")
		# dir_files = os.listdir(dName)

		parent_dir = os.path.dirname(dName)
	
		name_dir = os.path.basename(dName)
		print(name_dir)
		newpath = parent_dir+'\\'+ name_dir+"organized" 

		if not os.path.exists(newpath):
			os.makedirs(newpath)

		os.chdir(dName)
		dir_files = os.listdir(dName)

		for f in dir_files:
			shutil.copy(f,newpath)

		os.chdir(newpath)

		# os.mkdir(parent_dir, str(name_dir) +"_Original")
		# os.mkdir(parent_dir,"Original")
		# print("Here is my Directory: ", dName)
		files = [f for f in sorted(os.listdir(dName)) if os.path.isfile(f) and (f.endswith("jpg") or f.endswith("png") or f.endswith("jpeg") or f.endswith('JPG'))]
		self.countChanged.emit([0,''])
		if(len (files)==0):
			eMsg1 = QMessageBox()
			eMsg1.setIcon(QMessageBox.Critical)
			eMsg1.setWindowTitle('Error')
			eMsg1.setText("No images are present!")
			eMsg1.exec()
			print('no images are present')
			exit()
		else:
			pass	

		event_dir = ''
		event_dir_lis = []
		image_dir_lis = []
		no_of_images = 0
		empty_str = ''
		created = ''
		count= 0
		
		for f in files:
			# scanning the files 
			scan = readqr(f)
			if (scan!=False):
				created = scan

				if(created[:-2] != event_dir):
					event_dir = created[:-2]
					# creating directory for the event
					os.mkdir(event_dir)


				try:
					# creating new directory with the client id 
					os.mkdir(scan)
					# moving the client dir to event dir 


					image_dir = shutil.move(scan, event_dir)
					os.mkdir(os.path.join(image_dir+'/','Preview Sets'))
					os.mkdir(os.path.join(image_dir+'/','Raw Pics of Photographer'))
					os.mkdir(os.path.join(image_dir+'/','Final Sets'))


					# renaming the qr code file after folder creating
					#qrname = f'qr-{f}'
					qrname = f"{created}{'{:03}'.format(0)}.JPG"
					os.rename(f, qrname)
					# moving qrcode file to client dir
					shutil.move(qrname, image_dir+"/Raw Pics of Photographer")
					# initializing image count to be placed in that client folder 
					no_of_images = 0

				except Exception as e:
					print(e)
					exit()
				
			else:
				no_of_images += 1
				if(created != empty_str):
					file_rename = f"{created}{'{:03}'.format(no_of_images)}.JPG"
					os.rename(f, file_rename)
					new_path = shutil.move(file_rename, image_dir+"/Raw Pics of Photographer")
					# print(f'{f} moved to {new_path}')
				else:
					eMsg = QMessageBox()
					eMsg.setIcon(QMessageBox.Critical)
					eMsg.setWindowTitle('Error')
					eMsg.setText("No Qr Code Found!")
					eMsg.exec()

			# webbrowser.open(event_dir)
			# print("CHECK: ", event_dir)
			count += 1
			perc = int(count/len(files)*100)
			self.countChanged.emit([perc,f])
			image_dir_lis.append(image_dir)
			event_dir_lis.append(event_dir)
			# print(image_dir)

		image_dir_lis = list(set(image_dir_lis))
		event_dir_lis = list(set(event_dir_lis))
		for items in image_dir_lis:
			# os.mkdir(os.path.join(items+'/','Preview Sets'))
			# os.mkdir(os.path.join(items+'/','Raw Pics of Photographer'))
			# os.mkdir(os.path.join(items+'/','Final Sets'))

			os.mkdir(os.path.join(items+'/Preview Sets','Basic watermarked'))
			os.mkdir(os.path.join(items+'/Preview Sets/Basic watermarked','8 Best edited & watermarked'))

			os.mkdir(os.path.join(items+'/Preview Sets','Standard watermarked'))
			os.mkdir(os.path.join(items+'/Preview Sets/Standard watermarked','16 Best edited & watermarked'))
			os.mkdir(os.path.join(items+'/Preview Sets/Standard watermarked','All raw watermarked'))


			os.mkdir(os.path.join(items+'/Preview Sets','Premium watermarked'))
			os.mkdir(os.path.join(items+'/Preview Sets/Premium watermarked','16 Best edited & watermarked'))
			os.mkdir(os.path.join(items+'/Preview Sets/Premium watermarked','All raw watermarked'))
			os.mkdir(os.path.join(items+'/Preview Sets/Premium watermarked','Video watermarked'))

			os.mkdir(os.path.join(items+'/Final Sets','Basic'))
			os.mkdir(os.path.join(items+'/Final Sets/Basic','8 Best edited'))


			os.mkdir(os.path.join(items+'/Final Sets','Standard'))
			os.mkdir(os.path.join(items+'/Final Sets/Standard','16 Best edited'))
			os.mkdir(os.path.join(items+'/Final Sets/Standard','All raw pics'))


			os.mkdir(os.path.join(items+'/Final Sets','Premium'))
			os.mkdir(os.path.join(items+'/Final Sets/Premium','16 Best edited'))
			os.mkdir(os.path.join(items+'/Final Sets/Premium','All raw'))
			os.mkdir(os.path.join(items+'/Final Sets/Premium','Video'))



		# print(image_dir_lis)
		# print(event_dir_lis)
		return event_dir_lis, event_dir,newpath
	except:	
		eMsg = QMessageBox()
		eMsg.setIcon(QMessageBox.Critical)
		eMsg.setWindowTitle('Error')
		eMsg.setText('Error' + str(sys.exc_info()[0]) + 'Occured')
		eMsg.exec()
		return False


