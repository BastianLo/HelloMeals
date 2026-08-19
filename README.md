
<h3 align="center">HelloMeals</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/BastianLo/HelloMeals.svg)](https://github.com/BastianLo/Hellomeals/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/BastianLo/HelloMeals.svg)](https://github.com/BastianLo/Hellomeals/pulls)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](/LICENSE)
![CI Pipeline](https://github.com/BastianLo/Hellomeals/actions/workflows/deploy-docker-image.yml/badge.svg)
</div>

---

<p align="center"> HelloMeals is a self-hostable recipe manager with an integrated scraper to scrape recipes in a large scale.
    <br> 
</p>

## 📝 Table of Contents

- [Features](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 Features <a name = "about"></a>
WIP: Project is still in development and not feature complete!

* Scrape and view Recipes from a central place
* Scraper currently supports the following sites:
  * Chefkoch.de
  * Kitchenstories
  * Hellofresh
  * Lecker.de
  * Eatsmarter
* Pantry Management
  * Add ingredients to your pantry
  * View which recipes you can cook with the current ingredients in your pantry
  * View recipes with a specific Ingredient
* Manage & merge recipes tags for easier filtering
* PWA for Mobile


## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Installing

A step by step series of examples that tell you how to get a development env running.

First clone this repository
```
git clone https://github.com/BastianLo/HelloMeals
```

Then install the required dependencies

```
pip install -r HelloMeals/requirements.txt
```

After successfully installing the dependencies, apply the django database migrations

```
HelloMeals/src/manage.py migrate
```

The Application is now correctly installed and can be run

```
python3 HelloMeals/src/manage.py runserver
```

## 🔧 Running the tests <a name = "tests"></a>
WIP

## 🎈 Usage <a name="usage"></a>
WIP

## 🚀 Deployment <a name = "deployment"></a>

### Docker
Fermento can easily be deployed using docker.

```
version: "3.3"
services:
    db:
        container_name: hello-meals-db
        image: postgres:15
        restart: always
        volumes:
            - ./postgres-data:/var/lib/postgresql/data
        environment:
            POSTGRES_USER: ${POSTGRES_USER}
            POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
            POSTGRES_DB: hellomeals
    hello-meals:
        container_name: hello-meals
        restart: always
        environment:
            - USERNAME=${USERNAME}
            - PASSWORD=${PASSWORD}
            - EMAIL=${EMAIL}
            - DEBUG=False
            - APP_URL=${APP_URL}
            - TIMEZONE=${TIMEZONE}
            - COUNTRY=${COUNTRY}
            - POSTGRES_HOST=db
            - POSTGRES_USER=${POSTGRES_USER}
            - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
            - DOWNLOAD_IMAGES=${DOWNLOAD_IMAGES} #Should images for recipes be downloaded? (True/False)
        ports:
            - "6753:6753"
        image: "bastianlo/hellomeals:latest"
        volumes:
            - ./data:/HelloMeals/src/data
```

## ⛏️ Built Using <a name = "built_using"></a>

- [Django](https://www.djangoproject.com/) - Web Framework
- [Vue.js](https://vuejs.org/) - Frontend Framework
- [Tailwind CSS](https://tailwindcss.com/) - CSS Framework
- 

## ✍️ Authors <a name = "authors"></a>

- [@BastianLo](https://github.com/BastianLo) - Idea & Initial work

See also the list of [contributors](https://github.com/BastianLo/HelloMeals/contributors) who participated in this project.

## 🎉 Acknowledgements <a name = "acknowledgement"></a>
This project is using icons from flaticon.com
