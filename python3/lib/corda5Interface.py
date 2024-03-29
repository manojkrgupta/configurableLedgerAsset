#!/usr/bin/env python3
import os
import sys
import math
import time
import json
import urllib3
import logging
import pyqrcode
import datetime as dt
import requests
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
import matplotlib.image  as mpimg
from pprint     import pformat
from IPython.display import display
from pyhtml2pdf import converter
from IPython.core.display import HTML

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
package = 'com.r3.developers.configurableInstrument'
apiServer='https://corda-rest-worker/api/v1'
apiServerAuth=('admin', 'admin')
verifier_url = 'http://localhost:9009'

nodes = {
        'Authority' : 'CN=Authority, OU=Test Dept, O=R3, L=London, C=GB',
        'Bob'       : 'CN=Bob, OU=Test Dept, O=R3, L=London, C=GB',
        'Charlie'   : 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB',
        'Alice'     : 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB',
        'NotaryRep1': 'CN=NotaryRep1, OU=Test Dept, O=R3, L=London, C=GB',
        'Dave'      : 'CN=Dave, OU=Test Dept, O=R3, L=London, C=GB',
        }

replace_maters_list = { 'API_SERVER': apiServer, 'PACKAGE': package}
def set_in_master_list(k, v): replace_maters_list[k] = v

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
class Corda5:
  def __init__(s, apiServer=apiServer, apiServerAuth=apiServerAuth, nodes=nodes, replace_maters_list=replace_maters_list, level=logging.INFO, version=2, verifier_url=verifier_url):
    s.apiServer = apiServer
    s.apiServerAuth = apiServerAuth
    s.apiServerFlow='{}/flow'.format(s.apiServer)
    s.nodes = nodes
    s.verifier_url = verifier_url
    s.replace_maters_list = replace_maters_list
    s.pid = os.getpid()
    s.get_log(level)
    s.version = version
    s.queryFlow = 'ListInstrument'
    s.short_name = dict()
    for n in s.nodes:
      s.short_name[s.nodes[n]] = n
    s.warmup()

  def warmup(s):
    s.x500 = dict()
    res = requests.get('{}/virtualnode'.format(s.apiServer), auth=s.apiServerAuth, verify=False)
    s.parse_res(res)
    #print(res)
    if res.status_code == 200:
      for v in res.json()['virtualNodes']:
        s.x500[v['holdingIdentity']['x500Name']] = v['holdingIdentity']['shortHash']
        s.log.debug("{} {}".format(v['holdingIdentity']['x500Name'], v['holdingIdentity']['shortHash']))
    else:
      s.log.error("error while retreiving details of nodes. response code={}. response={}".format(res.status_code, res.json())) 
      return

  def message(s, text, h=4):
    message_format = {
                        3: '<h4 style="background-color:cyan;color:blue; font-family: monospace">{}</h4>',
#                         4: '<h4 style="background-color:#FAE5D3;color:Green; font-family: monospace;>{}</h4>',
#                         4: '<h4 style="color:Green; font-family: monospace">{}</h4>'
                        4: '<h4 style="color:blue; font-family: monospace">{}</h4>'
                     }
    message_format[None] = message_format[4]
    msg = message_format.get(h, message_format[None])
    if type(text) == list:
        for t in text:
            print(t, end="")
#             display(HTML(msg.format(t)))
    else:
#         print(text)
        display(HTML(msg.format(text)))

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def next_request_id(s): return('{}.{}'.format(s.pid, time.time()))

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def running_from_jupyter(t):
    return(True if os.environ.get('JPY_PARENT_PID') else False)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def get_log(s, level=logging.INFO):
    s.log = logging.getLogger(os.environ.get('LOGGER', 'study.root'))
    if s.log.hasHandlers(): return(s.log)
    if s.running_from_jupyter():
      s.log_file_name = 'jupyter_based_log_not_enabled'
      s.log_format = os.environ.get('STUDY_JUPYTER_LOG_FORMAT', " %(asctime)s | %(log_color)s%(levelname).1s%(reset)s | %(log_color)s%(message)s%(reset)s")
      from colorlog import ColoredFormatter
      formatter = ColoredFormatter(s.log_format, datefmt="%d-%m %H:%M:%S", reset=True, log_colors=dict(DEBUG='black', INFO='green', WARNING='yellow', ERROR='red', CRITICAL='red'))
      handler = logging.StreamHandler()
    elif (sys.argv[0] == '') or os.environ.get('STUDY_CONSOLE_LOG') not in (None, '0', 'False', 'false', False, 'no', 'No', 'None'):
      import coloredlogs
      s.log_format = os.environ.get('LOGGER_FORMAT', '%(asctime)s | %(levelname).1s | %(message)s')
      formatter = coloredlogs.ColoredFormatter(fmt=s.log_format, datefmt="%d-%m %H:%M:%S")
      handler = logging.StreamHandler(stream=sys.stdout)
    else:
      s.log_file_name = os.environ.get('LOGGER_FILE')
      if s.log_file_name is None:
        if os.environ.get('LOGGER_FILE_IGNORE_PID_IN_NAME', '').strip().lower() in ('', 'false', 'no', '0'):
          s.log_file_name="/log/{}.{}_{}.log".format(os.path.basename(sys.argv[0]), time.strftime('%d%b%Y'), os.getpid())
        else:
          s.log_file_name="/log/{}.{}.log".format(os.path.basename(sys.argv[0]), time.strftime('%d%b%Y'))
        os.environ['LOGGER_FILE'] = s.log_file_name
      s.log_format = os.environ.get('LOGGER_FORMAT', '%(asctime)s | %(levelname).1s | %(message)s')
      print("log file : {}".format(s.log_file_name))
      formatter = logging.Formatter(fmt=s.log_format, datefmt="%d-%m %H:%M:%S")
      handler = logging.FileHandler(s.log_file_name)
    s.log_level = int(os.environ.get('LOGGER_LEVEL', level))
    logging.root.setLevel(s.log_level)
    handler.setLevel(s.log_level)
    handler.setFormatter(formatter)
    s.log.setLevel(s.log_level)
    s.log.addHandler(handler)
    s.log.propagate = False
    return(s.log)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def replace(s, o):
    if type(o) == str:
      conversion_function = str
    else:   # for json object
      conversion_function = json.loads # str to obj ==> json.loads('{"a": "apple"}') ==> {'a': 'apple'}
      o = json.dumps(o)                # obj to str ==> json.dumps({'a': 'apple'}) ==> '{"a": "apple"}'

    for k in s.replace_maters_list:
      o = o.replace("__{}__".format(k), s.replace_maters_list[k])

    result = conversion_function(o)
    s.log.debug(result)
    return(result)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def parse_res(s, res):
    s.log.debug(res.status_code)
    s.log.debug(res.json())
    #print(res.text)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def get(s, node, req_id):
    url = '{}/{}/{}'.format(s.apiServerFlow, s.x500[s.nodes[node]], req_id)
    s.log.debug("Request type=get to url='{}'".format(url))
    res = requests.get(url, auth=apiServerAuth, verify=False)
    s.parse_res(res)
    return(req_id, res)

# ---------------------------------------------------------------------------------------------------
#
# "flowStatus": "COMPLETED", "RUNNING"
# ---------------------------------------------------------------------------------------------------
  def post(s, node, data, wait_for_completion=True):
    url  = '{}/{}'.format(s.apiServerFlow, s.x500[s.nodes[node]])
    req_id = s.next_request_id()
    s.replace_maters_list['REQUEST_NUMBER']  = req_id
    s.log.debug("Request type=post to url='{}'".format(url))
    s.log.debug("Original Request = {}".format(data))
    data = s.replace(data)
    s.log.debug("After filling values = {}".format(data))
    res = requests.post(url, data=json.dumps(data), auth=apiServerAuth, verify=False)
    s.parse_res(res)

    #if res.status_code != 200:
    #  return(req_id, res, res.json())

    result = None

    if wait_for_completion:
      state = 'RUNNING'
      while state == 'RUNNING':
        time.sleep(4)
        (ignore, res) = s.get(node=node, req_id=req_id)
        if res.status_code != 200:
          s.parse_res(res)
          state = 'FAILED'
        res_json = res.json()
        state=res_json.get('flowStatus')
        #if state != 'RUNNING':
        #  s.parse_res(res)
        if state == 'COMPLETED': result = res_json['flowResult']
        if state == 'FAILED': result = res_json['flowError']
        if state is None:
          state = 'FAILED'
          result = None
    else:
      (req_id, res) = s.get(node=node, req_id=req_id)
    return(req_id, res, result)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def query_all_nodes(s, query=None):
    query = query if query else s.queryFlow  
    for n in s.nodes:
      df = s.query(n, query, True)
      #s.log.info("Result for query={} from '{}/{}/{}'".format(query, n, s.x500[s.nodes[n]], s.nodes[n]))
      #display(df)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def query(s, node, query=None, show=False):
    query = query if query else s.queryFlow  
    s.log.debug("Running query={} on '{}/{}/{}'".format(query, node, s.x500[s.nodes[node]], s.nodes[node]))
    queryRequest = {
                    "clientRequestId": "__REQUEST_NUMBER__",
                    "flowClassName": "__PACKAGE__.query.__QUERY__",
                    "requestBody": {}
              }
    t1 = dt.datetime.now()
    s.replace_maters_list['QUERY'] = query
    (req, res, result) = s.post(node, queryRequest)
    (req, res) = s.get(node, req)
    res_json = res.json()
    state=res_json.get('flowStatus')
    t2 = dt.datetime.now()
    df = None
    if state == 'COMPLETED':
      result_list = json.loads(res_json['flowResult'])
      df = pd.DataFrame(result_list)
      if show:
        s.log.info("Result for query={} from '{}/{}/{}'. (Time taken={})".format(query, node, s.x500[s.nodes[node]], s.nodes[node], (t2-t1)))
        display(df)
    else:
      s.log.error("Failure while querying for '{}' from '{}/{}/{}' {}. (Time taken={})".format(query, node, s.x500[s.nodes[node]], s.nodes[node], res_json, (t2-t1)))
    return(df)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def transfer(s, inst_id, from_node, to_node, quantity=None):
    s.actions = {'Transfer':
                  { "clientRequestId": "__REQUEST_NUMBER__",
                    "flowClassName": "__PACKAGE__.workflows.Transfer",
                    "requestBody": {
                      "id": "__TRANSFER_ASSET_ID__", # "abadf72d-a7b1-43e2-a122-5749dffbee58",
                      "to": "__TRANSFER_TO__"
                    }
                  }
                }
    s.log.info("Tranfering instrument id '{}' to '{}'".format(inst_id, to_node))
    s.replace_maters_list['TRANSFER_ASSET_ID'] = inst_id
    s.replace_maters_list['TRANSFER_TO'] = s.nodes[to_node]
    if s.version > 1 and quantity: s.actions['Transfer']['requestBody']['quantity'] = quantity
    return(s.action(from_node, 'Transfer'))

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def issue(s, from_node, to_node, name, quantity=None, transferable=False, expiry=None, verifiable=True, attributes=None):
#    s.actions = {'Issue':
#                  { "clientRequestId": "__REQUEST_NUMBER__",
#                    "flowClassName": "__PACKAGE__.workflows.Issue",
#                    "requestBody": {
#                          "name" : "__ISSUE_NAME__",
#                          "to": "__ISSUE_TO__", #"CN=Alice, OU=Test Dept, O=R3, L=London, C=GB",
#                          "transferable": "__TRANSFERABLE__", # false
#                          "expiry"      : "__EXPIRY__", # 
#                          "attributes": { 
#                                "__ATTRIBUTES__"  #"college": "Apple Collage", #"university": "Apple"
#                          }
#                    }
#                  }
#               }
    s.log.info("Issuing instrument='{}' to '{}'".format(name, to_node))
    s.actions = {'Issue':
                  { "clientRequestId": "__REQUEST_NUMBER__",
                    "flowClassName": "__PACKAGE__.workflows.Issue",
                    "requestBody": {
                    }
                  }
               }
    s.actions['Issue']['requestBody']['name'] = name
    s.actions['Issue']['requestBody']['to'] = s.nodes[to_node]
    s.actions['Issue']['requestBody']['transferable'] = 'true' if transferable else 'false'
    if s.version > 1 : s.actions['Issue']['requestBody']['verifiable'] = 'true' if verifiable else 'false'
    if s.version > 1 and quantity: s.actions['Issue']['requestBody']['quantity'] = quantity
    if expiry: s.actions['Issue']['requestBody']['expiry'] = expiry 
    if attributes: s.actions['Issue']['requestBody']['attributes'] = attributes

    return(s.action(from_node, 'Issue'))

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def redeem(s, inst_id, from_node, quantity=None):
    s.actions = {'Redeem':
                  { "clientRequestId": "__REQUEST_NUMBER__",
                    "flowClassName": "__PACKAGE__.workflows.Redeem",
                    "requestBody": {
                      "id": "__REDEEM_ASSET_ID__", # "abadf72d-a7b1-43e2-a122-5749dffbee58",
                    }
                  }
                }
    s.log.info("Redeeming instrument id '{}' quantity '{}'".format(inst_id, quantity))
    s.replace_maters_list['REDEEM_ASSET_ID'] = inst_id
    if s.version > 1 and quantity: s.actions['Redeem']['requestBody']['quantity'] = quantity
    return(s.action(from_node, 'Redeem'))

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def action(s, node, action):
    s.log.info("Running action '{}' on '{}/{}/{}'".format(action, node, s.x500[s.nodes[node]], s.nodes[node]))
    t1 = dt.datetime.now()
    (req, res, result) = s.post(node, s.actions[action])
    #(req, res) = s.get(node, req)
    if res.status_code != 200:
      s.log.error("Failure detected {}".format(result))  
      return(req, res, res.json())
    res_json = res.json()
    state=res_json.get('flowStatus')
    if state == 'COMPLETED':
      #result = res_json['flowResult']
      #result_list = json.loads(result)
      s.log.info(result)
    if state == 'FAILED':
      #result = res_json['flowError']
      s.log.info(result)
    if state is None:
      state = 'FAILED'
      result = None
    t2 = dt.datetime.now()
    s.log.info("Time taken = {}".format(t2-t1))
    return(req, res, result)


  def verifier(s, data, query=None):
    query = query if query else s.queryFlow
    df = s.query(s.short_name[data['issuer']], query)
    if len(df) < 1:
      s.log.error("No data on '{}'".format(data['issuer']))
      return
    tdf = df[(df['name'] == data['name']) & (df['owner'] == data['owner'])]
    if len(tdf) < 1:
      s.log.error("no data matching name='{}', owner='{}'".format(data['name'], data['owner']))
      return

    #if   data['transferable'].lower() == 'true': data['transferable']=True
    #elif data['transferable'].lower() == 'false': data['transferable']=False
    #else: data['transferable']=None

    #if   data['verifiable'].lower() == 'true': data['verifiable']=True
    #elif data['verifiable'].lower() == 'false': data['verifiable']=False
    #else: data['verifiable']=None

#{"name": "Government Bond 2024", "owner": "CN=Alice, OU=Test Dept, O=R3, L=London, C=GB", "issuer": "CN=Authority, OU=Test Dept, O=R3, L=London, C=GB", "quantity": 10, "transferable": true, "expiry": null, "verifiable": true, "attributes": {"payments": "['10Jun2023', '10Sep2023', '10Dec2023', '10Mar2024']"}}
    total_quantity_found = 0

    for (i,row) in df.iterrows():
      if row['transferable'] == data['transferable']:
        if row['expiry'] == data['expiry']:
          if row['verifiable'] == data['verifiable']:
            if data['quantity'] is None: 
              s.log.info("verify success {} {}".format(data, row))  
              return True
            else:
              total_quantity_found = total_quantity_found + row['quantity']  
              if total_quantity_found >= data['quantity']:
                s.log.info("verify success {} {}, total found so far={}".format(data, row.to_dict(), total_quantity_found))
                return True
              else:
                s.log.info("verify progress {} {}, total found so far={}".format(data, row.to_dict(), total_quantity_found))
        
    return(False)  



# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def qr_code_for(s, owner, inst_id, query=None, show=True):
    query = query if query else s.queryFlow
    df = s.query(owner, query)
    if len(df) < 1:
      s.log.error("No data matching id='{}' in '{}'".format(inst_id, owner))
      return
    tdf = df[df['id'] == inst_id]
    if len(tdf) != 1:
      s.log.error("data matching id='{}' in '{}' is of length='{}'. Expected length is exactly 1.".format(inst_id, owner, len(tdf)))
      return
    
    json_string = json.dumps(tdf.to_dict('records')[0])
    s.log.debug(json_string)
    s.log.info('{}?data={}'.format(s.verifier_url, json_string))
    encoded = pyqrcode.create('{}?data={}'.format(s.verifier_url, json_string))
    encoded.png('/tmp/myqr.png', scale = 3)
    img = mpimg.imread('/tmp/myqr.png')
    if show:
      plt.imshow(img , cmap = 'gray')
    return(img)  

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def qr_code(s, inst_id, json_string, show=False):
    qr_file= '/tmp/qr_{}.png'.format(inst_id)
    s.log.info('{}?data={}'.format(s.verifier_url, json_string))
    encoded = pyqrcode.create('{}?data={}'.format(s.verifier_url, json_string))
    #encoded = pyqrcode.create(json_string)
    encoded.png(qr_file, scale = 6)
    if show:
      img = mpimg.imread(qr_file)
      plt.imshow(img , cmap = 'gray')
    return(qr_file)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def print_to_pdf(s, owner, inst_id, query=None, show=False):
    t1 = dt.datetime.now()
    html_file = '/tmp/report_{}.html'.format(inst_id)
    pdf_file = '/tmp/report_{}.pdf'.format(inst_id)
    query = query if query else s.queryFlow
    df = s.query(owner, query)
    if len(df) < 1:
      s.log.error("No data matching id='{}' in '{}'".format(inst_id, owner))
      return

    tdf = df[df['id'] == inst_id]
    if len(tdf) != 1:
      s.log.error("data matching id='{}' in '{}' is of length='{}'. Expected length is exactly 1.".format(inst_id, owner, len(tdf)))
      return
    del(tdf['id']) # we don't need to show id

    tdf_dict = tdf.to_dict('records')[0]
    #display(tdf_dict)
    if tdf_dict['verifiable'] not in (True, 'true', 'True'):
        s.log.error("instrument id='{}' is not verifiable".format(inst_id))
        return None

    json_string = json.dumps(tdf_dict)
    s.log.debug(json_string)
    qr_file = s.qr_code(inst_id, json_string, show=False)

    table_html = tdf.transpose().to_html(header=False)
    f = open(html_file, 'w')
    # to align table to center -- style="margin-left: auto; margin-right: auto;"
    html_text = """<html>
    <head>__HEADER__</head>
    <body align="center">
    <br>
    <center>
      __TABLE__
    </center>
    <br>
    <img src="__QRFILE__" width="200" height="200">
    </body>
    </html>"""
    html_text = html_text.replace('__HEADER__', tdf_dict['name'])
    html_text = html_text.replace('__TABLE__' , table_html)
    html_text = html_text.replace('__QRFILE__', qr_file)
    f.write(html_text)
    f.close()
    html_file_path = os.path.abspath(html_file)
    converter.convert(f'file:///{html_file_path}', pdf_file)
    if show:
      display(HTML(html_text))
      #webbrowser.open("file:///{}".format(html_file_path))
    t2 = dt.datetime.now()  
    s.log.info("Time taken = {}".format(t2-t1))
    return(pdf_file)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
def main():
  return(True)

if __name__ == "__main__":
  main()
  sys.exit(0)
