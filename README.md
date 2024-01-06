# A Web App to Track Your BTC Addresses

 ![version](https://img.shields.io/badge/version-1.0.1-blue.svg)
Kudos to Creative-time for the [Balck Dashboard Flask template](https://www.creative-tim.com/product/black-dashboard-flask)!
## Table of Contents

- [A Web App to Track Your BTC Addresses](#a-web-app-to-track-your-btc-addresses)
  - [Table of Contents](#table-of-contents)
  - [🪽 Features:](#-features)
  - [✅ Technology](#-technology)
  - [😱 Limitation](#-limitation)
  - [Docker Support](#docker-support)
  - [Create/Edit `.env` file](#createedit-env-file)
  - [Manual Build](#manual-build)
    - [👉 Set Up for `Unix`, `MacOS`](#-set-up-for-unix-macos)
    - [👉 Set Up for `Windows`](#-set-up-for-windows)
  - [Recompile SCSS](#recompile-scss)
  - [Documentation](#documentation)
  - [Template File Structure](#template-file-structure)
  - [Browser Support](#browser-support)
  - [Resources](#resources)
  - [Licensing](#licensing)

<br />

## 🪽 Features:
- 🪽 Create a user and each user could track their addresses independently
- 🪽 Add a BTC address to track in your dashboard
- 🪽 Support adding a nick name for the address so you can easily know which address is which
- 🪽 Able to Synchronize balance of the address and delete the address from tracking
- 🪽 Have pagination to view a list of transactions related to the address.

## ✅ Technology
- ✅ `Persistence`: SQLite
- ✅ `Framework`: Flask and Jinja2
- ✅ `Authentication`: Session Based
- ✅ `Deployment`: Docker, Page Compression (Flask-Minify) 
- ✅ `API`: Use Blockchain.com API 

## 😱 Limitation
- 😱 Blockchain.com API will time out for large offset. Blockchair API is better for large offset, but I run out of time to switch
- 😱 User profile is only partialy connected to the DB, which means all user will see my pickachu placeholder profile except email and user name.
<br />

## Docker Support

> Get the code

```bash
$ git clone git@github.com:ariattt/cointracker.git
$ cd cointracker
```

> Start the app in Docker

```bash
$ docker-compose up --build 
```

Visit `http://localhost:5085` in your browser. The app should be up & running. If you have `Error: error getting credentials - err: exec: "docker-credential-desktop": executable file not found in $PATH, out: ` on mac, change credsStore to credStore in ~/.docker/config.json.

<br />

## Create/Edit `.env` file

The meaning of each variable can be found below: 

- `DEBUG`: if `True` the app runs in develoment mode
  - For production value `False` should be used
- `ASSETS_ROOT`: used in assets management
  - default value: `/static/assets`
- `OAuth` via Github
  - `GITHUB_ID`=<GITHUB_ID_HERE>
  - `GITHUB_SECRET`=<GITHUB_SECRET_HERE> 

<br />

## Manual Build

> UNZIP the sources or clone the private repository. After getting the code, open a terminal and navigate to the working directory, with product source code.

### 👉 Set Up for `Unix`, `MacOS` 

> Install modules via `VENV`  

```bash
$ python -m venv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```
To exit the virtual environment, use `deactivate` command

<br />

> Set Up Flask Environment

```bash
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```

<br />

> Start the app

```bash
$ flask run
// OR
$ flask run --cert=adhoc # For HTTPS server
```

At this point, the app runs at `http://127.0.0.1:5000/`. 

<br />

### 👉 Set Up for `Windows` 

> Install modules via `VENV` (windows) 

```
$ virtualenv env
$ .\env\Scripts\activate
$ pip3 install -r requirements.txt
```

<br />

> Set Up Flask Environment

```bash
$ # CMD 
$ set FLASK_APP=run.py
$ set FLASK_ENV=development
$
$ # Powershell
$ $env:FLASK_APP = ".\run.py"
$ $env:FLASK_ENV = "development"
```

<br />

> Start the app

```bash
$ flask run
// OR
$ flask run --cert=adhoc # For HTTPS server
```

At this point, the app runs at `http://127.0.0.1:5000/`. 

<br />

## Recompile SCSS  

The SCSS/CSS files used to style the Ui are saved in the `apps/static/assets` directory. 
In order to update the Ui colors (primary, secondary) this procedure needs to be followed. 

```bash
$ yarn # install modules
$ # # edit variables 
$ vi apps/static/assets/scss/black-dashboard/custom/_variables.scss 
$ gulp # SCSS to CSS translation
```

The `_variables.scss` content defines the `primary` and `secondary` colors: 

```scss
$default:       #344675 !default; // EDIT for customization
$primary:       #e14eca !default; // EDIT for customization
$secondary:     #f4f5f7 !default; // EDIT for customization
$success:       #00f2c3 !default; // EDIT for customization
$info:          #1d8cf8 !default; // EDIT for customization
$warning:       #ff8d72 !default; // EDIT for customization
$danger:        #fd5d93 !default; // EDIT for customization
$black:         #222a42 !default; // EDIT for customization
```

<br />

## Documentation

The documentation for the **Black Dashboard Flask** is hosted at our [website](https://demos.creative-tim.com/black-dashboard-flask/docs/1.0/getting-started/getting-started-flask.html).

<br />

## Template File Structure

Within the download you'll find the following directories and files:

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |
   |    |-- home/                           # A simple app that serve HTML files
   |    |    |-- routes.py                  # Define app routes
   |    |
   |    |-- authentication/                 # Handles auth routes (login and register)
   |    |    |-- routes.py                  # Define authentication routes  
   |    |    |-- models.py                  # Defines models  
   |    |    |-- forms.py                   # Define auth forms (login and register) 
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>          # CSS files, Javascripts files
   |    |
   |    |-- templates/                      # Templates used to render pages
   |    |    |-- includes/                  # HTML chunks and components
   |    |    |    |-- navigation.html       # Top menu component
   |    |    |    |-- sidebar.html          # Sidebar component
   |    |    |    |-- footer.html           # App Footer
   |    |    |    |-- scripts.html          # Scripts common to all pages
   |    |    |
   |    |    |-- layouts/                   # Master pages
   |    |    |    |-- base-fullscreen.html  # Used by Authentication pages
   |    |    |    |-- base.html             # Used by common pages
   |    |    |
   |    |    |-- accounts/                  # Authentication pages
   |    |    |    |-- login.html            # Login page
   |    |    |    |-- register.html         # Register page
   |    |    |
   |    |    |-- home/                      # UI Kit Pages
   |    |         |-- index.html            # Index page
   |    |         |-- 404-page.html         # 404 page
   |    |         |-- *.html                # All other pages
   |    |    
   |  config.py                             # Set up the app
   |    __init__.py                         # Initialize the app
   |
   |-- requirements.txt                     # App Dependencies
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- run.py                               # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />

## Browser Support

At present, we officially aim to support the last two versions of the following browsers:

<img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/chrome.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/firefox.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/edge.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/safari.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/opera.png" width="64" height="64">

<br />

## Resources

- Demo: <https://www.creative-tim.com/live/black-dashboard-flask>
- Download Page: <https://www.creative-tim.com/product/black-dashboard-flask>
- Documentation: <https://demos.creative-tim.com/black-dashboard-flask/docs/1.0/getting-started/getting-started-flask.html>
- License Agreement: <https://www.creative-tim.com/license>
- Support: <https://www.creative-tim.com/contact-us>
- Issues: [Github Issues Page](https://github.com/creativetimofficial/black-dashboard-flask/issues)

<br />


## Licensing

- Copyright 2019 - present [Creative Tim](https://www.creative-tim.com/)
- Licensed under [Creative Tim EULA](https://www.creative-tim.com/license)
