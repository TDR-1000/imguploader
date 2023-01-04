from endpoints.methods import dbmaker, Verfiy
from flask import request
import requests

import sys
sys.dont_write_bytecode = True


def createkey():
    getsql = dbmaker()
    cur = getsql[0]
    con = getsql[1]

    masterkey = str(request.args.get('master_key'))
    getver = Verfiy.verifymasterkey(masterkey=masterkey)
    if getver[0]:
        return getver[1]

    dcid = str(request.args.get('dcid'))
    text = str(request.args.get('text'))
    ccolor = str(request.args.get('color'))
    log = str(request.args.get('log'))
    if str(dcid) == 'None' or dcid == '' or str(text) == '' or text == 'None' or str(ccolor) == 'None' or ccolor == '' or str(log) == 'None' or log == '':
        invalidarg = {
            "Error": "You must have an dcid, text, color or log as a argument"
        }   
        return invalidarg, 400

    getdcver = cur.execute(f"SELECT key FROM keys WHERE dcid=('{str(dcid)}')").fetchall()
    if str(getdcver) != '[]':
        con.close()
        invalidarg = {
            "Error": "The user have an api_key"
        }   
        return invalidarg, 200

    retries = 0
    try:
        makeapikey = requests.get('https://api.ghostboy.dev/passwd?psize=25').json()['Password']
    except:
        while retries < 10:
            try:
                makeapikey = requests.get('https://api.ghostboy.dev/passwd?psize=25').json()['Password']
            except:
                retries += 1

        if requests.get('https://api.ghostboy.dev/passwd?psize=1').status_code != 200:
            connectionres = {
                "Error": "Something wrent wrong with the connection to the api"
            }
            return connectionres, 500


    cur.execute("INSERT INTO keys(key, dcid, customtext, color, webhook) VALUES (?,?,?,?,?)",
                (makeapikey, dcid, text, ccolor, log))
    con.commit()

    getver = cur.execute(f"SELECT key FROM keys WHERE dcid=('{str(dcid)}')").fetchall()
    con.close()
    if getver == '[]':
        invalidarg = {
            "Error": "Something wrent wrong"
        }   
        return invalidarg, 500
    
    apikey = {
        "Apikey": str(makeapikey)
    }
    return apikey, 200