from endpoints.methods import dbmaker, Verfiy
from flask import request

import sys
sys.dont_write_bytecode = True

def fetchkeys():
    getsql = dbmaker()
    cur = getsql[0]
    con = getsql[1]

    masterkey = str(request.args.get('master_key'))
    getver = Verfiy.verifymasterkey(masterkey=masterkey)
    if getver[0]:
        return getver[1]


    getallkeys = cur.execute(f"SELECT dcid FROM keys").fetchall()
    con.close()
    allkeys = {}
    counter = 0
    for key in getallkeys:
        counter += 1
        allkeys.update(
            {
                f'Key{counter}': key
            }
        )
    return allkeys, 200