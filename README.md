<h3 align="center">automate-whatsapp-messages</h3>

> this is currently built only to _send_ whatsapp messages;

The project is using `selenium` to navigate through the [web.whatsapp.com](https://web.whatsapp.com/), with the help [keyboard shortcuts](https://faq.whatsapp.com/6204576529560565/?cms_platform=web) _automater_ can easily navigate through the whatsapp website.

listed below are the steps that needs to be taken to _send a message_:
1. login to `whatsapp` ( through QR code ) : 
	- To make sure we don't have to login to the `whatsapp` we can use profiles; I am using [firefox profiles](https://support.mozilla.org/en-US/kb/profile-manager-create-remove-switch-firefox-profiles); To create a new profile you can search `about:profiles` and select `creat a new profile`. 
	- After setting up a _new profile_, you can replace the `root-directory` of the `firefoxprofile = webdriver.FirefoxProfile(root-directory)`
2. create a new chat : `CTRL+SHIFT+N`
	- You can use actions to emulate this key combination `actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('n').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()`
2. type the contact name
3. type the message
4. press `ENTER`
5. close chat : `ESC`

