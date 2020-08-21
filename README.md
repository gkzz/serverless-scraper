# Serverless Scraper

Serverless Scraper with AWS Lambda Function and Selenium WebDriver


Spetial Thanks to

- [Serverlessを使って簡単にAWS Lambda Layers上でHeadless Chromeを動かす](https://blog.ikedaosushi.com/entry/2018/12/22/231421)

## Usage

- Configure ~/.aws/config
```
$ aws configure
```


- git clone
```
$ git clone https://github.com/gkzz/serverless-scraper.git \
&& cd serverless-scraper
```

- Download chromedriver and headless-chrome
```
$ . install.sh
```

- Install serverless framework and modify config/.env
```
$ sudo npm install -g serverless
$ cd selenium-layer
$ npm init
$ sudo npm install --save serverless-dotenv-plugin
$ cat config/.env.tmpl > config/.env
$ pip install -t selenium/python/lib/python3.7/site-packages selenium
```

- Deploy Chrome/Selenium WebDriver!
```
$ serverless print
$ serverless deploy
```

- Prepare before deploying a Python Program with sls command
```
$ cd lambda
$ npm init
$ sudo npm install --save serverless-python-requirements \
> && sudo npm install --save serverless-dotenv-plugin \
> && sudo npm install --save serverless-offline

$ cat config/.env.tmpl > config/.env
```

- Deploy it!
```
$ serverless print
$ serverless deploy
```

## Technology Used

### on local
- serverless
    - Framework Core: 1.60.4
    - Plugin: 3.2.6
    - SDK: 2.2.1
    - Components Core: 1.1.2
    - Components CLI: 1.4.0
- ChromeDriver 2.40
- Headless Chrome v1.0.0-55

### AWS Lambda
- Python 3.7

## Notes

```
gkz@local ~/serverless-chrome (master) $ tree -L 2
.
├── install.sh
├── lambda
│   ├── config
│   ├── handler.py
│   ├── node_modules
│   ├── package.json
│   ├── package-lock.json
│   └── serverless.yml
├── LICENSE
├── README.md
└── selenium-layer
    ├── config
    ├── driver
    ├── node_modules
    ├── package.json
    ├── package-lock.json
    ├── selenium
    └── serverless.yml

8 directories, 10 files
```


## FAQ

- `selenium.common.exceptions.WebDriverException: Message: chrome not reachable`
    - Check the following issues
    - [adieuadieu/serverless-chrome/issues/133](https://github.com/adieuadieu/serverless-chrome/issues/133)


https://chromedriver.storage.googleapis.com/

https://chromedriver.chromium.org/downloads

https://github.com/adieuadieu/serverless-chrome/releases