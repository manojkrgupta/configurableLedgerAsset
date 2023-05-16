#!/usr/bin/env python3
import os
import sys
import math
import time
import json
import urllib3
import logging
import pyqrcode
import datetime
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
apiServer='https://localhost:8888/api/v1/flow'
apiServerAuth=('admin', 'admin')
nodes = {
        'Bob'       : {'x500': 'CN=Bob, OU=Test Dept, O=R3, L=London, C=GB'       , 'hash': '4774B43D1C81' },
        'Dave'      : {'x500': 'CN=Dave, OU=Test Dept, O=R3, L=London, C=GB'      , 'hash': '272937EA30B2' },
        'Alice'     : {'x500': 'CN=Alice, OU=Test Dept, O=R3, L=London, C=GB'     , 'hash': '45C63C50EA0B' },
        'NotaryRep1': {'x500': 'CN=NotaryRep1, OU=Test Dept, O=R3, L=London, C=GB', 'hash': 'D7F48A43D822' },
        'Charlie'   : {'x500': 'CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB'   , 'hash': 'DF47208EC301' }
        }

replace_maters_list = { 'API_SERVER': apiServer, 'PACKAGE': package}
def set_in_master_list(k, v): replace_maters_list[k] = v
steps=[
        {'name': 'IssueNewDocToDocServer',
         'post': 'DocIssuer', # 'https://localhost:8888/api/v1/flow/{{DocIssuer Bob 5204D03415E3}}'
         'request': {
             "clientRequestId": "__REQUEST_NUMBER__",
             "flowClassName": "com.r3.developers.v2docserver.workflows.IssueNewDocToDocServer",
             "requestData": {
                 "doc_path" : "/tmp/file_name",
                 "doc_owner": nodes['Dave']['x500'],  # "__DOC_OWNER__",
                 "doc_server": nodes['Alice']['x500'] # "__DOC_SERVER__"
                 }
             },
         'after_action': lambda res_json: set_in_master_list('DOC_ID', res_json['flowResult'])
         },
        {'name': 'IssueNewDocInformOwner',
         'post': 'DocIssuer', # 'url': '__API_SERVER__/__DOC_ISSUER__', # 'https://localhost:8888/api/v1/flow/{{DocIssuer Bob 5204D03415E3}}'
         'request': {
             "clientRequestId": "__REQUEST_NUMBER__",
             "flowClassName": "com.r3.developers.v2docserver.workflows.IssueNewDocInformOwner",
             "requestData": {
                 "doc_id" : "__DOC_ID__",
                 "doc_password" : "passwd",
                 "doc_owner": nodes['Dave']['x500'],  # "__DOC_OWNER__",
                 "doc_server": nodes['Alice']['x500'] # "__DOC_SERVER__"
                 }
             }
         },
        {'name': 'ListDocOwnerState',
         'post': 'DocOwner', # 'url' : '__API_SERVER__/__DOC_OWNER__', # 'https://localhost:8888/api/v1/flow/{{DocOwner Dave 3E9761F82115}}'
         'request':{
             "clientRequestId": "__REQUEST_NUMBER__",
             "flowClassName": "com.r3.developers.v2docserver.query.ListDocOwnerState",
             "requestData": {
                 }
             }
         },
        {'name': 'ListDocServerState',
         'post': 'DocServer', # 'url' : '__API_SERVER__/__DOC_SERVER__', # 'https://localhost:8888/api/v1/flow/{{DocServer Alice AA4F6A5FEBF1}}'
         'request': {
             "clientRequestId": "__REQUEST_NUMBER__",
             "flowClassName": "com.r3.developers.v2docserver.query.ListDocServerState",
             "requestData": {
                 }
             }
         }
        ]


# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
class Corda5:
  def __init__(s, apiServer=apiServer, apiServerAuth=apiServerAuth, nodes=nodes, replace_maters_list=replace_maters_list, level=logging.INFO, version=2):
    s.apiServer = apiServer
    s.apiServerAuth = apiServerAuth
    s.nodes = nodes
    s.replace_maters_list = replace_maters_list
    s.pid = os.getpid()
    s.get_log(level)
    s.version = version
    s.queryFlow = 'ListInstrument'
    checks = [
            {'func': s.test                            , 'args': list(),     'coverage': ['disk']},
           ]

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
          s.log_file_name="{}/log/{}.{}_{}.log".format(os.getenv('BaseDir'), os.path.basename(sys.argv[0]), time.strftime('%d%b%Y'), os.getpid())
        else:
          s.log_file_name="{}/log/{}.{}.log".format(os.getenv('BaseDir'), os.path.basename(sys.argv[0]), time.strftime('%d%b%Y'))
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
    url = '{}/{}/{}'.format(s.apiServer, s.nodes[node]['hash'], req_id)
    s.log.debug("Request type=get to url='{}'".format(url))
    res = requests.get(url, auth=apiServerAuth, verify=False)
    s.parse_res(res)
    return(req_id, res)

# ---------------------------------------------------------------------------------------------------
#
# "flowStatus": "COMPLETED", "RUNNING"
# ---------------------------------------------------------------------------------------------------
  def post(s, node, data, wait_for_completion=True):
    url  = '{}/{}'.format(s.apiServer, s.nodes[node]['hash'])
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
      df = s.query(n, query, False)
      s.log.info("Result for query={} from '{}/{}/{}'".format(query, n, s.nodes[n]['hash'], s.nodes[n]['x500']))
      display(df)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def query(s, node, query=None, show=False):
    query = query if query else s.queryFlow  
    s.log.debug("Running query={} on '{}/{}/{}'".format(query, node, s.nodes[node]['hash'], s.nodes[node]['x500']))
    queryRequest = {
                    "clientRequestId": "__REQUEST_NUMBER__",
                    "flowClassName": "__PACKAGE__.query.__QUERY__",
                    "requestBody": {}
              }
    s.replace_maters_list['QUERY'] = query
    (req, res, result) = s.post(node, queryRequest)
    (req, res) = s.get(node, req)
    res_json = res.json()
    state=res_json.get('flowStatus')
    df = None
    if state == 'COMPLETED':
      result_list = json.loads(res_json['flowResult'])
      df = pd.DataFrame(result_list)
      if show:
        s.log.info("Result for query={} from '{}/{}/{}'".format(query, node, s.nodes[node]['hash'], s.nodes[node]['x500']))  
        display(df)
    else:
      s.log.error("Failure while querying for '{}' from '{}/{}/{}' {}".format(query, node, s.nodes[node]['hash'], s.nodes[node]['x500'], res_json))
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
    s.replace_maters_list['TRANSFER_TO'] = s.nodes[to_node]['x500']
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
    s.actions['Issue']['requestBody']['to'] = s.nodes[to_node]['x500']
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
    s.log.info("Running action '{}' on '{}/{}/{}'".format(action, node, s.nodes[node]['hash'], s.nodes[node]['x500']))
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
    return(req, res, result)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def qr_code_for(s, owner, inst_id, query=None, show=True):
    query = query if query else s.queryFlow
    df = s.query(owner, query)
    tdf = df[df['id'] == inst_id]
    if len(tdf) != 1:
      s.log.error("data matching id='{}' in '{}' is of length='{}'. Expected length is exactly 1.".format(inst_id, owner, len(tdf)))
      return
    
    json_string = json.dumps(tdf.to_dict('records')[0])
    s.log.debug(json_string)

    encoded = pyqrcode.create(json_string)
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
    encoded = pyqrcode.create(json_string)
    encoded.png(qr_file, scale = 6)
    if show:
      img = mpimg.imread(qr_file)
      plt.imshow(img , cmap = 'gray')
    return(qr_file)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def print_to_pdf(s, owner, inst_id, query=None, show=False):
    html_file = '/tmp/report_{}.html'.format(inst_id)
    pdf_file = '/tmp/report_{}.pdf'.format(inst_id)
    query = query if query else s.queryFlow
    df = s.query(owner, query)
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
    return(pdf_file)

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def launch(s):
    print(s.nodes)
    print(s.replace_maters_list)
    print(steps)
    for req in steps:
      print("\n\n==================================================")
      print("Sending request = {}".format(req['name']))
      if 'post' in req:
        (req_id, res, result) = s.post(node=req['post'], data=req['request'], wait_for_completion=True)
        #(req_id, res) = s.get(node=req['post'], req_id=req_id)
        if 'after_action' in req:
          req['after_action'](res.json())
      if 'get'  in req:
        (req_id, res) = s.get(node=req['get'], req_id=req['req_id'])

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
  def start(s):
    length = len(checks)
    if s.any_one_function is not None and s.any_one_function.lower() in ('help', 'usage', '-h', '--help'):
      for i in range(length):
        log.warning("{}/{} function='{}'. Coverage={}.".format(i+1, length, checks[i]['func'].__name__,  checks[i]['coverage']))
      return()

    start_time = time.time()
    length = len(checks)
    for i in range(length):
      log.debug(checks[i]['func'].__name__)
      if s.any_one_function is None:
        if checks[i]['func'].__name__ in s.ignore_if_not_asked: continue
        args = checks[i]['args']
        log.warning("{}/{} starting check function='{}' with args='{}'. Coverage={}.".format(i+1, length, checks[i]['func'].__name__,  args, checks[i]['coverage']))
        step_time = time.time()
        got = checks[i]['func'](*args)
      elif s.any_one_function == checks[i]['func'].__name__:
        args = s.args
        log.warning("{}/{} starting check function='{}' with args='{}'. Coverage={}.".format(i+1, length, checks[i]['func'].__name__,  args, checks[i]['coverage']))
        step_time = time.time()
        got = checks[i]['func'](*args) # function argument is picked from command line
      else: continue
      if got is None: continue
      s.log.info(got)
      #log.info("{}/{} check function={} done in {} seconds. total time = {} seconds.".format(i+1, length, checks[i]['func'].__name__, round(time.time()-step_time,2), round(time.time() - start_time, 2)))

  def test(s):
    print(s.i.display_frp_table_nse(isin_list=['INE066F01012']))

def main():
  o = Test()
  o.launch()
  return(True)

if __name__ == "__main__":
  main()
  sys.exit(0)
