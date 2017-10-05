# aurorame.me
**THIS IS THE MOST IMPORTANT SECURITY STEP SO IF YOU DON'T READ ANY OF BELOW, PLEASE READ THIS. MAKE SURE YOU HIDE "website.db" FROM THE INTERNET.**
## So what is this?
This is the open source version of my uploadv2.php uploader I use for aurorame.me. It contains the SQLite3 DB for added setup speed too.
## Great! What are the system requirements for the setup I plan to run this on?
Great question! There are a few key things, but most VPS's/domain providers should suffice:
- I would suggest >10GB of free disk space. I personally use a 120GB virtual disk on my IIS VM.
- A web server which can server multiple directories, **can hide files** and supports PHP. I personally use IIS.
- I personally use PHP 7.0 but I have not tried anything lower. Your mileage may vary.
- Cloudflare. I would suggest using it for your site anyway due to its powerful firewall but you **must** use it for this project due to how IP logging is setup.
## What data is logged in the DB?
There are 2 tables:
- **keylist** - This is the one to be edited by the administrator. This contains the following. Please note you can remove all of the columns except dkey:
  - **discordid** - This contains the users Discord ID in case they need to be contacted.
  - **email** - This contains the users e-mail in case they need to be contacted.
  - **dkey** - This is the one column you cannot remove. This is the key that gets checked/logged when they upload. I use a randomly generated string for this.
- **uploadlog** - This is the table that is not intended to be edited:
  - **dkey** - This is the key specified above.
  - **filename** - The name of the file.
  - **ipaddr** - The IP address of the uploader.
## Lets get started. How do I go about setting this up?
1. Install http://sqlitebrowser.org/ to allow us to manage the DB.
2. Make a root directory for this project.
3. Enable the SQLite3 driver for PHP.
4. Put upload.php and website.db in this directory and created a directory called "i".
5. **Make sure website.db is hidden at this point.**
6. Make the root of your website point to the root of your directory.
7. make **i.*** (or whatever subdomain you want to use) point to `[directory root]/i`
8. Edit `$finaldir` in upload.php to your final upload domain. (If you used `i.*` it will be `https://i.[domain]/`)
9. Edit the ShareX template so that `INSERT_NAME_HERE` is the name of your project and `INSERT_URL_HERE` is your root domain.
10. Insert your own key into the table `keylist`.
11. Hope it all works :)
