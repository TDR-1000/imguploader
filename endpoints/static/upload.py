from endpoints.methods import dbmaker, log, filecleaner, getstats, domain, Verfiy
from flask import request
from threading import Thread
import datetime
import os
import random
from os.path import exists


import sys
sys.dont_write_bytecode = True


def uploader():
    getsql = dbmaker()
    cur = getsql[0]
    con = getsql[1]

    if request.method != 'POST':
        metherror = {
            "Error": "False method"
        }
        return metherror, 405


    api_key = str(request.args.get('api_key'))


    verkey = Verfiy.verifykey(key=api_key)
    if verkey[0]:
        con.close()
        return verkey[1]


    currentpath = f'{os.getcwd()}/templates/images'
    try:
        filereq = request.files['image']
        if filereq == 'None' or filereq == None:
            invalidarg = {
                "Error": "You must have an img in the request"
            }
            return invalidarg, 400
        
        if filereq.filename == 'image':
            filename = f'{filereq.filename}{str(random.randint(0, 1000))}.png'
        else:
            filename = filereq.filename 

        

        getcustomsettings = cur.execute(f"SELECT webhook, dcid FROM keys WHERE key=('{str(api_key)}')").fetchall()
        webhookurl = getcustomsettings[0][0]
        getdcid = getcustomsettings[0][1]
        dcid = f'<@{getdcid}> ({getdcid})'

        path = filename.split('.')[0]
        filetype = filename.split('.')[1]

        if exists(f'{currentpath}/{filename}'):
            exist = True
            while exist:
                newfilename = f'{path}{str(random.randint(0, 1000))}.{filetype}'

                imgfile = f'{currentpath}/{newfilename}'
                if not exists(imgfile):
                    filereq.save(imgfile)
                    filename = newfilename
                    path = newfilename.split('.')[0]
                    exist = False
                else:
                    pass
        else:
            imgfile = f'{currentpath}/{filename}'
            filereq.save(imgfile)

        cur.execute(f"INSERT INTO keyupload (key, imgname) VALUES (?, ?)", (api_key, imgfile.split('/')[-1].split('.')[0]))
        con.commit()
        con.close()

        imgstats = os.stat(imgfile)
        filetime = datetime.datetime.fromtimestamp(imgstats.st_ctime, datetime.timezone(datetime.timedelta(hours=1))).strftime('%d.%m.%Y | %H:%M')

        filesize = getstats(imgstats.st_size)
        imgtext = f'{filetime} | {round(filesize[1], 3)} ({filesize[0]})'
        connectip = request.headers.get('X-Forwarded-For').split(', ')[0]



        Thread(target=log, args=(connectip, api_key, webhookurl, imgtext, dcid, filename,)).start()
        Thread(target=filecleaner,).start()
        
        status = f"https://{domain}/{path}"

        return status, 200


    except Exception as e:
        errorres = {
            "Error": str(e)
        }
        return errorres, 500
