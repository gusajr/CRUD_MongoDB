#from six.moves import tkinter as tk
import tkinter as tk
import getpass
from PIL import Image
from pymongo import MongoClient
import pprint

class UI(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.master = master
		self.init_ui()

		#hay fierro = database con la informacion of the sensor
		#if(hay fierro):
		#	mandas alerta


	def init_ui(self):
		self.master.title("Metal detector")
		self.master.configure(background='white')
		JFrame1 = tk.Frame(root,height=900,width =650)
		self.JFrame1 = JFrame1
		self.JFrame1.configure(background='white')
		self.JFrame1.grid_propagate(False)
		self.title  = tk.Label (root, text="Metal detector",height=8,width=120, fg="black",bg="red", font=("Arial", 10))
		self.graphs  = tk.Button (self.JFrame1, text="Graphs",height=12,width=39, fg="black",bg="SlateGray1").grid(padx=20, pady=20,row=0, column=0)
		rawData = tk.Button (self.JFrame1, text="Raw data",height=12,width=39, fg="white",bg="grey",command=self.rawDataFunction).grid(padx=20, pady=20, row=0, column=1)#.expand()
		self.rawData = rawData
		dataLog = tk.Button (self.JFrame1, text="Data log",height=12,width=39, fg="white",bg="grey").grid(padx=20, pady=20, row=1, column=0)#.expand()
		self.dataLog = dataLog
		quit    = tk.Button (self.JFrame1, text="Quit",height=12,width=39,fg="black",bg="SlateGray1", command=self.quit).grid(padx=20, pady=20, row=1, column=1)#.expand()
		self.quit = quit
		self.title.pack()
		self.JFrame1.pack()

	def rawDataFunction(self):
		#print("hola")
		self.windowRawData=WindowRawData()

class WindowRawData(UI):
	def __init__(self):
		windowRawData= tk.Frame.__init__(self)
		windowRawData=tk.Tk()
		#self.windowRawData=windowRawData
		self.windowRawData=windowRawData
		self.windowRawData.geometry("800x650")
		self.windowRawData.resizable(0,0)
		self.windowRawData.title("Raw Data window Data Base")
		self.windowRawData.configure(background='light cyan')
		texto="You are accessing to the Raw Data Database, what do you want to do?"
		self.texto=texto
		etiqueta=tk.Label(self.windowRawData, text=self.texto, font=("Arial", 15), background='light cyan')
		self.etiqueta = etiqueta
		self.etiqueta.pack()
		word=tk.StringVar()
		self.word=word
		serial=""
		self.serial=serial
		entrySearchLog=tk.Entry(self.windowRawData,width=80,textvariable=self.word)
		self.entrySearchLog=entrySearchLog
		self.entrySearchLog.bind("<Return>",self.enterSearch)
		#self.entrySearchLog.bind("<Return>", (lambda event: self.getWord))
		self.entrySearchLog.pack(pady=20)
		buttonSearch = tk.Button(self.windowRawData, text="Log Search",command=self.getSearch, fg="black",bg="SlateGray1")
		self.buttonSearch=buttonSearch
		self.buttonSearch.place(x=650,y=45)
		entrySelectLog=tk.Entry(self.windowRawData,width=80)
		self.entrySelectLog=entrySelectLog
		self.entrySelectLog.pack(pady=20)
		self.entrySelectLog.bind("<Return>",self.enterSelect)
		buttonSelectLog = tk.Button(self.windowRawData, text="Select log",command=self.getSelect, fg="black",bg="SlateGray1")
		self.buttonSelectLog=buttonSelectLog
		self.buttonSelectLog.place(x=650, y=105)
		entryAddComment=tk.Entry(self.windowRawData,width=80)
		self.entryAddComment=entryAddComment
		self.entryAddComment.pack(pady=20)
		self.entryAddComment.bind("<Return>",self.enterComment)
		self.buttonAddComment = tk.Button(self.windowRawData, text="Add comment", fg="black",bg="SlateGray1", command=self.getComment)
		self.buttonAddComment.place(x=650, y=165)
		#entry=TextEntry(self)
		#entry.pack()
		JFrame2 = tk.Frame(windowRawData,height=900,width =650)
		self.JFrame2 = JFrame2
		scrollbar=tk.Scrollbar(self.JFrame2)
		self.scrollbar=scrollbar
		text = tk.Text(self.JFrame2, height=25, width=60, font=("Arial", 10))
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.text=text
		self.text.pack(side=tk.LEFT, fill=tk.Y)
		self.scrollbar.config(command=text.yview)
		self.text.config(yscrollcommand=scrollbar.set)
		#quote = """***********************************Bienvenido***********************************"""
		quote=""
		self.quote=quote
		
		client = MongoClient(direccion_ip)
		self.client=client
		db=client.bosch
		self.db=db
		collection= db.bosch.RawData
		#print(db.list_collection_names())
		self.collection=collection
		read=""
		self.read=read
		#list=[][]
		#cont=0
		#self.cont=cont
		for register in self.collection.find():
			#pprint.pprint(register)
			#read=read+"\n"+str(register)
			#list.append(str(register))
			#self.cont+=1
			self.read=""" ********************************************************************************
						\n*	    	  Register number {0} in RawDatabase 					 *
						\n*********************************************************************************\n""".format(register['Register number'])
			self.text.insert(tk.END, self.read)
			self.read=("Magnetic field strenght [T]: {0} \nSent frequency [Hz]: {1}".format(
				register['Magnetic field strenght [T]'],register['Sent frequency [Hz]']))
			self.text.insert(tk.END, self.read)
			self.read=("\nReceived frequency [Hz]: {0}\n".format(
				register['Received frequency [Hz]']))
			self.text.insert(tk.END, self.read)
		self.word=""
		#for register in self.collection.find({'Register number':{'$eq':self.word}}):
		#	pprint.pprint(register)
		'''for car in cars:
        print('{0} {1}'.format(car['name'], 
            car['price']))
        '''
		self.text.see("end")
		self.JFrame2.pack()
		

	def enterSearch(self,event):
		self.getSearch()
	def enterSelect(self,event):
		self.getSelect()
	def enterComment(self,event):
		self.getComment()

	def getSearch(self):
		self.word=int(self.entrySearchLog.get())
		self.entrySearchLog.delete(0,tk.END)
		self.addText()
		self.word=""

	def getSelect(self):
		self.word=int(self.entrySelectLog.get())
		self.entrySelectLog.delete(0,tk.END)
		self.selectLog()

	def getComment(self):
		self.word=self.entryAddComment.get()
		self.entryAddComment.delete(0,tk.END)
		print(self.word)
		self.commentLog(self.word)

	def addText(self):
		for register in self.collection.find({'Register number':{'$eq':self.word}}):
			#pprint.pprint(register)
			#read=read+"\n"+str(register)
			#list.append(str(register))
			self.read="""\n-----------------------------------------------------------------------------------------------------
			\n|	   	        Register number {0} found		 		    	  |
			\n-----------------------------------------------------------------------------------------------------\n""".format(self.word)
			self.text.insert(tk.END, self.read)
			self.read=("Magnetic field strenght [T]: {0} \nSent frequency [Hz]: {1}".format(
				register['Magnetic field strenght [T]'],register['Sent frequency [Hz]']))
			self.text.insert(tk.END, self.read)
			self.read=("\nReceived frequency [Hz]: {0}\n".format(
				register['Received frequency [Hz]']))
			self.text.insert(tk.END, self.read)
			#self.read=("Comments: {0}\n".format(
			#	register['Comments']))
			cont=1
			for comment in register['Comments']:
				self.read=("Comment"+str(cont)+": "+comment+"\n")
				self.text.insert(tk.END, self.read)
				cont+=1

		#self.text.insert(tk.END,"hola")
			#self.text.insert(tk.END, self.read)
		#self.text.insert(tk.END, '\n')
		#self.text.insert(tk.END, "Se buscó el registro con la serie: "+self.word)
		self.text.see("end")
		self.word=""

	def selectLog(self):
		self.serial=self.word
		for register in self.collection.find({'Register number':{'$eq':self.word}}):
			#pprint.pprint(register)
			self.read="""\n*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*----*--*--*--*--*--*--*--*--*--*--*--*--*--
						\n|   		Register number {0} found and selected                |
						\n*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*----*--*--*--*--*--*--*--*--*--*--*--*--*--\n""".format(self.word)
			self.text.insert(tk.END, self.read)
		self.text.see("end")
	#def reset_scrollregion(self, event):
	#	self.JFrame2.configure(scrollregion=self.JFrame2.bbox("all"))

	def commentLog(self, comment):
		#print("comentario: "+comment)
		#for register in self.collection.find({'Register number':{'$eq':self.serial}}):
			#coll.update({'ref': ref}, {'$push': {'tags': new_tag}})

		self.collection.update_one({'Register number':self.serial}, {'$push': {'Comments': self.word}})
			#register.comment(comment)
		self.read="""\n.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-
						\n|   	   	        Comment added correctly			 	         	   |
						\n.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-.-..-""".format(self.word)
		self.text.insert(tk.END, self.read)
		self.text.see("end")

	def closeW(self):
		self.destroy()

'''class TextEntry(tk.Button):
	def __init__(self):
		self.tk=tk
		entrySearchLog=tk.Entry(width=80)
		self.entrySearchLog=entrySearchLog
		#self.entrySearchLog.pack()
'''
if  __name__== "__main__":
	
	root = tk.Tk()
	root.geometry("900x650")
	APP=UI(master=root)
	root.resizable(0,0)
	APP.mainloop()