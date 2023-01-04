from endpoints.methods import dbmaker, Verfiy
from flask import request

import sys
sys.dont_write_bytecode = True


def deletekey():
    getsql = dbmaker()
    cur = getsql[0]
    con = getsql[1]

    dcid = str(request.args.get('dcid'))
    verdc = Verfiy.verifydc(dc=dcid)
    if verdc[0]:
        return verdc[1]

    masterkey = str(request.args.get('master_key'))
    getver = Verfiy.verifymasterkey(masterkey=masterkey)
    if getver[0]:
        return getver[1]

    makeverdc = Verfiy.verifydc(dc=dcid)
    if makeverdc[0]:
        return makeverdc[1]

    cur.execute(f"DELETE FROM keys WHERE dcid='{str(dcid)}'")
    con.commit()
    con.close()

    delkeyres = {
        "Status": "Succesfull delete key"
    }   
    return delkeyres, 200