from endpoints.methods import Verfiy, dbmaker
from flask import request

import sys
sys.dont_write_bytecode = True



def get_images():
    getsql = dbmaker()
    cur = getsql[0]
    con = getsql[1]

    api_key = str(request.args.get('api_key'))
    verkey = Verfiy.verifykey(key=api_key)
    if verkey[0]:
        con.close()
        return verkey[1]

    masterkey = str(request.args.get('master_key'))
    getver = Verfiy.verifymasterkey(masterkey=masterkey)
    if getver[0]:
        return getver[1]
    
    
    get_key_images = cur.execute(f"SELECT imgname FROM keyupload WHERE key=('{str(api_key)}')").fetchall()
    if str(get_key_images)  == '[]':
        fetch_failed = {
            "Error": "No images found from this key"
        }
        return fetch_failed, 500
    
    all_images = {}
    counter = 0
    for image_name in get_key_images:
        counter += 1
        all_images.update(
            {
                f'Image{counter}': image_name
            }
        )
            
    return all_images, 200