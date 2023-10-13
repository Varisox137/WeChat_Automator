# WeChat_Automator

##### Using the `uiautomator` library to control program window and auto reply, for WeChat on PC.



##### Program settings are in `wechat_automation.json` file, with the following keys and values:

Necessary :

- (list) `shutdown` : list of length 2+, with [0] as the shutdown trigger and [1] as the password input prompt

Recommended :

- (dict, default = `{}` ) `responses` : indicating the auto-reply keywords and responses

Optional :

- (bool, default = `False`) `logging` : whether to generate a log file (from the original `uiautomator.Logger`)
- (str, default = `'confirm'` ) `password` : the password to shutdown the program after auto-replied from trigger
- (str, default = `'! '` ) `spec_char` : the starting character(s) that indicates a command/auto-reply keyword
- (str, default = `'{Alt}s'` ) `send` : the hotkey(s) to send the auto-replied message
- (str, default = `'N/A'` ) `not_found` : the message to reply if no command/keyword matched

