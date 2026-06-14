TELEGRAM GROUP MEDIA DOWNLOADER
================================

WHAT THIS DOES:
Downloads all media files (photos, videos, documents, audio) from a Telegram group or channel that has "restrict content sharing" enabled.

REQUIREMENTS:
- Windows, Mac, or Linux computer
- Internet connection
- A Telegram account that is ALREADY a member of the target group

STEP 1: Install Python
- Go to https://www.python.org/downloads/
- Download and install Python (check "Add to PATH" on Windows)

STEP 2: Install Telethon
- Open Command Prompt (Windows) or Terminal (Mac/Linux)
- Type: pip install telethon
- Press Enter

STEP 3: Get Your API Credentials
- Go to https://my.telegram.org/apps
- Log in with your Telegram account
- Create a new application (any name, e.g. "Downloader")
- Copy your API ID and API Hash

STEP 4: Download the Script
- Save the script as telegram_downloader.py

STEP 5: Run the Script
- Open Command Prompt or Terminal
- Navigate to where you saved the script: cd Desktop
- Type: python telegram_downloader.py
- Press Enter

STEP 6: Follow the Prompts
- Enter your API ID
- Enter your API Hash
- Enter the group link (e.g., t.me/groupname or t.me/+InviteCode)
- Enter your phone number when asked (first time only)
- Enter the verification code sent to Telegram

The script will download all media files to a "downloads" folder.

NOTES:
- You must be a member of the group to download from it
- First run requires phone verification; subsequent runs do not
- The script works even if the group has "restrict saving content" enabled
- with that you can download contents that were activated seen this week or month 
