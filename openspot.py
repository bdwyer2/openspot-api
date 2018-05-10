import requests, json, re, binascii, hashlib, sys

class OpenSpot():
  def __init__(self, hostname="openspot.local", password="openspot"):
    self.hostname = hostname
    self.password = password

    r = requests.post("http://" + self.hostname + "/gettok.cgi")
    tok = str(r.json()['token'])
    tok_pass = (tok + self.password).encode('utf-8')
    digest = hashlib.sha256(tok_pass).hexdigest()
    self.post = {'token': tok, 'digest': digest}
    login = requests.post("http://" + self.hostname + "/login.cgi", json=self.post)
    jwt = login.json()['jwt']
    self.headers = {"Authorization":"Bearer "+ jwt}

  def get_cwid(self):
    rcwid = requests.get("http://"+ self.hostname + "/modemcwid.cgi", json=self.post, headers=self.headers)
    return(rcwid.json())

  def get_nullsettings(self):
    rnullsettings = requests.get("http://"+ self.hostname + "/nullsettings.cgi", json=self.post, headers=self.headers)
    return(rnullsettings.json())

  def send_sms(self, dstid, srcid, message="hello", calltype=0, fmt=1, tdma_channel=0, modem=1):
    """spot.send_sms(srcid=3109883, dstid=1107812)"""
    encoded = binascii.hexlify(message.encode("utf-16be"))

    post ={"only_save": 0,
           "intercept_net_msgs": 0,
           "send_dstid": dstid,
           "send_calltype": calltype, # 0 = private / 1 = group
           "send_srcid": srcid,
           "send_format": fmt, # 0 = ETSI / 1 = UDP / 2 = UDP/Chinese
           "send_tdma_channel": tdma_channel,
           "send_to_modem": modem,
           "send_msg": encoded}

    output = requests.post("http://" + self.hostname + "/status-dmrsms.cgi", json=post, headers=self.headers)
    return(output)

