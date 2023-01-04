from endpoints.methods import dbmaker, Verfiy
from flask import request
import requests

import sys
sys.dont_write_bytecode = True

def reset():
    getsql = dbmaker()
    cur = getsql[0]
    con = getsql[1]

    masterkey = str(request.args.get('master_key'))
    getver = Verfiy.verifymasterkey(masterkey=masterkey)
    if getver[0]:
        return getver[1]

    dcid = str(request.args.get('dcid'))
    verdc = Verfiy.verifydc(dc=dcid)
    if verdc[0]:
        return verdc[1]

    try:
        makeapikey = requests.get('https://api.ghostboy.dev/passwd?psize=25').json()['Password']
    except:
        notdone = True
        while notdone:
            try:
                makeapikey = requests.get('https://api.ghostboy.dev/passwd?psize=25').json()['Password']
                notdone = False
            except:
                pass
    cur.execute(f"UPDATE keys SET key=('{str(makeapikey)}') WHERE dcid='{str(dcid)}'")
    con.commit()

    getver = cur.execute(f"SELECT key FROM keys WHERE dcid=('{str(dcid)}')").fetchall()
    con.close()
    delkeyres = {
        "Apikey": getver[0][0]
    }
    return delkeyres, 200