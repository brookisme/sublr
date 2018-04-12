from __future__ import print_function
import os
import re
import json
from glob import glob
import webbrowser as web
import sublr.config as c
from shutil import copyfile, move



def off(noisy=c.NOISY):
    """ disable remote
    """
    try:
        os.remove(c.CONFIG_PATH)
    except OSError:
        _print(c.NOT_ON,noisy,level="WARN")


def remove(ident,noisy=c.NOISY):
    """ remove remote config
    """
    file=c.REMOTE_CONFIG_PATH_TMPL.format(ident)
    try:
        os.remove(file)
        _print(c.REMOVED_TMPL.format(ident),noisy)
    except OSError:
        _print(c.FILE_DOES_NOT_EXIST_TMPL.format(file),noisy,level="WARN")


def init(ident,noisy=c.NOISY):
    """ initialize remote config
    """
    file=c.REMOTE_CONFIG_PATH_TMPL.format(ident)
    if os.path.exists(file):
        try:
            try:
                move(c.CONFIG_PATH,c.BAK_CONFIG_PATH)
            except IOError:
                _print(c.INITIAL_CONFIG,True)
            copyfile(file, c.CONFIG_PATH)
            _print(c.ON_TMPL.format(ident),noisy)
        except OSError:
            pass
    else:
        _print(c.FILE_DOES_NOT_EXIST_TMPL.format(file),True,level="ERROR")  


def open_port(port=c.DEFAULT_PORT,noisy=c.NOISY):
    """ open port for current remote in a web browser
    """
    with open(c.CONFIG_PATH, 'r') as f:
        cnfg=json.load(f)
    url=c.URL_TMPL.format(cnfg['host'],port)
    web.open_new_tab(url)
    _print(c.OPENED_TMPL.format(url),noisy)


def current():
    """ print current remote ident
    """
    try:
        with open(c.CONFIG_PATH, 'r') as f:
            cnfg=json.load(f)
        _print(c.WHO_TMPL.format(cnfg.get('sublr','unknown')),True)
    except IOError:
         _print(c.SUBL_OFF,True)



def create(ident,ip,remote_path=c.REMOTE_PATH,auto_init=c.AUTO_INIT,noisy=c.NOISY):
    """ create new remote sftp-config file

        Args:

            ident<str>: name used to identify sftp-config
            ip<str>:     
                - ip address for remote config
                - must be valid ip or include the string 'dev'
            remote_path<str>: path to the code-base on remote instance
            auto_init<bool>: if true initialize remote after creation


    """
    cnfg=c.CONFIG_DICT.copy()
    if re.match(c.IP_REGEX,ip) or re.search('dev',ip):
        cnfg['host']=ip
        cnfg['remote_path']=remote_path
        cnfg['sublr']=ident
        file=c.REMOTE_CONFIG_PATH_TMPL.format(ident)
        with open(file, 'w') as f:
            json.dump(cnfg,f,indent=4,sort_keys=True)
        if auto_init: 
            init(ident, noisy)
    else:
        _print(c.INVALID_IP_TMPL.format(ip),True,level="ERROR")


def list_remotes():
    """ list the idents for the available remote sftp-config files
    """
    selector=c.REMOTE_CONFIG_PATH_TMPL.format('*')
    root=c.REMOTE_CONFIG_PATH_TMPL.format('')
    files=glob(c.REMOTE_CONFIG_PATH_TMPL.format('*'))
    _print(c.AVAILABLE_REMOTES,True)
    for file in files:
        ident=file.replace(root,'')
        _print(c.AVAILABLE_REMOTE_TMPL.format(ident),True)




#
# HELPERS
#
def _print(msg,noisy,level='INFO'):
    if noisy:
        print("[{}] SUBLIME-REMOTE: {}".format(level,msg))


