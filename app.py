# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

dict={  123456 : "Your Query against 123456 was in Progress. You will get a reply from customer once our team resolved this",123457 : "Your Query against 123457 was Cancelled", 123458 : "Your Query against 123458 was moved to our technical team. it will be resolved in 12 hour",  123459 : "Your Query against 123459 was pending",  123455 : "Your Query against 123455 was cancelled by our administrator contact them by mail:aaa@cs.com or 9876543210"}
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request--Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print('response is {}'.format(res))
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    print ('Goes Fine')
    print (req.get("result").get("action"))
    if req.get("result").get("action") != "Query.Ticket":
        #print ('Entered Wrong way')
        return {}

    ticket_id = req.get("result").get("parameters").get("number-integer")[0]
    #print ('1--{}'.format(ticket_id))
    if ticket_id in dict:
        data=dict[ticket_id]
    else:
        data='Your Ticket ID is not in our DB. Please contact our Customer care executive in Mail:aaa@cs.com or in Mobile:9876543210'
    #print('data is {}'.format(data))
    #print (data)
    res = makeWebhookResult(data)
    return res

def makeWebhookResult(data):
    print ('Entered makewebhook result')
    speech = data
    print("Response:")
    print(speech)

    return {"speech": speech, "displayText": speech}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
