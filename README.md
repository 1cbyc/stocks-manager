# Stocks Manager

Stock portfolio manager built with Flask

<!-- ![Screen Shot 2020-10-05 at 18 22 12](https://user-images.githubusercontent.com/10364402/95099033-13ff6600-0738-11eb-8610-504ec3e297a6.png)
![](https://user-images.githubusercontent.com/10364402/95098968-01852c80-0738-11eb-8f02-42939f5163b9.png) -->

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Built With](#built-with)
* [Contributing](#contributing)
* [License](#license)


### Built With
Frameworks, tools and libraries used in this project
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Bootstrap](https://getbootstrap.com)
* [Wallstreet](https://pypi.org/project/wallstreet/0.1.5/)
* [JQuery](https://jquery.com)
* [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)

## Getting Started
Clone using `https://github.com/1cbyc/stocks-manager.git`.

### Install the requirements:
```bash
$ pip install -r requirements.txt
```

### Environment Setup
1. Copy `env.example` to `.env`:
```bash
$ cp env.example .env
```

2. Edit `.env` and set your configuration values:
   - `SECRET_KEY`: Generate a secure secret key for Flask sessions
   - `OKTA_API_TOKEN`: Your Okta API token
   - `OKTA_URL`: Your Okta organization URL
   - Other OIDC settings as needed

3. Ensure `client_secrets.json` is configured for Okta OIDC authentication

### Run the app:
```bash
$ python run.py
```
or
```bash
$ flask run
```

The app will run on `http://127.0.0.1:8001` in development mode.

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License
Distributed under the MIT License. See `LICENSE` for more information.
