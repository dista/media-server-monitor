'''
Created on 2011-12-18

@author: dista
'''

import api.index
import UI.index
import web
import conf

urls = (
        "/mms/ui", UI.index.app,
        "/mms/api", api.index.app
        )


app = web.application(urls, locals())

if __name__ == "__main__":
    app.run()
