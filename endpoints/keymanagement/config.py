from endpoints.methods import dbmaker, Verfiy, Configparser
from flask import request

import sys
sys.dont_write_bytecode = True


def config():
    getsql = dbmaker()
    cur = getsql[0]
    con = getsql[1]



    confart = request.args.get('configart')
    if str(confart) == '' or str(confart) == 'None':
        argtext = {
            "Error": "configart is not defined",
            "Configarts": [
                "1. Change configuration",
                "2. Get configurations"
            ]
        }
        return argtext, 400

    if str(confart) == '1':
        masterkey = str(request.args.get('master_key'))
        getver = Verfiy.verifymasterkey(masterkey=masterkey)
        if getver[0]:
            return getver[1]



        dcid = str(request.args.get('dcid'))
        verdc = Verfiy.verifydc(dc=dcid)
        if verdc[0]:
            return verdc[1]

            
        getchangeart = request.args.get('changeart')
        if str(getchangeart) == '' or str(getchangeart) == 'None':
            invalidarg = {
                "Changeart not specified": [
                    "1. Set custom text",
                    "2. Set color",
                    "3. Set webhook"
                ]
            }
            return invalidarg, 400

        if str(getchangeart) == '1':
            gettext = str(request.args.get('customtext'))
            if str(gettext) == '' or str(gettext) == 'None':
                invalidarg = {
                    "Error": "you must have an custom text (customtext) as a argument"
                }   
                return invalidarg, 400
            

            cur.execute(f"UPDATE keys SET customtext='{str(gettext)}' WHERE dcid='{str(dcid)}'")
            con.commit()
            con.close()
            changetext = {
                "Status": "succesfull change settings"
            }
            return changetext, 200
            
        if str(getchangeart) == '2':
            getcolor = request.args.get('color')
            if str(getcolor) == '' or str(getcolor) == 'None':
                invalidarg = {
                    "Error": "you must have an color as a argument"
                }   
                return invalidarg, 400

            cur.execute(f"UPDATE keys SET color='{str(getcolor)}' WHERE dcid='{str(dcid)}'")
            con.commit()
            con.close()
            changetext = {
                "Status": "succesfull change settings"
            }
            return changetext, 200


        if str(getchangeart) == '3':
            getlogurl = request.args.get('log')
            if str(getlogurl) == '' or str(getlogurl) == 'None':
                invalidarg = {
                    "Error": "you must have an log (webhook url) as a argument"
                }   
                return invalidarg, 400

            cur.execute(f"UPDATE keys SET webhook='{str(getlogurl)}' WHERE dcid='{str(dcid)}'")
            con.commit()
            con.close()
            changetext = {
                "Status": "succesfull change settings"
            }
            return changetext, 200
        else:
            invalidarg = {
                "Error": f"invalid argument {getchangeart}"
            }
            return invalidarg, 400

    if str(confart) == '2':
        masterkey = str(request.args.get('master_key'))
        getver = Verfiy.verifymasterkey(masterkey=masterkey)
        if getver[0]:
            return getver[1]

        configart = str(request.args.get('lookconfigart'))
        if str(configart) == 'None' or configart == '':
            invalidarg = {
                "Configarts (lookconfigart)": [
                    "1 Get a specific configuration from a dcid",
                    "2 Get a specific configuration from a key",
                    "3 Get all configuration"
                ]
            }   
            return invalidarg, 400

        if configart == '1':
            dcid = str(request.args.get('dcid'))
            verdc = Verfiy.verifydc(dc=dcid)
            if verdc[0]:
                return verdc[1]
    

            geconfigs = cur.execute(f"SELECT dcid, key, dcid, customtext, color, webhook FROM keys WHERE dcid=('{dcid}')").fetchall()
            config = Configparser.showconfig(geconfigs)
            con.close()
            return config, 200


        if configart == '2':
            key = str(request.args.get('key'))
            getver = Verfiy.verifykey(key=key)
            if getver[0]:
                return getver[1]
    

            geconfigs = cur.execute(f"SELECT dcid, key, dcid, customtext, color, webhook FROM keys WHERE key=('{key}')").fetchall()
            config = Configparser.showconfig(geconfigs)
            con.close()
            return config, 200

        if configart == '3':
            geconfigs = cur.execute(f"SELECT dcid, key, dcid, customtext, color, webhook FROM keys").fetchall()
            config = geconfigs
            con.close()
            return config, 200

        else:
            invalidarg = {
                "Error: Invalid argument"
            }
            return invalidarg, 400