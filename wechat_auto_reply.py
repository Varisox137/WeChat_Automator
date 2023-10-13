from uiautomation import WindowControl,Logger
from json import loads as jl

# override to hide disable console output
# if not input('T ?'): print=lambda *_:None

wechat=WindowControl(Name='微信')
print('\nwechat window:\n  ',wechat)
wechat.SetTopmost(True)

dialog=wechat.ListControl(Name='会话')
print('\ndialog widget:\n  ',dialog)

conf_dict={}
try:
    with open('wechat_automation.json','r') as config:
        conf_dict=jl(config.read())
    assert ('shutdown' in conf_dict), ValueError('No shutdown settings found in json file !')
    shutdown_res=conf_dict['shutdown']
    assert len(shutdown_res)>=2, ValueError('Shutdown command or password not set !')
except FileNotFoundError as fnf:
    print(fnf)
    raise

LOGGING=conf_dict.get('logging',False)
PWD=conf_dict.get('password','confirm')
CHAR=conf_dict.get('spec_char','! ')
SEND=conf_dict.get('send','{Alt}s')
NOT_FOUND=conf_dict.get('not_found','N/A')

assert (not PWD.startswith(CHAR)), ValueError('Shutdown password should not begin with command spec_char !')

responses=conf_dict.get('responses',{})

if not LOGGING: Logger.SetLogFile('')

last_respond=''

while True:
    unread=dialog.TextControl(searchDepth=3)
    while not unread.Exists(maxSearchSeconds=3,searchIntervalSeconds=0): pass
    print('\nunread:\n  ',unread)

    if unread.Name:
        unread.Click(simulateMove=False)
        last_unread_msg=wechat.ListControl(Name='消息').GetChildren()[-1].Name
        print('\nlast unread msg:\n  ',last_unread_msg)
        if not last_unread_msg.startswith(CHAR):
            if last_respond==shutdown_res[1] and last_unread_msg==PWD:
                wechat.SendKeys('shutdown completed...'+SEND,waitTime=0)
                break
            del last_unread_msg
            continue

        # matching keywords
        res=responses[last_unread_msg[1:]] if last_unread_msg[1:] in responses\
            else shutdown_res[1] if last_unread_msg[1:]==shutdown_res[0] else NOT_FOUND

        wechat.SendKeys(res,waitTime=0)
        wechat.SendKeys(SEND,waitTime=0)
        last_respond=res

wechat.SetTopmost(False)
print('\nprogram shutdown......')
