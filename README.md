<h1 align="center">Welcome to Telegram Advert Bot 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000" />
  <a href="#" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/code\_fredy" target="_blank">
    <img alt="Twitter: code\_fredy" src="https://img.shields.io/twitter/follow/code\_fredy.svg?style=social" />
  </a>
</p>

### 🏠 Project Biography

The importance of marketing has always been inevitable to neglect for growing businesses seeking to reach more of it's target users. This telegram application seeks to meet the goal of share vital content to members of specified target groups/channels (excluding the registered administrators of that group). In addition to that, each of the sent messages are recorded and by default, deleted aftered two(2) hours to protect which ever account the user uses, from ban.

From the perspective of a user trying to market his/her services or products, this bot would go a long way without you having to worry about engaging with users individually. And when a user finds the content interesting, you receive a feedback which gives the user a call to action right away with their first customer.

For group owners/admins, this bot can serve an a direct broadcaster of important or urgent information straight to the members of the group. This prevent you from worrying about who has seen the message on the group or not, because they have all received it individually.

## Installation

```sh
pip3 install -r requirements.txt
```

<!-- USAGE EXAMPLES -->
## Usage

To use this application as your own, follow these simple steps;

  - Fork this repository (`git clone https://github.com/Pycomet/telegram-group-engagement-bot.git`)

  - Create a `.env` file with the following data
    - `TOKEN` - This is the telegram bot token from `@botfather`
    - `USERNAME` - Instagram account username
    - `PASSWORD` - Instagram account password
    - `WEBHOOK_URL` - Pre-defined web hook to be used for the app
    - `ADMIN_ID` - Admin telegram ID for special access
    - `GROUP_ID` - Telegram group to be managed the bot for receiving engagement links

  - Goto `config.py` and set `DEBUG` to "True" to run locally and "False" to run in production

  - Run the entrypoint file `python app.py`

Enjoy!

## Show your support

Give a ⭐️ if this project helped you!

<a href="https://www.patreon.com/Codefred">
  <img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Author

👤 **Codefred(Alfred Emmanuel Inyang)**

* Website: www.codedfred.me
* Twitter: [@code\_fredy](https://twitter.com/code\_fredy)
* Github: [@Pycomet](https://github.com/Pycomet)
* LinkedIn: [@alfredemmanuelinyang](https://linkedin.com/in/alfredemmanuelinyang)

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_