import requests, json, re, binascii, hashlib, sys

class OpenSpot():
  def __init__(self, hostname="openspot.local", password="openspot"):
    self.__hostname = hostname
    self.__password = password

    r = requests.post("http://" + self.__hostname + "/gettok.cgi")
    tok = str(r.json()['token'])
    tok_pass = (tok + self.__password).encode('utf-8')
    digest = hashlib.sha256(tok_pass).hexdigest()
    self.__post = {'token': tok, 'digest': digest}
    login = requests.post("http://" + self.__hostname + "/login.cgi", json=self.__post)
    jwt = login.json()['jwt']
    self.__headers = {"Authorization":"Bearer "+ jwt}

  def get_cwid(self):
    x = requests.get("http://" + self.__hostname + "/modemcwid.cgi", json=self.__post, headers=self.__headers)
    return(x.json())

  def get_nullsettings(self):
    x = requests.get("http://" + self.__hostname + "/nullsettings.cgi", json=self.__post, headers=self.__headers)
    return(x.json())

  def get_status(self):
    x = requests.get("http://" + self.__hostname + "/status.cgi", json=self.__post, headers=self.__headers)
    return(x.json())

  def get_sms_status(self):
    x = requests.get("http://" + self.__hostname + "/status-dmrsms.cgi", json=self.__post, headers=self.__headers)
    return(x.json())

  def get_ip_status(self):
    x = requests.get("http://" + self.__hostname + "/status-srfipconnserver.cgi", json=self.__post, headers=self.__headers)
    return(x.json())

  def get_homebrew_settings(self):
    x = requests.get("http://" + self.__hostname + "/homebrewsettings.cgi", json=self.__post, headers=self.__headers)
    return(x.json())

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

    output = requests.post("http://" + self.__hostname + "/status-dmrsms.cgi", json=post, headers=self.__headers)
    return(output)

  def reboot():
    pass
    #TODO


