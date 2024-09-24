<h3 align="center">automate-whatsapp-messages</h3>

> silly project that is currently built only to _send_ whatsapp messages;

The project is using `selenium` to navigate through the [web.whatsapp.com](https://web.whatsapp.com/), with the help [keyboard shortcuts](https://faq.whatsapp.com/6204576529560565/?cms_platform=web) _automater_ can easily navigate through the whatsapp website.

#### Basic Setup

you need to follow the steps listed below before running a script
1. login to `whatsapp` ( through QR code ) : 
	- To make sure we don't have to login to the `whatsapp` we can use profiles; I am using [firefox profiles](https://support.mozilla.org/en-US/kb/profile-manager-create-remove-switch-firefox-profiles); To create a new profile you can search `about:profiles` and select `create a new profile`. 
	- create a `env.py` file inside the `automator` and add the _line_ below
```python
FFPROFILE=r"<path-to-firefox-profile>"
```

---

#### Map Of Content

- [wa_status](automater/wa_status.py) : edit whatsapp status
- [wa_otm](automater/wa_otm.py) : send onetime message