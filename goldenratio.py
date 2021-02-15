#!/usr/bin/env python

#  -------------------------o-----------------------------------
#  Add layers with squares, circuls, spiral of golden ratio
#  and guidelines
#  Agregar capas de cuadrados, circulos, espiral de proporcion aurea
#  y lineas guias
#  -------------------------o-----------------------------------

from gimpfu import *
import math

def golden_ratio(img,layer,wdbrush,gldivis,showSpiral,showSquare,showCircles):
    pdb.gimp_message_set_handler(2)
    pdb.gimp_progress_init("Starting adding golden ratio layers...", None)
    currcontext = savecurrcontext()
    pdb.gimp_context_set_brush_size(wdbrush)
    #pdb.gimp_message(type(gldivis))
    #pdb.gimp_message(gldivis)
    prepar(img)
    phi = phiValue()
    grarray = ratiocalculation(img,wdbrush,phi)
    addguidelines(gldivis,img)
    if showSpiral:
        spiralgr(img,phi,wdbrush)
    if showCircles:
        circlelayers(grarray,img,wdbrush)
    if showSquare:
        squarelayers(grarray,img)
    restorecontext(currcontext)
    pdb.gimp_progress_set_text( "Golden ratio layers added OK")
    pdb.gimp_progress_end()

def savecurrcontext():
    currwbrush = pdb.gimp_context_get_brush_size()
    currforegr = pdb.gimp_context_get_foreground()
    currbackgr = pdb.gimp_context_get_background()
    return (currwbrush,currforegr,currbackgr)

def restorecontext(currvalues):
    #pdb.gimp_message(currvalues)
    pdb.gimp_context_set_brush_size(currvalues[0])
    pdb.gimp_context_set_foreground(currvalues[1])
    pdb.gimp_context_set_background(currvalues[2])

def prepar(currimg):
    pdb.gimp_progress_set_text("Verifying obsolete Golden Rate layers...")
    vergrl = [l for l in list(currimg.layers) if (("squaregr" in l.name) or ("circlegr" in l.name) or ("guidelinesgr" in l.name) or ("spiralgr" in l.name))]
    if vergrl != [] :
        cont = 0.0
        increment = 1.0/len(vergrl)
        while vergrl != []:
            pdb.gimp_progress_update(round(cont,2))
            line = "Previous Layer \"" + vergrl[0].name + "\" is deleted ... " +  str(round(cont*100,2)) + " %"
            pdb.gimp_progress_update(round(cont,2))
            cont += increment
            pdb.gimp_progress_set_text(line)
            pdb.gimp_image_remove_layer(currimg, vergrl[0])
            vergrl = [l for l in list(currimg.layers) if (("squaregr" in l.name) or ("circlegr" in l.name) or ("guidelinesgr" in l.name) or ("spiralgr" in l.name))]
        pdb.gimp_progress_set_text("Obsolete Golden Rate layers are deleted OK")
    else:
        pdb.gimp_progress_set_text("No obsolete Golden Rate layers were found")

def phiValue():
     return (1 + math.sqrt(5))/2.0

def ratiocalculation(currimg,wdbrush,phi):
    a = currimg.width
    if currimg.height > currimg.width :
        a = currimg.height
    b = 5*a
    limit = pow(wdbrush,4)
    grarray = [a]
    while a > limit and (b - a ) >  limit :
        b = a
        a = a*(phi-1.0)
        if b - a > limit :
            grarray.append(a)
    #pdb.gimp_message(grarray)
    pdb.gimp_progress_set_text("Array of golden ratio secuence is calculated OK...")
    return grarray

def ratiocalculation2(rwidth,rheight,phi):
    a = rwidth*1.0
    grarray = []
    if rheight > rwidth :
        a = rheight*1.0
    for n in range(7):
        a = a*(phi-1.0)
        grarray.append(a)
    #pdb.gimp_message(grarray)
    pdb.gimp_progress_set_text("Array of golden ratio secuence for spiral created OK...")
    return grarray

def addguidelines(gldivis,currimg):
    advperc = 0
    procname = "guidelinesgr"
    activity = "Adding Guides Lines"
    i = float(0)
    crosspoints = [i]
    div = int(gldivis)
    for num in range(div):
        i += 1.0/gldivis
        crosspoints.append(i)
    totallines = len(crosspoints)+6
    createnewlayer(procname,currimg)
    actvlayer = currimg.active_layer
    showadvance(round(advperc*100,2),activity)
    pdb.gimp_progress_update(advperc)
    for crosspoint in crosspoints:
        xaxis = crosspoint * float(actvlayer.width)
        yaxis = crosspoint * float(actvlayer.height)
        glcolorsqr(crosspoint)
        pdb.gimp_pencil(actvlayer,4,[0,yaxis,actvlayer.width,yaxis]) # horizontal lines
        pdb.gimp_pencil(actvlayer,4,[xaxis,0,xaxis,actvlayer.height]) # vertical lines
        advperc += 1.0/totallines
        pdb.gimp_progress_update(round(advperc,2))
        showadvance(round(advperc*100,2),activity)
    pdb.gimp_context_set_foreground("#FFC29B")
    crosspoints = [(0.0,0.0,1.0,1.0),(0.0,1.0,1.0,0.0),(0.5,0.0,1.0,0.5),(0.0,0.5,0.5,1.0),(0.5,0.0,0.0,0.5),(1.0,0.5,0.5,1.0)]
    # diagonal lines
    for crosspoint in crosspoints:
        x1 = crosspoint[0]*actvlayer.width
        y1 = crosspoint[1]*actvlayer.height
        x2 = crosspoint[2]*actvlayer.width
        y2 = crosspoint[3]*actvlayer.height
        pdb.gimp_pencil(actvlayer,4,[x1,y1,x2,y2])
        advperc += 1.0/totallines
        pdb.gimp_progress_update(round(advperc,2))
        showadvance(round(advperc*100,2),activity)
    actvlayer.flush()
    pdb.gimp_progress_set_text("GuideLines Layer added OK")

def createnewlayer(lname,currimg):
    typelayer = currimg.base_type
    modelayer = 28 # LAYER-MODE-NORMAL
    newlayer = pdb.gimp_layer_new(currimg,currimg.width,currimg.height,typelayer,lname,100,modelayer)
    pdb.gimp_layer_add_alpha(newlayer)
    typefill = 3 # FILL-TRANSPARENT
    pdb.gimp_drawable_fill(newlayer,typefill)
    pdb.gimp_image_insert_layer(currimg,newlayer,None,-1)
    currimg.active_layer = newlayer
    pdb.gimp_progress_set_text("Layer \"%s\" created OK" % (lname))

def createnewlayer2(lname,currimg,lwidth,lheight):
    typelayer = currimg.base_type
    modelayer = 28 # LAYER-MODE-NORMAL
    newlayer = pdb.gimp_layer_new(currimg,lwidth,lheight,typelayer,lname,100,modelayer)
    pdb.gimp_layer_add_alpha(newlayer)
    typefill = 3 # FILL-TRANSPARENT
    pdb.gimp_drawable_fill(newlayer,typefill)
    pdb.gimp_image_insert_layer(currimg,newlayer,None,-1)
    currimg.active_layer = newlayer
    pdb.gimp_progress_set_text("Layer \"%s\" created OK" % (lname))

def showadvance(quantity,procname):
    line = "Operation : \"" + str(procname) + "\" is " + str(quantity) + " % completed"
    pdb.gimp_progress_set_text(line)

def squarelayers(grarray,currimg):
    advperc = 0
    secsqur = 1
    increment = 1.0/float(len(grarray))
    activity = "Adding Squares Layers"
    pdb.gimp_context_set_foreground("#2ABB9B")
    for nlayer in grarray:
        procname = "squaregr" + str(secsqur)
        createnewlayer(procname,currimg)
        actvlayer = currimg.active_layer
        xbl = actvlayer.width/2 - nlayer/2 # x-point bottom-left 
        xbr = actvlayer.width/2 + nlayer/2 # x-point bottom-right 
        yta = actvlayer.height/2 - nlayer/2 # y-point top-above 
        ytd = actvlayer.height/2 + nlayer/2 # y-point top-downn 
        advperc += increment
        pdb.gimp_progress_update(round(advperc,2))
        showadvance(round(advperc*100,2),activity)
        pdb.gimp_pencil(actvlayer,10,[xbl,ytd,xbr,ytd,xbr,yta,xbl,yta,xbl,ytd]) 
        pdb.plug_in_autocrop_layer(currimg, actvlayer)
        secsqur += 1
        actvlayer.flush()
    pdb.gimp_progress_set_text("Layers of Squares are added OK")

def glcolorsqr(div):
    if div == 0.5:
        pdb.gimp_context_set_foreground("#C93756")
    elif div == 0.25 or div == 0.75:
          pdb.gimp_context_set_foreground("#39D5FF")
    else:
        pdb.gimp_context_set_foreground("#5EFCA1")

def circlelayers(grarray,currimg,wdbrush):
    advperc = 0
    secsqur = 1 
    increment = 1.0/float(len(grarray))
    opsel = 0 # CHANNEL-OP-ADD
    fillforegcolor = 0 # FILL-FOREGROUND
    activity = " Creation of Circles Layers"
    pdb.gimp_context_set_foreground("#E08A1E")
    for nlayer in grarray:
        procname = "circlegr" + str(secsqur)
        createnewlayer(procname,currimg)
        actvlayer = currimg.active_layer
        x = actvlayer.width/2 - nlayer/2.0
        y = actvlayer.height/2 - nlayer/2.0
        pdb.gimp_progress_update(round(advperc,2))
        showadvance(round(advperc*100,2),activity)
        pdb.gimp_image_select_ellipse(currimg,opsel,x,y,nlayer,nlayer)
        pdb.gimp_selection_border(currimg,wdbrush)
        pdb.gimp_drawable_edit_fill(actvlayer,fillforegcolor)
        pdb.gimp_selection_none(currimg)
        pdb.plug_in_autocrop_layer(currimg, actvlayer)
        advperc += increment
        secsqur += 1
        actvlayer.flush()
    pdb.gimp_progress_set_text("Layers of Circles are added OK")

def spiralgr(currimg,phi,wdbrush):
    pdb.gimp_context_set_brush_size(wdbrush*3)
    pdb.gimp_context_set_foreground("#F22613")
    procname = "spiralgr"
    grarray = ratiocalculation2(currimg.width,currimg.height,phi)
    if currimg.width > currimg.height:
        newwidth = grarray[0]+grarray[1]
        newheight = grarray[0]
        createnewlayer2(procname,currimg,newwidth,newheight)
    else:
        newwidth = grarray[0]
        newheight = grarray[0]+grarray[1]
        createnewlayer2(procname,currimg,newwidth,newheight)
    actvlayer = currimg.active_layer
    npoints = len(grarray)*90
    points = spiralpoints(npoints,actvlayer,grarray)
    spiraldraws(points,actvlayer)
    offx = (currimg.width - actvlayer.width) / 2
    offy = (currimg.height - actvlayer.height) / 2
    pdb.gimp_layer_set_offsets(actvlayer, offx, offy)
    pdb.gimp_progress_set_text("Spiral layer added OK")

def spiralpoints(npoints,actvlayer,grarray):
    activity = "Calculating Spiral points"
    advperc = 0.0
    increme = 1.0/npoints
    # formula spiral : radius(angle) = ae**(c*angle), c = ln(Phi)/90
    a = 0.0
    points = []
    valinit = definecenters(actvlayer,grarray)
    points = []
    for i,radius in enumerate(grarray):
        x0 = valinit[i][0]
        y0 = valinit[i][1]
        ag = valinit[i][2]
        for angle in range(ag,ag+91,1):
            x = x0 + radius*math.cos(math.radians(angle))
            y = y0 + radius*math.sin(math.radians(angle))
            points.append((x,y))
            pdb.gimp_progress_update(round(advperc,2))
            showadvance(round(advperc*100,2),activity)
            advperc += increme
    #pdb.gimp_message(points)
    return points

def definecenters(actvlayer,grarray):
    centerx = [grarray[0],grarray[0],actvlayer.width-grarray[2],actvlayer.width-grarray[2],grarray[0]+grarray[4],grarray[0]+grarray[4],actvlayer.width-grarray[2]-grarray[6]]
    centery = [grarray[0],grarray[1],grarray[1],actvlayer.height-grarray[3],actvlayer.height-grarray[3],grarray[1]+grarray[5],grarray[1]+grarray[5]]
    angle = [180,270,0,90,180,270,0]
    if actvlayer.height > actvlayer.width:
        centerx = [grarray[0],grarray[1],grarray[1],actvlayer.width-grarray[3],actvlayer.width-grarray[3],grarray[1]+grarray[5],grarray[1]+grarray[5]]
        centery = [grarray[1],grarray[1],grarray[2],grarray[2],grarray[2]+grarray[5],grarray[2]+grarray[5],grarray[2]+grarray[6]]
        angle = [90,180,270,0,90,180,270]
    centers = []
    for i in range(7):
        x = centerx[i]
        y = centery[i]
        a = angle[i]
        centers.append((x,y,a))
    return centers

def spiraldraws(points,actvlayer):
    advperc = 0
    estimstep = 1.0/len(points) # according to my points created
    activity = "Drawing Spiral"
    for point in points:
        x = point[0] 
        y = point[1]
        pdb.gimp_progress_update(round(advperc,2))
        showadvance(round(advperc*100,2),activity)
        pdb.gimp_pencil(actvlayer,2,[x,y])
        advperc += estimstep
        actvlayer.flush()

register(
    "python-fu-golden-rate",
    "Add Golden Ratio layers : squares, circles, spiral and guidelines",
    "Agregar capas de cuadrados, circulos, espirales en proporcion aurea y lineas guias, da error si agrego acentos",
    "Jeum",
    "Jeum",
    "31Jan2021",
    "Golden Ratio...",
    "",
    [
        (PF_IMAGE, "image",       "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_SLIDER, "brushwidth", "Brush width", 2.0, (2, 8, 0.1)),
        (PF_RADIO, "numdivision", "Axis divideb by ...", 2, (("2", 2),("4",4),("8",8))),
        (PF_TOGGLE, "addSpiral", "Add Spiral?", True),
        (PF_TOGGLE, "addSquares", "Add Squares?", True),
        (PF_TOGGLE, "addCircles", "Add Circles?", True),
    ],
    [],
    golden_ratio,
    menu="<Image>/Filters/Custom/"
)

main()
