from endpoints.methods import  dbmaker, getstats, website_icon, website_name, embed_description
from flask import render_template
from os.path import exists
import datetime
import os
from PIL import ImageColor

import sys
sys.dont_write_bytecode = True


def sender(imgfile):
    if imgfile == None:
        return render_template('invalid.html'), 400

    if exists(f'templates/images/{imgfile}') == False and exists(f'templates/images/{imgfile}.png') == False and exists(f'templates/images/{imgfile}.jpg') == False and exists(f'templates/images/{imgfile}.gif') == False and exists(f'templates/images/{imgfile}.mp4') == False:
        return render_template('invalid.html'), 400
    
    if exists(f'templates/images/{imgfile}') == False:
        if exists(f'templates/images/{imgfile}.png') != False:
            imgfile += '.png'
        if exists(f'templates/images/{imgfile}.jpg') != False:
            imgfile += '.jpg'
        if exists(f'templates/images/{imgfile}.gif') != False:
            imgfile += '.gif'
        if exists(f'templates/images/{imgfile}.mp4') != False:
            imgfile += '.mp4'

    getsql = dbmaker()
    cur = getsql[0]
    con = getsql[1]

    currentfile = str(imgfile).split('.')[0]
    
    getkey = cur.execute(f"SELECT key FROM keyupload WHERE imgname=('{currentfile}')").fetchall()
    if str(getkey) == '[]':
        imgtext = 'Uploaded to ghostboy.dev'
        color = '#2F4F4F'
    else:
        getconfig = cur.execute(f"SELECT customtext, color FROM keys WHERE key=('{str(getkey[0][0])}')").fetchall()
        customtext = getconfig[0][0]
        color = getconfig[0][1]
    con.close()




    imgstats = os.stat(f'templates/images/{imgfile}')
    filetime = datetime.datetime.fromtimestamp(imgstats.st_ctime, datetime.timezone(datetime.timedelta(hours=1))).strftime('%d.%m.%Y | %H:%M')

    filesize = getstats(imgstats.st_size)
    imgtext = f'{filetime} | {round(filesize[1], 3)} ({filesize[0]})'


    rgbcolor = ImageColor.getcolor(f'#{color}', 'RGB')
    if imgfile.endswith('.mp4'):
        return render_template('movie.html', imagename=imgfile, infotext=imgtext, color=color, uploadtext=customtext, rgbcolor1=rgbcolor[0], rgbcolor2=rgbcolor[1], rgbcolor3=rgbcolor[2], website_icon=website_icon, website_name=website_name, embed_description=embed_description)

    return render_template('img.html', imagename=imgfile, infotext=imgtext, color=color, uploadtext=customtext, rgbcolor1=rgbcolor[0], rgbcolor2=rgbcolor[1], rgbcolor3=rgbcolor[2], website_icon=website_icon, website_name=website_name, embed_description=embed_description)