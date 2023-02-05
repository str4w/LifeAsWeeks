# -*- coding: utf-8 -*-
"""
Generate a diagram showing weeks of each year, for all the years in a range.
Inspired by  https://waitbutwhy.com/2014/05/life-weeks.html
"""

#!/usr/bin/env python

import math
import cairo
import datetime
import yaml
import sys


if not cairo.HAS_PDF_SURFACE:
    raise Exception('cairo was not compiled with PDF support')

def dow(y,m,d):
    return datetime.date(y,m,d).isoweekday()%7
def daysbetween(a,b):
    return (datetime.date(a[0],a[1],a[2])-datetime.date(b[0],b[1],b[2])).days

def draw_func(ctx,w,h,params):
    
    aspect=float(h)/w

    ctx.scale (min(w,h),min(w,h)) 
    margin=0.05
    if parameters["Title"]:
        top=margin*2
    else:
        top=margin
    bottom=aspect-margin
    grid=(0.05+margin,1.0-margin)
    startyear=parameters["StartDate"][0]
    verticalgap=0.003
    
    fontsize_year=0.01
    fontsize_title=0.025

    nbrows=parameters["NumberOfYears"]
    
    spans=[[(1973,1,1),(1973,2,20), (0.5,0.5,0.5)],
           [(1979,9,1),(1985,7,1),  (0.4,0.8,0.4)],
           [(1985,9,1),(1991,7,1),  (0.4,0.4,0.8)],
           [(1991,9,1),(1996,6,1),  (0.8,0.4,0.8)],
            ]

    cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
                        cairo.FONT_WEIGHT_BOLD)
                        
    if parameters["Title"]:
        cr.set_font_size(fontsize_title)
        ext=cr.text_extents(parameters["Title"])
        print (ext)
        ctx.move_to (0.5-ext[2]/2.,margin+margin/2. +ext[3]/2.)
        ctx.show_text(parameters["Title"])
        
    cr.set_font_size(fontsize_year)
    
    

    def faded():
        ctx.set_source_rgb (0.5, 0.5, 0.5) # Solid color
        ctx.set_line_width (0.001)
    def dark():
        ctx.set_source_rgb (0.0, 0.0, 0.0) # Solid color
        ctx.set_line_width (0.001)
    def month():
        ctx.set_source_rgb (0.8, 0.0, 0.0) # Solid color
        ctx.set_line_width (0.0005)

    def xpos(day):
        return grid[0]+(grid[1]-grid[0])*day/(54.*7)

    def rowcenter(y):
        totalheight=bottom-top+verticalgap
        perrow=totalheight/nbrows
        return top-verticalgap/2+perrow*(y+0.5)
    def rowheight():
        totalheight=bottom-top+verticalgap
        perrow=totalheight/nbrows
        return perrow-verticalgap
    
    def rowtop(y):
        return rowcenter(y)-rowheight()/2.

    def rowbottom(y):
        return rowcenter(y)+rowheight()/2.
    def getdayspan(year,span):
        start=datetime.date(span[0][0],span[0][1],span[0][2])
        end=datetime.date(span[1][0],span[1][1],span[1][2])
        ystart=datetime.date(year,1,1)
        yend=datetime.date(year+1,1,1)
        din=(start-ystart).days
        dend=(end-ystart).days
        dyr=(yend-ystart).days
        if dend<0 or din>dyr:
            return None
        else:
            return (max(din,0),min(dyr,dend))

    for y in range(0,nbrows):
        year=startyear+y
        startdow=0#dow(year,1,1)
        for s in spans:
            dayspan=getdayspan(year,s)
            if not dayspan is None:
                print ("Setting",s,"for year",year)
                print (dayspan)
                h0=rowtop(y) #top+(y-1)*(bottom-top)/nbrows
                h1=rowbottom(y) #top+y*(bottom-top)/nbrows
                x0=xpos(startdow+dayspan[0])
                x1=xpos(startdow+dayspan[1])
                ctx.rectangle (x0, h0, x1-x0, h1-h0)
                ctx.set_source_rgb(s[2][0],s[2][1],s[2][2])
                ctx.fill()




    faded()
    for y in range(0,nbrows):
        h0=rowtop(y) #top+(y-1)*(bottom-top)/nbrows
        h1=rowbottom(y) #top+y*(bottom-top)/nbrows
        #h1=top+y*(bottom-top)/nbrows
        ctx.move_to (grid[0], h0)
        ctx.line_to (grid[1], h0)
#        ctx.close_path ()
        ctx.stroke ()
        ctx.move_to (grid[0], h1)
        ctx.line_to (grid[1], h1)
#        ctx.close_path ()
        ctx.stroke ()
        for x in [grid[0],xpos(53*7),grid[1]]:
            ctx.move_to (x,  h0)
            ctx.line_to (x,  h1)
            ctx.stroke ()

    dark()
#    for w in range(1,53):
#        x0=xpos(w*7)
#        ctx.move_to (x0, top)
#        ctx.line_to (x0, bottom)
#        ctx.stroke ()
    for y in range(0,nbrows):
        dark()
        year=startyear+y
        startdow=0#dow(year,1,1)
        endday=startdow+daysbetween((year+1,1,1),(year,1,1))
        x0=xpos(startdow)
        x1=xpos(endday)
        h0=rowtop(y) #top+(y-1)*(bottom-top)/nbrows
        h1=rowbottom(y) #top+y*(bottom-top)/nbrows
        ctx.move_to (0.05,h1)
        ctx.show_text(str(year))
        ctx.move_to (x0, h0)
        ctx.line_to (x1, h0)
        ctx.stroke ()
        ctx.move_to (x0, h1)
        ctx.line_to (x1, h1)
        ctx.stroke ()
        ctx.move_to (x0, h0)
        ctx.line_to (x0, h1)
        ctx.stroke ()
        ctx.move_to (x1, h0)
        ctx.line_to (x1, h1)
        ctx.stroke ()
        for d in range(1,daysbetween((year+1,1,1),(year,1,1))):
            if (datetime.date(year,1,1)+datetime.timedelta(days=d)).weekday()==6:
                wday=startdow+d
                xw=xpos(wday)
                ctx.move_to (xw, h0)
                ctx.line_to (xw, h1)
                ctx.stroke ()
        month()
        for m in range(2,13):
            mday=startdow+daysbetween((year,m,1),(year,1,1))
            xm=xpos(mday)
            ctx.move_to (xm, h0)
            ctx.line_to (xm, h1)
            ctx.stroke ()
            
 #       ctx.close_path ()
 #       ctx.stroke ()


    #ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
    #ctx.set_line_width (0.02)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("Usage: LifeAsWeeks config.yml output.pdf")
    else:
        parameters=yaml.load(open(sys.argv[1]), Loader=yaml.SafeLoader)
        
        width_in_inches, height_in_inches = parameters["PaperSizeInInches"]
        width_in_points, height_in_points = width_in_inches * 72, height_in_inches * 72
        width, height = width_in_points, height_in_points
    
        surface = cairo.PDFSurface(sys.argv[2],width,height)
        cr = cairo.Context (surface)
        cr.save()
        draw_func(cr, width, height, parameters)
        cr.restore()
        cr.show_page()
        surface.finish()



