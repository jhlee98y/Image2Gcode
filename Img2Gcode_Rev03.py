#!/usr/bin/python
version = '0.01'

version = '0.01'

import sys
VERSION = sys.version_info[0]

if VERSION == 3:
    from tkinter import *
    from tkinter.filedialog import *
    import tkinter.messagebox
else:
    from Tkinter import *
    from tkFileDialog import *
    import tkMessageBox

if VERSION < 3 and sys.version_info[1] < 6:
    def next(item):
        return item.next()

from math import *
from time import time
import os
import re
import binascii
import getopt
import operator

try:
    PIL = True
    from PIL import Image
    from PIL import ImageTk
    from PIL import ImageOps
    import _imaging
except:
    PIL = False
    
try:
    NUMPY = True
    try:
        import numpy.numarray as numarray
        import numpy.core
        olderr = numpy.core.seterr(divide='ignore')
        plus_inf = (numarray.array((1.,))/0.)[0]
        numpy.core.seterr(**olderr)
    except ImportError:
        import numarray, numarray.ieeespecial
        plus_inf = numarray.ieeespecial.inf
except:
    NUMPY = False

class Application(Frame):
    
    def __init__(self, master):
	Frame.__init__(self, master)
	self.w = 800
	self.h = 600
	frame = Frame(master, width= self.w, height=self.h)
	self.master = master
        self.x = -1
        self.y = -1	

	self.initComplete = 0	
	self.onConComplete = 0
	self.createWidgets()

		
    def createWidgets(self):
        ###########################################################################
        #                         INITILIZE VARIABLES                             #
        #    if you want to change a default setting this is the place to do it   #
        ###########################################################################        
        self.yscale     = StringVar()
        self.Xscale     = StringVar()
        self.pixsize    = StringVar()
        self.toptol     = StringVar()
        self.tolerance  = StringVar()
        self.units      = StringVar()
        self.funits     = StringVar()
        self.gpre       = StringVar()

	self.strXDPI    = StringVar()
	self.strYDPI    = StringVar()
	self.strRaster_w    = StringVar()
        self.strRaster_h    = StringVar()
	self.strRaster_w_mm    = StringVar()
        
	self.show_axis  = BooleanVar()
	self.invert     = BooleanVar()
	self.normalize  = BooleanVar()
	self.cuttop     = BooleanVar()
	self.cutperim   = BooleanVar()
	self.origin     = StringVar()
	self.strSPEED   = StringVar()
	self.strSPEED_rpd = StringVar()
	self.strLaser_str_low =  StringVar()
	self.strLaser_str_high =  StringVar()
        
        self.gcode      = []
	self.segID      = []
        self.IMAGE_FILE   = (os.path.expanduser("~")+"/None")
               
        self.aspect_ratio =  0
        self.SCALE = 1        
	self.XDPI = 200
	self.YDPI = 200	
        self.raster_w = 1  # inch unit
        self.raster_h = -1  # inch unit
        self.raster_mm_w = 25.4  # metric unit
        self.raster_mm_h = 25.4  # metric unit
	self.SPEED = 1000  # Laser Feedrate (mm/min)
	self.SPEED_rpd = 1000
	self.Laser_str_low = 40
	self.Laser_str_high =200	
	
	
        self.ui_TKimage = PhotoImage()
        self.im  = self.ui_TKimage
        self.wim = self.ui_TKimage.width()
        self.him = self.ui_TKimage.height()
        self.aspect_ratio =  float(self.wim-1) / float(self.him-1)
        
        ## Initialize String Valriables #
	self.show_axis.set(1)
	self.invert.set(0)
	self.normalize.set(0)
	self.cuttop.set(1)
	self.cutperim.set(1)  
	
        self.yscale.set("5.0")
        self.Xscale.set("0")
        self.pixsize.set("0")
        self.toptol.set("-0.005")
        self.tolerance.set("0.001")
        self.gpre.set("G21 G90")
	self.origin.set("Default")
	self.strXDPI.set("100")
	self.strYDPI.set("100")
	self.strRaster_w.set("1.0")
        self.strRaster_h.set("-1.0")
	self.strRaster_w_mm.set("100.0")
	
        self.yscale.set("5.0")
        self.Xscale.set("0")
        self.pixsize.set("0")	
	self.units.set("inch")            # Options are "in" and "mm"
	
	self.strSPEED.set("1000")
	self.strSPEED_rpd.set("3000")
	self.strLaser_str_low.set("40")
	self.strLaser_str_high.set("220")	

	self.statusMessage = StringVar()
	self.statusMessage.set("Welcome to Image2gcode")
	
	###########################################################################
	##                         Creat Frame                                    #
	##                                                                        #
	########################################################################### 
	self.master.bind("<Configure>", self.Master_Configure)
        self.master.bind('<Enter>', self.bindConfigure)
        #self.master.bind('<Escape>', self.KEY_ESC)
        #self.master.bind('<Control-g>', self.KEY_CTRL_G)	
	#self.master.title("Simple Image to Gcode Generator")
	#self.pack(fill=BOTH, expand=1)
	#Style().configure("TFrame", background="#333")
	#self.centerWindow()

	# Image Information	
	self.Label_font_prop = Label(self.master,text="Original Image Information:", anchor=W)

	self.Label_Yscale = Label(self.master,text="Image Height", anchor=CENTER)
	self.Label_Yscale_u = Label(self.master,text="pixel", anchor=W)
	self.Entry_Yscale_val = Label(self.master, textvariable=self.yscale, anchor=W)
	#self.Entry_Yscale = Entry(self.master,width="15")
	#self.Entry_Yscale.configure(textvariable=self.yscale)
	#self.Entry_Yscale.bind('<Return>', self.Recalculate_Click)
	#self.yscale.trace_variable("w", self.Entry_Yscale_Callback)
	#self.NormalColor =  self.Entry_Yscale.cget('bg')

	self.Label_Yscale2 = Label(self.master,text="Image Width", anchor=CENTER)
	self.Label_Yscale2_u = Label(self.master,text="pixel", anchor=W)
	self.Label_Yscale2_val = Label(self.master,textvariable=self.Xscale, anchor=W)

	self.Label_PixSize = Label(self.master,text="Pixel Size", anchor=CENTER)
	self.Label_PixSize_u = Label(self.master,text=" ", anchor=W)
	self.Label_PixSize_val = Label(self.master,textvariable=self.XDPI, anchor=W)
	
	
	# make a Status Bar
	self.statusbar = Label(self.master, textvariable=self.statusMessage, \
	                           bd=1, relief=SUNKEN , height=1)
	self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)
	

	# Creat Buttons
	#self.Save_Button = Button(self.master,text="Save G-Code",command=self.genGcode)
	#self.Roughing_but = Button(self.master,text="Open Roughing Settings",command=self.ROUGH_Settings_Window)

	# Creat Canvas
	lbframe = Frame( self.master )
	self.PreviewCanvas_frame = lbframe
	self.PreviewCanvas = Canvas(lbframe, width=self.w-250, \
	                                height=self.h-50, background="grey")
	self.PreviewCanvas.pack(side=LEFT, fill=BOTH, expand=1)
	self.PreviewCanvas_frame.place(x=230, y=10)

	self.PreviewCanvas.bind("<1>"        , self.mousePanStart)
	self.PreviewCanvas.bind("<B1-Motion>", self.mousePan)
	self.PreviewCanvas.bind("<2>"        , self.mousePanStart)
	self.PreviewCanvas.bind("<B2-Motion>", self.mousePan)
	self.PreviewCanvas.bind("<3>"        , self.mousePanStart)
	self.PreviewCanvas.bind("<B3-Motion>", self.mousePan)		
	
        
        # Creat File Menu
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        
        # File menu        
        fileMenu = Menu(menubar, tearoff = 0)
        fileMenu.add_command(label="Open", command=self.onOpen)
        fileMenu.add_command(label="Convert", command=self.onConvert)
        fileMenu.add_separator()
        fileMenu.add_command(label="Generate Gcode", command=self.genGcode)
        #fileMenu.add_command(label="Save as", command=self.donothing)
        fileMenu.add_command(label="Quit", command=self.menu_File_Quit)
        
        menubar.add_cascade(label="File", menu=fileMenu)        
        
        # Edit menu        
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="General Settings", command=self.GEN_Settings_Window)
        #editmenu.add_separator()
        #editmenu.add_command(label="Cut", command=self.donothing)
        #editmenu.add_command(label="Copy", command=self.donothing)
        #editmenu.add_command(label="Paste", command=self.donothing)
        #editmenu.add_command(label="Delete", command=self.donothing)
        #editmenu.add_command(label="Select All", command=self.donothing)
        
        menubar.add_cascade(label="Settings", menu=editmenu)

        # Help menu                
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)        

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)	
	
	
    ################################################################################
    def entry_set(self, val2, calc_flag=0, new=0):
        if calc_flag == 0 and new==0:
            try:
                self.statusbar.configure( bg = 'yellow' )
                val2.configure( bg = 'yellow' )
                self.statusMessage.set(" Recalculation required.")
            except:
                pass
        elif calc_flag == 3:
            try:
                val2.configure( bg = 'red' )
                self.statusbar.configure( bg = 'red' )
                self.statusMessage.set(" Value should be a number. ")
            except:
                pass
        elif calc_flag == 2:
            try:
                    self.statusbar.configure( bg = 'red' )
                    val2.configure( bg = 'red' )
            except:
                    pass
        elif (calc_flag == 0 or calc_flag == 1) and new==1 :
            try:
                    self.statusbar.configure( bg = 'white' )
                    self.statusMessage.set(" ")
                    val2.configure( bg = 'white' )
            except:
                    pass
        elif (calc_flag == 1) and new==0 :
            try:
                    self.statusbar.configure( bg = 'white' )
                    self.statusMessage.set(" ")
                    val2.configure( bg = 'white' )
            except:
                    pass
    
        elif (calc_flag == 0 or calc_flag == 1) and new==2:
            return 0
        return 1
    
    ################################################################################    
    def centerWindow(self):
        w=800 
        h=600
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        
        x = (sw-w)/2
        y = (sh-h)/2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))            
	
    ###############################################    
    def onOpen(self):
        global image       
        init_dir = os.path.dirname(self.IMAGE_FILE)
        if ( not os.path.isdir(init_dir) ):
            init_dir = os.path.expanduser("~")

        fileselect = askopenfilename(filetypes=[("Image Files", ("*.pgm","*.jpg","*.png","*.gif")),
                                                ("All Files","*")],\
                                                 initialdir=init_dir)        
        
        if fileselect != '' and fileselect != ():
            self.Read_image_file(fileselect)
            self.Plot_Data() 
        else:
            menu_File_Quit()


    ###############################################
    def Read_image_file(self,fileselect):
        im = []
        if not ( os.path.isfile(fileselect) ):
            self.statusMessage.set("Image file not found: %s" %(fileselect))
            self.statusbar.configure( bg = 'red' )            
        else:
            self.statusMessage.set("Image file: %s " %(fileselect))
            self.statusbar.configure( bg = 'white' ) 
            try:
		PIL_im = Image.open(fileselect)   
		self.wim, self.him = PIL_im.size
                # Convert image to grayscale
		PIL_im = PIL_im.convert("L") 
   

		self.aspect_ratio =  float(self.wim-1) / float(self.him-1)
		#self.Xscale.set("%.3f" %( self.aspect_ratio * float(self.yscale.get())) ) 
		self.yscale.set("%.3f" %(self.him))		
		self.Xscale.set("%.3f" %(self.wim))		
		
		self.pixsize.set("%.3f" %( float(self.yscale.get()) / (self.him - 1.0) ) )
                                
                ######################################
                ######################################
                #if PIL:
		self.im = PIL_im
		self.SCALE = 1
		self.ui_TKimage = ImageTk.PhotoImage(self.im.resize((50,50), Image.ANTIALIAS))
                #else:
                #    self.ui_TKimage = im
                #    self.im = self.ui_TKimage
                #    self.SCALE = 1
                    
		self.IMAGE_FILE = fileselect
                    
            except:
                self.statusMessage.set("Unable to Open Image file: %s" %(self.IMAGE_FILE))
                self.statusbar.configure( bg = 'red' )    
                
    ###############################################   
    def Quit_Click(self, event):
        self.statusMessage.set("Exiting!")
        root.destroy()

    ###############################################
    def mousePanStart(self,event):
        self.panx = event.x
        self.pany = event.y

    ###############################################
    def mousePan(self,event):
        all = self.PreviewCanvas.find_all()
        dx = event.x-self.panx
        dy = event.y-self.pany
        for i in all:
            self.PreviewCanvas.move(i, dx, dy)
        self.lastx = self.lastx + dx
        self.lasty = self.lasty + dy
        self.panx = event.x
        self.pany = event.y

   ###############################################	
    def Recalculate_Click(self, event):
        pass

    #############################
    def Entry_Yscale_Check(self):
        try:
            value = float(self.yscale.get())
            if  value <= 0.0:
                self.statusMessage.set(" Height should be greater than 0 ")
                return 2 # Value is invalid number
            else:
                self.Xscale.set("%.3f" %( self.aspect_ratio * float(self.yscale.get())) )
                self.pixsize.set("%.3f" %( float(self.yscale.get()) / (self.him - 1.0) ) )
        except:
            return 3     # Value not a number
        return 0         # Value is a valid number
    def Entry_Yscale_Callback(self, varName, index, mode):
        self.entry_set(self.Entry_Yscale, self.Entry_Yscale_Check(), new=1)      
    
    ##########################################
    #        CANVAS PLOTTING STUFF           #
    ##########################################
    def Plot_Data(self):
        self.PreviewCanvas.delete(ALL)
        
        ##if (self.Check_All_Variables() > 0):
        ##    return
        
        cszw = int(self.PreviewCanvas.cget("width"))
        cszh = int(self.PreviewCanvas.cget("height"))
        wc = float(cszw/2)
        hc = float(cszh/2)

        try:
            test = self.im.size
            self.SCALE = min( float(cszw-20)/float(self.wim), float(cszh-20)/float(self.him))
            if self.SCALE < 1:
                nw=int(self.SCALE*self.wim)
                nh=int(self.SCALE*self.him)
            else:
                nw = self.wim
                nh = self.him
                self.SCALE = 1
            self.ui_TKimage = ImageTk.PhotoImage(self.im.resize((nw,nh), Image.ANTIALIAS))
        except:
            self.SCALE = 1            

        self.canvas_image = self.PreviewCanvas.create_image(wc, \
                            hc, anchor=CENTER, image=self.ui_TKimage)

        midx = 0
        midy = 0
        minx = int(self.wim/2)
        miny = int(self.him/2)
        maxx = -minx
        maxy = -miny
        
        ##########################################
        #         ORIGIN LOCATING STUFF          #
        ##########################################
        CASE = str(self.origin.get())
        if     CASE == "Top-Left":
            x_zero = minx
            y_zero = maxy
        elif   CASE == "Top-Center":
            x_zero = midx
            y_zero = maxy
        elif   CASE == "Top-Right":
            x_zero = maxx
            y_zero = maxy
        elif   CASE == "Mid-Left":
            x_zero = minx
            y_zero = midy
        elif   CASE == "Mid-Center":
            x_zero = midx
            y_zero = midy
        elif   CASE == "Mid-Right":
            x_zero = maxx
            y_zero = midy
        elif   CASE == "Bot-Left":
            x_zero = minx
            y_zero = miny
        elif   CASE == "Bot-Center":
            x_zero = midx
            y_zero = miny
        elif   CASE == "Bot-Right":
            x_zero = maxx
            y_zero = miny
        else:          #"Default"
            x_zero = minx
            y_zero = miny    
        
        axis_length = int(self.wim/4)

        PlotScale =  self.SCALE
        axis_x1 =  cszw/2 + (-x_zero             ) * PlotScale
        axis_x2 =  cszw/2 + ( axis_length-x_zero ) * PlotScale
        axis_y1 =  cszh/2 - (-y_zero             ) * PlotScale
        axis_y2 =  cszh/2 - ( axis_length-y_zero ) * PlotScale
        
        for seg in self.segID:
            self.PreviewCanvas.delete(seg)
        self.segID = []
        ##if self.show_axis.get() == True:
            # Plot coordinate system origin
            ##self.segID.append( self.PreviewCanvas.create_line(axis_x1,axis_y1, axis_x2,axis_y1, fill = 'red'  , width = 2))
            ##self.segID.append( self.PreviewCanvas.create_line(axis_x1,axis_y1, axis_x1,axis_y2, fill = 'green', width = 2))

            
    ##########################################################################            
    def donothing(self):
        #filewin = Toplevel(root)
        button = Button(self, text="Do nothing button")
        #quitButton = Button(self, text="Are you sure?", command=self.quit)
        button.pack() 

    ################################################################################
    #                         General Settings Window                              #
    ################################################################################
    def GEN_Settings_Window(self):
        gen_settings = Toplevel(width=460, height=350)
        gen_settings.grab_set() # Use grab_set to prevent user input in the main window during calculations
        gen_settings.resizable(0,0)
        gen_settings.title('Settings')
        #gen_settings.iconname("Settings")

        D_Yloc  = 6
        D_dY = 30
        xd_label_L = 12

        w_label=200
        w_entry=60
        w_units=60
        xd_entry_L=xd_label_L+w_label+10
        xd_units_L=xd_entry_L+w_entry+5

        #Radio Button
        D_Yloc=D_Yloc
        self.Label_Units = Label(gen_settings,text="Image Resize for Laser engraving")
        self.Label_Units.place(x=xd_label_L, y=D_Yloc, width=213, height=31)
        #self.Radio_Units_IN = Radiobutton(gen_settings,text="inch", value="in",
        #                                 width="100", anchor=W)
        #self.Radio_Units_IN.place(x=w_label+22, y=D_Yloc, width=75, height=23)
        #self.Radio_Units_IN.configure(variable=self.units )
        #self.Radio_Units_MM = Radiobutton(gen_settings,text="mm", value="mm",
        #                                 width="100", anchor=W)
        #self.Radio_Units_MM.place(x=w_label+110, y=D_Yloc, width=75, height=23)
        #self.Radio_Units_MM.configure(variable=self.units )
        #self.units.trace_variable("w", self.Entry_units_var_Callback)

	# set DPI
        D_Yloc=D_Yloc+D_dY
        self.Label_Tolerance = Label(gen_settings,text="DPI")
        self.Label_Tolerance.place(x=xd_label_L, y=D_Yloc, width=w_label, height=21)
        #self.Label_Tolerance_u = Label(gen_settings,textvariable=self.units, anchor=W)
        #self.Label_Tolerance_u.place(x=xd_units_L, y=D_Yloc, width=w_units, height=21)
        self.Entry_Tolerance = Entry(gen_settings,width="15")
        self.Entry_Tolerance.place(x=xd_entry_L, y=D_Yloc, width=w_entry, height=23)
        self.Entry_Tolerance.configure(textvariable=self.strXDPI)
        self.tolerance.trace_variable("w", self.Entry_Tolerance_Callback)
        self.entry_set(self.Entry_Tolerance,self.Entry_Tolerance_Check(),2)

	# set Image Size
	D_Yloc=D_Yloc+D_dY
	self.Label_Tolerance = Label(gen_settings,text="Image Size(width)")
	self.Label_Tolerance.place(x=xd_label_L, y=D_Yloc, width=w_label, height=21)
	self.Label_Tolerance_u = Label(gen_settings,text="mm", anchor=W)
	self.Label_Tolerance_u.place(x=xd_units_L, y=D_Yloc, width=w_units, height=21)
	self.Entry_Tolerance = Entry(gen_settings,width="15")
	self.Entry_Tolerance.place(x=xd_entry_L, y=D_Yloc, width=w_entry, height=23)
	self.Entry_Tolerance.configure(textvariable=self.strRaster_w_mm)
	self.tolerance.trace_variable("w", self.Entry_Tolerance_Callback)
	self.entry_set(self.Entry_Tolerance,self.Entry_Tolerance_Check(),2)
	
	# set Marking FeedRate
	D_Yloc=D_Yloc+D_dY
	self.Label_FeedRate = Label(gen_settings,text="Marking Feedrate(mm/min)")
	self.Label_FeedRate.place(x=xd_label_L, y=D_Yloc, width=w_label, height=21)
	self.Label_FeedRate_u = Label(gen_settings,text="mm/min", anchor=W)
	self.Label_FeedRate_u.place(x=xd_units_L, y=D_Yloc, width=w_units, height=21)
	self.Entry_FeedRate = Entry(gen_settings,width="15")
	self.Entry_FeedRate.place(x=xd_entry_L, y=D_Yloc, width=w_entry, height=23)
	self.Entry_FeedRate.configure(textvariable=self.strSPEED)
	#self.tolerance.trace_variable("w", self.Entry_Tolerance_Callback)
	#self.entry_set(self.Entry_Tolerance,self.Entry_Tolerance_Check(),2)

	# set Rapid move FeedRate
	D_Yloc=D_Yloc+D_dY
	self.Label_FeedRate = Label(gen_settings,text="Rapid move Feedrate(mm/min)")
	self.Label_FeedRate.place(x=xd_label_L, y=D_Yloc, width=w_label, height=21)
	self.Label_FeedRate_u = Label(gen_settings,text="mm/min", anchor=W)
	self.Label_FeedRate_u.place(x=xd_units_L, y=D_Yloc, width=w_units, height=21)
	self.Entry_FeedRate = Entry(gen_settings,width="15")
	self.Entry_FeedRate.place(x=xd_entry_L, y=D_Yloc, width=w_entry, height=23)
	self.Entry_FeedRate.configure(textvariable=self.strSPEED_rpd)
	#self.tolerance.trace_variable("w", self.Entry_Tolerance_Callback)
	#self.entry_set(self.Entry_Tolerance,self.Entry_Tolerance_Check(),2)


	# set Laser Strength Low/High Threshold
	D_Yloc=D_Yloc+D_dY
	self.Label_FeedRate = Label(gen_settings,text="Laser Strength Low Threshold")
	self.Label_FeedRate.place(x=xd_label_L, y=D_Yloc, width=w_label, height=21)
	self.Label_FeedRate_u = Label(gen_settings,text="", anchor=W)
	self.Label_FeedRate_u.place(x=xd_units_L, y=D_Yloc, width=w_units, height=21)
	self.Entry_FeedRate = Entry(gen_settings,width="15")
	self.Entry_FeedRate.place(x=xd_entry_L, y=D_Yloc, width=w_entry, height=23)
	self.Entry_FeedRate.configure(textvariable=self.strLaser_str_low)	

	D_Yloc=D_Yloc+D_dY
	self.Label_FeedRate = Label(gen_settings,text="Laser Strength High Threshold")
	self.Label_FeedRate.place(x=xd_label_L, y=D_Yloc, width=w_label, height=21)
	self.Label_FeedRate_u = Label(gen_settings,text="", anchor=W)
	self.Label_FeedRate_u.place(x=xd_units_L, y=D_Yloc, width=w_units, height=21)
	self.Entry_FeedRate = Entry(gen_settings,width="15")
	self.Entry_FeedRate.place(x=xd_entry_L, y=D_Yloc, width=w_entry, height=23)
	self.Entry_FeedRate.configure(textvariable=self.strLaser_str_high)		
	

        D_Yloc=D_Yloc+D_dY
        self.Label_Gpre = Label(gen_settings,text="G Code Header")
        self.Label_Gpre.place(x=xd_label_L, y=D_Yloc, width=w_label, height=21)
        self.Entry_Gpre = Entry(gen_settings,width="15")
        self.Entry_Gpre.place(x=xd_entry_L, y=D_Yloc, width=200, height=23)
        self.Entry_Gpre.configure(textvariable=self.gpre)

        D_Yloc=D_Yloc+D_dY
        self.Label_Gpost = Label(gen_settings,text="G Code Postscript")
        self.Label_Gpost.place(x=xd_label_L, y=D_Yloc, width=w_label, height=21)
        self.Entry_Gpost = Entry(gen_settings)
        self.Entry_Gpost.place(x=xd_entry_L, y=D_Yloc, width=200, height=23)
        #self.Entry_Gpost.configure(textvariable=self.gpost)
        
        #D_Yloc=D_Yloc+D_dY
        #self.Label_LaceBound = Label(gen_settings,text="Lace Bounding")
        #self.Label_LaceBound.place(x=xd_label_L, y=D_Yloc, width=w_label, height=21)
        #self.LaceBound_OptionMenu = OptionMenu(gen_settings, self.lace_bound, "None","Secondary","Full",\
        #                                       command=self.Set_Input_States_GEN_Event)
        #self.LaceBound_OptionMenu.place(x=xd_entry_L, y=D_Yloc, width=w_entry+40, height=23)

        #D_Yloc=D_Yloc+D_dY
        #self.Label_ContAngle = Label(gen_settings,text="LB Contact Angle")
        #self.Label_ContAngle.place(x=xd_label_L, y=D_Yloc, width=w_label, height=21)
        #self.Label_ContAngle_u = Label(gen_settings,text="deg", anchor=W)
        #self.Label_ContAngle_u.place(x=xd_units_L, y=D_Yloc, width=w_units, height=21)
        #self.Entry_ContAngle = Entry(gen_settings,width="15")
        #self.Entry_ContAngle.place(x=xd_entry_L, y=D_Yloc, width=w_entry, height=23)
        #self.Entry_ContAngle.configure(textvariable=self.cangle)
        #self.cangle.trace_variable("w", self.Entry_ContAngle_Callback)
        #self.entry_set(self.Entry_ContAngle,self.Entry_ContAngle_Check(),2)

        #Radio Button
        #D_Yloc=D_Yloc+D_dY
        #self.Label_SplitStep = Label(gen_settings,text="Offset Stepover")
        #self.Label_SplitStep.place(x=xd_label_L, y=D_Yloc, width=113, height=21)


        #self.Radio_SplitStep_N = Radiobutton(gen_settings,text="None", value="0",
        #                                 width="100", anchor=W)
        #self.Radio_SplitStep_N.place(x=w_label+22, y=D_Yloc, width=75, height=23)
        #self.Radio_SplitStep_N.configure(variable=self.splitstep )

        #self.Radio_SplitStep_H = Radiobutton(gen_settings,text="1/2 Step", value="0.5",
        #                                 width="100", anchor=W)
        #self.Radio_SplitStep_H.place(x=w_label+110, y=D_Yloc, width=75, height=23)
        #self.Radio_SplitStep_H.configure(variable=self.splitstep )

        #self.Radio_SplitStep_Q = Radiobutton(gen_settings,text="1/4 Step", value="0.25",
        #                                 width="100", anchor=W)
        #self.Radio_SplitStep_Q.place(x=w_label+198, y=D_Yloc, width=75, height=23)
        #self.Radio_SplitStep_Q.configure(variable=self.splitstep )



        #Radio Button
        #D_Yloc=D_Yloc+D_dY
        #self.Label_PlungeType = Label(gen_settings,text="Plunge Type")
        #self.Label_PlungeType.place(x=xd_label_L, y=D_Yloc, width=113, height=21)
        #self.Radio_PlungeType_S = Radiobutton(gen_settings,text="Vertical", value="simple",
        #                                 width="100", anchor=W)
        #self.Radio_PlungeType_S.place(x=w_label+22, y=D_Yloc, width=75, height=23)
        #self.Radio_PlungeType_S.configure(variable=self.plungetype )
        #self.Radio_PlungeType_A = Radiobutton(gen_settings,text="Arc", value="arc",
        #                                 width="100", anchor=W)
        #self.Radio_PlungeType_A.place(x=w_label+110, y=D_Yloc, width=75, height=23)
        #self.Radio_PlungeType_A.configure(variable=self.plungetype )

        ## Buttons ##
        gen_settings.update_idletasks()
        Ybut=int(gen_settings.winfo_height())-30
        Xbut=int(gen_settings.winfo_width()/2)

        self.GEN_Close = Button(gen_settings,text="Close",command=self.Close_Current_Window_Click)
        self.GEN_Close.place(x=Xbut, y=Ybut, width=130, height=30, anchor="center")

        #self.Set_Input_States_GEN()
        
        
    #############################
    def Entry_units_var_Callback(self, varName, index, mode):
        if self.units.get() == 'in':
            self.funits.set('in/min')
        else:
            self.funits.set('mm/min')    
            
    #############################
    def Entry_Tolerance_Check(self):
        try:
            value = float(self.tolerance.get())
            if  value <= 0.0:
                self.statusMessage.set(" Tolerance should be greater than 0 ")
                return 2 # Value is invalid number
        except:
            return 3     # Value not a number
        return 0         # Value is a valid number
    def Entry_Tolerance_Callback(self, varName, index, mode):
        self.entry_set(self.Entry_Tolerance,self.Entry_Tolerance_Check(), new=1)            
    
        
    #############################    
    def Set_Input_States(self):
        if self.tool.get() != "V":
            self.Label_Vangle.configure(state="disabled")
            self.Entry_Vangle.configure(state="disabled")
        else:
            self.Label_Vangle.configure(state="normal")
            self.Entry_Vangle.configure(state="normal")

        if self.cuttop.get():
            self.Entry_Toptol.configure(state="disabled")
            self.Label_Toptol.configure(state="disabled")
            self.Label_Toptol_u.configure(state="disabled")
        else:
            self.Entry_Toptol.configure(state="normal")
            self.Label_Toptol.configure(state="normal")
            self.Label_Toptol_u.configure(state="normal")

    ###############################################            
    def Set_Input_States_Event(self,event):
        self.Set_Input_States()

    ###############################################
    def Set_Input_States_GEN(self):
        if self.lace_bound.get() == "None":
            self.Label_ContAngle.configure(state="disabled")
            self.Entry_ContAngle.configure(state="disabled")
        else:
            self.Label_ContAngle.configure(state="normal")
            self.Entry_ContAngle.configure(state="normal")

        if ( self.scanpat.get().find("R") == -1) or \
           ( self.scanpat.get().find("C") == -1):
            self.Label_LaceBound.configure(state="disabled")
            self.LaceBound_OptionMenu.configure(state="disabled")
            self.Label_ContAngle.configure(state="disabled")
            self.Entry_ContAngle.configure(state="disabled")
        else:
            self.Label_LaceBound.configure(state="normal")
            self.LaceBound_OptionMenu.configure(state="normal")
            
    ###############################################
    def Set_Input_States_GEN_Event(self,event):
        self.Set_Input_States_GEN()
        
        
    ###############################################
    def Close_Current_Window_Click(self):
        win_id=self.grab_current()
        win_id.destroy()

    ###############################################
    def menu_Mode_Change(self):
        dummy_event = Event()
        dummy_event.widget=self.master
        self.Master_Configure(dummy_event,1)	
	
    ###############################################
    def bindConfigure(self, event):
        if not self.initComplete:
            self.initComplete = 1
            self.menu_Mode_Change()

    ###############################################
    def Master_Configure(self, event, update=0):
        if event.widget != self.master:
            return
        x = int(self.master.winfo_x())
        y = int(self.master.winfo_y())
        w = int(self.master.winfo_width())
        h = int(self.master.winfo_height())
        if (self.x, self.y) == (-1,-1):
            self.x, self.y = x,y
        if abs(self.w-w)>10 or abs(self.h-h)>10 or update==1:
            ###################################################
            #  Form changed Size (resized) adjust as required #
            ###################################################
            self.w=w
            self.h=h

            if 0 == 0:                
                # Left Column #
                w_label=90
                w_entry=60
                w_units=35

                x_label_L=10
                x_entry_L=x_label_L+w_label+10
                x_units_L=x_entry_L+w_entry+5

                Yloc=6
                self.Label_font_prop.place(x=x_label_L, y=Yloc, width=w_label*2, height=21)

                Yloc=Yloc+24
                self.Label_Yscale2.place(x=x_label_L, y=Yloc, width=w_label, height=21)
                self.Label_Yscale2_u.place(x=x_units_L, y=Yloc, width=w_units, height=21)
                self.Label_Yscale2_val.place(x=x_entry_L, y=Yloc, width=w_entry, height=21)

		Yloc=Yloc+24
		self.Label_Yscale.place(x=x_label_L, y=Yloc, width=w_label, height=21)
		self.Label_Yscale_u.place(x=x_units_L, y=Yloc, width=w_units, height=21)
		#self.Entry_Yscale.place(x=x_entry_L, y=Yloc, width=w_entry, height=23)
		self.Entry_Yscale_val.place(x=x_entry_L, y=Yloc, width=w_entry, height=23)
                
                Yloc=Yloc+24
                self.Label_PixSize.place(x=x_label_L, y=Yloc, width=w_label, height=21)
                self.Label_PixSize_u.place(x=x_units_L, y=Yloc, width=w_units, height=21)
                self.Label_PixSize_val.place(x=x_entry_L, y=Yloc, width=w_entry, height=21)

		###################  ########################
		if self.onConComplete == 1:
		    self.Label_pos_orient = Label(self.master,text="Converted Image Information:",\
				                              anchor=W)	
		    
		    self.separator1 = Frame(self.master, height=2, bd=1, relief=SUNKEN)
		    self.separator2 = Frame(self.master, height=2, bd=1, relief=SUNKEN)
		    self.separator3 = Frame(self.master, height=2, bd=1, relief=SUNKEN)
		    self.separator4 = Frame(self.master, height=2, bd=1, relief=SUNKEN)	
		    
		    self.Label_con_x_Scale = Label(self.master,text="Image Height", anchor=CENTER)
		    self.Label_con_x_Scale_u = Label(self.master,text="mm", anchor=W)
		    self.Label_con_x_Scale_val = Label(self.master, text=str(self.raster_mm_h), anchor=W)	
		    
		    self.Label_con_y_Scale = Label(self.master,text="Image width", anchor=CENTER)
		    self.Label_con_y_Scale_u = Label(self.master,text="mm", anchor=W)
		    self.Label_con_y_Scale_val = Label(self.master, text=str(self.raster_mm_w), anchor=W)	
		    
		    
		    self.Label_con_DPI = Label(self.master,text="DPI", anchor=CENTER)
		    self.Label_con_DPI_u = Label(self.master,text=" DPI", anchor=W)
		    self.Label_con_DPI_val = Label(self.master, textvariable=self.strXDPI, anchor=W)	

		    Yloc=Yloc+24+12
		    self.separator1.place(x=x_label_L, y=Yloc,width=w_label+75+40, height=2)
		    Yloc=Yloc+6
		    self.Label_pos_orient.place(x=x_label_L, y=Yloc, width=w_label*2, height=21)
              
		    Yloc=Yloc+24
		    self.Label_con_y_Scale.place(x=x_label_L, y=Yloc, width=w_label, height=21)
		    self.Label_con_y_Scale_u.place(x=x_units_L, y=Yloc, width=w_units, height=21)
		    self.Label_con_y_Scale_val.place(x=x_entry_L, y=Yloc, width=w_entry, height=21)                
                
		    Yloc=Yloc+24
		    self.Label_con_x_Scale.place(x=x_label_L, y=Yloc, width=w_label, height=21)
		    self.Label_con_x_Scale_u.place(x=x_units_L, y=Yloc, width=w_units, height=21)
		    self.Label_con_x_Scale_val.place(x=x_entry_L, y=Yloc, width=w_entry, height=21)                

		    Yloc=Yloc+24
		    self.Label_con_DPI.place(x=x_label_L, y=Yloc, width=w_label, height=21)
		    self.Label_con_DPI_u.place(x=x_units_L, y=Yloc, width=w_units, height=21)
		    self.Label_con_DPI_val.place(x=x_entry_L, y=Yloc, width=w_entry, height=21)                
                
		
                ## Start Right Column
		###########################################################################
                w_label=90
                w_entry=60
                w_units=35

                x_label_R=self.w - 220
                x_entry_R=x_label_R+w_label+10
                x_units_R=x_entry_R+w_entry+5

                #Yloc=6
                #self.Label_tool_opt.place(x=x_label_R, y=Yloc, width=w_label*2, height=21)

                #Yloc=Yloc+24
                #self.Label_ToolDIA.place(x=x_label_R,   y=Yloc, width=w_label, height=21)
                #self.Label_ToolDIA_u.place(x=x_units_R, y=Yloc, width=w_units, height=21)
                #self.Entry_ToolDIA.place(x=x_entry_R,   y=Yloc, width=w_entry, height=23)

                #Yloc=Yloc+24
                #self.Label_Tool.place(x=x_label_R, y=Yloc, width=w_label, height=21)
                #self.Tool_OptionMenu.place(x=x_entry_R, y=Yloc, width=w_entry+40, height=23)

                #Yloc=Yloc+24
                #self.Label_Vangle.place(x=x_label_R, y=Yloc, width=w_label, height=21)
                #self.Entry_Vangle.place(x=x_entry_R, y=Yloc, width=w_entry, height=23)
                
                #Yloc=Yloc+24+12
                #self.separator3.place(x=x_label_R, y=Yloc,width=w_label+75+40, height=2)

                #Yloc=Yloc+6
                #self.Label_gcode_opt.place(x=x_label_R, y=Yloc, width=w_label*2, height=21)

                #Yloc=Yloc+24
                #self.Label_Scanpat.place(x=x_label_R, y=Yloc, width=w_label, height=21)
                #self.ScanPat_OptionMenu.place(x=x_entry_R, y=Yloc, width=w_entry+40, height=23)

                #Yloc=Yloc+24
                #self.Label_CutPerim.place(x=x_label_R, y=Yloc, width=w_label, height=21)
                #self.Checkbutton_CutPerim.place(x=x_entry_R, y=Yloc, width=w_entry+40, height=23)
                
                #Yloc=Yloc+24
                #self.Label_Scandir.place(x=x_label_R, y=Yloc, width=w_label, height=21)
                #self.ScanDir_OptionMenu.place(x=x_entry_R, y=Yloc, width=w_entry+40, height=23)
                
                #Yloc=Yloc+24
                #self.Entry_Feed.place(  x=x_entry_R, y=Yloc, width=w_entry, height=23)
                #self.Label_Feed.place(  x=x_label_R, y=Yloc, width=w_label, height=21)
                #self.Label_Feed_u.place(x=x_units_R, y=Yloc, width=w_units+15, height=21)

                #Yloc=Yloc+24
                #self.Label_p_feed.place(x=x_label_R,  y=Yloc, width=w_label,   height=21)
                #self.Entry_p_feed.place(x=x_entry_R,  y=Yloc, width=w_entry,   height=23)
                #self.Label_p_feed_u.place(x=x_units_R,y=Yloc, width=w_units+15,height=21)

                #Yloc=Yloc+24
                #self.Label_StepOver.place(x=x_label_R, y=Yloc, width=w_label, height=21)
                #self.Label_StepOver_u.place(x=x_units_R, y=Yloc, width=w_units, height=21)
                #self.Entry_StepOver.place(x=x_entry_R, y=Yloc, width=w_entry, height=23)

                #Yloc=Yloc+24
                #self.Entry_Zsafe.place(  x=x_entry_R, y=Yloc, width=w_entry, height=23)
                #self.Label_Zsafe.place(  x=x_label_R, y=Yloc, width=w_label, height=21)
                #self.Label_Zsafe_u.place(x=x_units_R, y=Yloc, width=w_units, height=21)


                #Yloc=Yloc+24
                #self.Label_Zcut.place(  x=x_label_R, y=Yloc, width=w_label, height=21)
                #self.Label_Zcut_u.place(x=x_units_R, y=Yloc, width=w_units, height=21)
                #self.Entry_Zcut.place(  x=x_entry_R, y=Yloc, width=w_entry, height=23)

                #Yloc=Yloc+24+12
                #self.separator4.place(x=x_label_R, y=Yloc,width=w_label+75+40, height=2)

                # Buttons etc.
                #Yloc=Yloc+12
                #self.Roughing_but.place(x=x_label_R, y=Yloc, width=90+75+40, height=30)
        
                # Buttons etc.
                #Ybut=self.h-60
                #self.Save_Button.place(x=12, y=Ybut, width=95, height=30)

                #self.PreviewCanvas.configure( width = self.w-455, height = self.h-50 )
                #self.PreviewCanvas_frame.place(x=220, y=10)

                #self.Set_Input_States()
            self.Plot_Data()

    ###############################################
    ##*****************************************************************************************************        
    ##   Convert Image to gray scaled image 14.7.18
    ##     - preset parameter : XDPI/YDPI, raster_w, raster_h
    ##     - Save processed image as .png file   
    ##*****************************************************************************************************        
    def onConvert(self):
        # define parameters regarding to image conversion
        global image
        global image_conv
	
	self.onConComplete = 1
        
        laser_power = 30
        bidirectional_raster = False
        is_metric = True
        origin_x = 0
        origin_y = 0
        # center, <top|middle|bottom><left|center|right>
        origin_loc = 'topleft'
        # for mirroring
        mirror_x = False
        mirror_y = False
        # output raster Falsesize
        keep_aspect_ratio = True
     
     
        # system parameters
        output_optional_border = False
        distribute_bits_in_floats = False
        MAX_BPF = 53        
	
	self.XDPI =  float(self.strXDPI.get())
	self.YDPI = self.XDPI
        self.raster_w = float(self.strRaster_w_mm.get())/25.4
        
        # image scaling & conversion
        (img_w,img_h) = self.im.size
        self.gcode = ";(image size(pixel) w=" + str(img_w) +", h=" + str(img_h) +") \n"
        print('(image size(pixel) w=%u,h=%u)' % (img_w,img_h))
        
        self.gcode = self.gcode + ";(raster requested size w=" + str(self.raster_w) +" inch, h=" + str(self.raster_h) +" inch) \n"   
        print '(raster requested size w=%f, h=%f)' % (self.raster_w,self.raster_h)
        
        # adjust to aspect ratio
        raster_w_scaled_to_h = self.raster_h*float(img_w)/img_h
        raster_h_scaled_to_w = self.raster_w*float(img_h)/img_w
        
        if self.raster_w < 0 and self.raster_h < 0:
            # set size to be exactly input image
            # raster size unit : inch 
            self.raster_w = img_w/float(self.XDPI)
            self.raster_h = img_h/float(self.YDPI)
            pix_w = img_w
            pix_h = img_h
            W = self.raster_w
            H = self.raster_h
        else:
            # resize image according to request raster size w/h            
            if self.raster_w < 0:
                self.raster_w = raster_w_scaled_to_h
            elif self.raster_h < 0:
                self.raster_h = raster_h_scaled_to_w
            elif keep_aspect_ratio:
                if self.raster_w < raster_w_scaled_to_h:
                    self.raster_h = raster_h_scaled_to_w
                    self.gcode = self.gcode + ";(keep aspect ratio scaling h down to " + str(self.raster_h) +") \n"   
                    print '(keep aspect ratio scaling h down to %f)' % (self.raster_h)
                elif self.raster_h < raster_h_scaled_to_w:
                    self.raster_w = raster_w_scaled_to_h
                    self.gcode = self.gcode + ";(keep aspect ratio scaling w down to " + str(self.raster_w) +") \n"
                    print '(keep aspect ratio scaling w down to %f)' % (self.raster_w)
        
            # calc resized image size 
            pix_w = int(self.raster_w * self.XDPI)
            pix_h = int(self.raster_h * self.YDPI)
            W = float(pix_w) / self.XDPI
            H = float(pix_h) / self.YDPI
        
        # handle origin offsetting
        if ( origin_loc == 'center' ):
            X = origin_x - W/2.0
            Y = origin_y + H/2.0
        else:
            if ( 'top' in origin_loc ):
                Y = origin_y
            elif ( 'bottom' in origin_loc ):
                Y = origin_y + H
            elif ( 'middle' in origin_loc ):
                Y = origin_y + H/2.0
            else:
                print('unknown origin_loc='+origin_loc)
                sys.exit()
        
            if ( 'left' in origin_loc ):
                X = origin_x
            elif ( 'center' in origin_loc ):
                X = origin_x - W/2.0
            elif ( 'right' in origin_loc ):
                X = origin_x - W
            else:
                print('unknown origin_loc='+origin_loc)
                sys.exit()
        
        self.gcode = self.gcode + ";(raster upper right corner x= " + str(X) +", y= "+str(Y) + ") \n" 
        self.gcode = self.gcode + ";(raster calculated size w= " + str(W*25.4) +" mm, y= "+str(H*25.4) + " mm) \n"
        print '(raster upper right corner x=%f,y=%f)' % (X,Y)
        print '(raster calculated size w=%f mm,h=%f mm)' % (W*25.4,H*25.4)
        
        if img_w != pix_w or img_h != pix_h:
            self.gcode = self.gcode + ";(rescaling image to " + str(pix_w) +" pixels, y= "+str(pix_w) + " pixels) \n" 
            print '(rescaling image to %u,%u pixels)' % (pix_w, pix_h)
            self.im = self.im.resize((pix_w, pix_h), Image.BICUBIC)
        else:
            self.gcode = self.gcode + ";(keeping image size " + str(pix_w) +" pixels, y= "+str(pix_w) + " pixels) \n" 
            print '(keeping image size %u,%u pixels)' % (pix_w, pix_h)
            
        # #convert to grayscale image 
        #image_conv = image.convert("L") 
        image_conv = self.im
        #im.save('image_progress_grayscale.png')            
        #image = image.convert('1')
        
        if mirror_x:
            self.gcode = self.gcode + ";(flip image left to right)\n"
            print '(flip image left to right)'
            image_conv = image_conv.transpose(Image.FLIP_LEFT_RIGHT)
        if mirror_y:
            self.gcode = self.gcode + ";(flip image top to bottom)\n"
            print '(flip image top to bottom)'
            image_conv = image_conv.transpose(Image.FLIP_TOP_BOTTOM)
	    
	self.raster_mm_w = W*25.4
	self.raster_mm_h = H*25.4  	    
	    
        #openfilename = self.IMAGE_FILE
        self.openfilename, fileExtension = os.path.splitext(self.IMAGE_FILE)
        image_conv.save(self.openfilename + "_conv.png", "PNG") 
	
	self.menu_Mode_Change()
	self.statusMessage.set("Image Conversion Completed")
	self.statusbar.configure( bg = 'white' ) 	

    ##******************************************************************************* 
    ##  Generate G-code  from convered Imange 14.7.18
    ##   - Code from Image to Gcode 
    ##   - Laser TTL modulatoin value gets from each pixel value  
    ##   - Call gcode.py module for generate each pixel's movement and TTL value    
    ##*******************************************************************************
    def genGcode(self):
        global image_conv
        x, y = 0, 0
	d_prev = 0
	scale_low = 60
	scale_high = 200
        w, h = image_conv.size  # pixel unit from converted image
        
        fileGcode = open(self.openfilename+".gcode", "w")  # open file to save 

	self.SPEED = float(self.strSPEED.get())
	self.SPEED_rpd = float(self.strSPEED_rpd.get())
	self.Laser_str_low = float(self.strLaser_str_low.get())
	self.Laser_str_high = float(self.strLaser_str_high.get())	
	
	self.gcode = self.gcode + ";(Engraving Feedrate= " + str(self.SPEED) + " mm/min) \n" 
        self.gcode = self.gcode + ";(Rapid Feedrate= " + str(self.SPEED_rpd) + " mm/min) \n"
	self.gcode = self.gcode + ";(TTL Low Threshold= " + str(self.Laser_str_low) +") \n"
	self.gcode = self.gcode + ";(TTL High Threshold= " + str(self.Laser_str_high) +") \n"
        
                     
        step = (1.0/float(self.XDPI))*25.4 
        self.gcode = self.gcode + ";(Step size= " + str(step) + " mm) \n"       
        print '(Step size= %f mm)' % step
        
        #for line in self.gcode:
        #            fileGcode.write(line+'\n')
        fileGcode.write(self.gcode)
                    
        g = genGcode(safetyheight=0.02)
        tempGcode = g.begin()
        print tempGcode
        fileGcode.write(tempGcode+"\n")
        #print g.continuous()
        #print g.safety()
        tempGcode = g.rapid(0,0)
        print tempGcode
        fileGcode.write(tempGcode+"\n")
        
        scanLeft = 0
        for j in range(h-1,-1,-1):   # j means y coordinate 
            if scanLeft==1:   # generate jigjag motion from left to right and right to left  
                for i in range(w):  # i means x corrdinate, range W(width)
                    d = 255-(image_conv.getpixel((i, h-j-1)))   # getpixel : 0~254 grayscale value, # grayscale : white = 254, black = 0                                                         
                    #d = float(temp2 / 255.0) * depth - depth  #scaling 255 to engraving depth, "-" depth means high value is low cutting
		    #temp = float(d)/255.0
		    #d = ((scale_high-scale_low)*temp)+scale_low
		    
		    if d > self.Laser_str_high :
			d = self.Laser_str_high
		    if d < self.Laser_str_low :
			d = 0
		    
		    if d > self.Laser_str_low :
			if d_prev < self.Laser_str_low :
			    tempGcode = g.cut(x, y, d_prev, feed=self.SPEED_rpd) 
			    print tempGcode
			    fileGcode.write(tempGcode +"\n")
			else:
			    tempGcode = g.cut(x, y, d_prev, feed=self.SPEED) 
			    print tempGcode
			    fileGcode.write(tempGcode +"\n")
		    else:
			if d_prev > self.Laser_str_low :
			    tempGcode = g.cut(x, y, d_prev, feed=self.SPEED) 
			    print tempGcode
			    fileGcode.write(tempGcode +"\n")			    
		    
                    x -= step
		    d_prev = d
                    #end of for i (X rater odd number line)
                x += step
                scanLeft = 0
            else: 
                for i in range(w-1,-1,-1):
                    d = 255-(image_conv.getpixel((i, h-j-1)))
                    #d = float(temp1 / 255.0) * depth - depth     
		    #temp = float(d)/255.0
		    #d = ((scale_high-scale_low)*temp)+scale_low
		    
		    if d > self.Laser_str_high :
			d = self.Laser_str_high
		    if d < self.Laser_str_low :
			d = 0
			
		    if d > self.Laser_str_low :
			if d_prev < self.Laser_str_low :
			    tempGcode = g.cut(x, y, d_prev, feed=self.SPEED_rpd) 
			    print tempGcode
			    fileGcode.write(tempGcode +"\n")
			else:
			    tempGcode = g.cut(x, y, d_prev, feed=self.SPEED) 
			    print tempGcode
			    fileGcode.write(tempGcode +"\n")
		    else:
			if d_prev > self.Laser_str_low :
			    tempGcode = g.cut(x, y, d_prev, feed=self.SPEED) 
			    print tempGcode
			    fileGcode.write(tempGcode +"\n")			    
					    
                    x += step
		    d_prev = d
		    #end of for i (X rater even number line)
                x -= step
                scanLeft = 1 #end if scanleft
	    # end of rater line	
            y += step
            #tempGcode = g.cut(y=y)
            #print tempGcode
            #fileGcode.write(tempGcode+"\n")  #End j range For loop
        #Print Gcode End
        tempGcode = g.end()
        print tempGcode
        fileGcode.write(tempGcode+"\n")
        
        fileGcode.close()
	
	self.statusMessage.set("Gcode Generation Completed: %s" %(fileGcode))
	self.statusbar.configure( bg = 'white' ) 

    ##################################################################             
    def menu_File_Quit(self):
        if message_ask_ok_cancel("Exit", "Exiting...."):
            self.Quit_Click(None)
    

## gcode.py is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by the
## Free Software Foundation; either version 2 of the License, or (at your
## option) any later version.  gcode.py is distributed in the hope that it
## will be useful, but WITHOUT ANY WARRANTY; without even the implied
## warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
## the GNU General Public License for more details.  You should have
## received a copy of the GNU General Public License along with gcode.py; if
## not, write to the Free Software Foundation, Inc., 59 Temple Place,
## Suite 330, Boston, MA 02111-1307 USA
## 
## gcode.py is Copyright (C) 2005 Chris Radek
## chris@timeguy.com

class genGcode:
	lastx = lasty = lastz = lasta = lastgcode = None
	lastfeed = None

	def __init__(self, homeheight = 1.5, safetyheight = 0.04):
		self.homeheight = homeheight
		self.safetyheight = self.lastz = safetyheight

	def begin(self):
		return "G21 \n" + "G90 \n" + "G28 X0, Y0\n" + "M161  ;Laser Power On"

	def end(self):
		return self.safety() + "\n" + "M162  ;Laser power off\n"

	def exactpath(self):
		return "G61"

	def continuous(self):
		return "G64"

	def rapid(self, x = None, y = None, z = None, a = None, gcode = "G00", feed=None):
		gcodestring = feedstring = xstring = ystring = zstring = astring = ""
		if x == None: x = self.lastx
		if y == None: y = self.lasty
		if z == None: z = self.lastz
		if a == None: a = self.lasta
		#if gcode != self.lastgcode:
		gcodestring = gcode
		self.lastgcode = gcode
		#if x != self.lastx:
		xstring = " X%.4f" % (x)
		self.lastx = x
		#if y != self.lasty:
		ystring = " Y%.4f" % (y)
		self.lasty = y
		#if z != self.lastz:
		zstring = "  M160 S%d" % (z)
		self.lastz = z
		if a != self.lasta:
			astring = " A%.4f" % (a)
			self.lasta = a
		if gcode == "G01" and feed and feed != self.lastfeed:
			feedstring = " F%.4f" % (feed)
			self.lastfeed = feed
		#return gcodestring + feedstring + xstring + ystring + zstring + astring
		return gcodestring + xstring + ystring + feedstring + zstring 

	def cut(self, x = None, y = None, z = None, a = None, feed=None):
		if x == None: x = self.lastx
		if y == None: y = self.lasty
		if z == None: z = self.lastz
		if a == None: a = self.lasta
		return self.rapid(x, y, z, a, gcode="G01", feed=feed)

	def home(self):
		return self.rapid(z=self.homeheight)

	def safety(self):
		return self.rapid(z=self.safetyheight)

################################################################################
def message_ask_ok_cancel(title, mess):
    ##if VERSION == 3:
    ##result=tkinter.messagebox.askokcancel(title, mess)
    ##else:
    result=tkMessageBox.askokcancel(title, mess)
    return result

################################################################################
#                          Startup Application                                 #
################################################################################
##if NUMPY == True:
##    Image_Matrix = Image_Matrix_Numpy
##else:
##    Image_Matrix = Image_Matrix_List
    
root = Tk()
app = Application(root)
app.master.title("Image2gcode V"+version)
#app.master.iconname("dmap2gcode")
app.master.minsize(800,600)
root.mainloop()

    
       
    