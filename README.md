# Blog with Django Rest Framework


<!-- ABOUT THE PROJECT -->
## About The Project

##### This is a sample for a blog web application with custom user model and commenting section, each user has its own profile that is customizable and only can see and change by the owner of profile
##### Each user (that verified) ,can create a post in blog and only the creator of post has the power to edit or delete the post.
##### You can change the env files in env directory to match your preference


### Built With
* [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
* ![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
* ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
* ![](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
* ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
* ![](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
* ![](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
* ![](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
* ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
* ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
* ![](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
* ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
* ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
* ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
* ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)



<!-- GETTING STARTED -->
## Getting Started

This project run in docker and has three phases :
- development
- stagging
- production

and each phase has its own docker compose file.
## Prerequisites

Frist you need to install <a href="https://docs.docker.com/engine/install/">docker</a> and <a href="https://docs.docker.com/compose/install/">docker compose</a> in your local machine or your cloud host.

## Installation
After installing the docker and docker compose you need to clone the repo
1. Clone the repo
   ```sh
   git clone https://github.com/smz6990/DRF-Blog.git
   ```
2. You need to choose which phase do you want to run the project

## Run in development phase:
   You have to  be in the same directory of docker-compose.yml file then run:
   ```sh
   docker compose up --build
   ```
 The build flag is for docker to know that we have Dockerfile and some requirement for the project and it needs to create the image for it first (if you already build the image ,it dont need it, but if you made changes to dockerfile or requirements.txt file you must add build flag. also you can run the command with *-d* to run in detach mode)
 
 #### To stop all the docker containers use:
 ```sh
 docker compose stop
 ```
 ##### To remove all docke containers use:
 ```sh
 docker compose down
 ```
 <hr>
 
 ## Run in stage phase:
   You have to  be in the same directory of docker-compose-stage.yml file then run:
   
   ```sh
   docker compose -f docker-compose-stage.yml up --build
   ```
 ##### To stop docker containers use:
 ```sh
 docker compose -f docker-compose-stage.yml stop
 ```
 ##### To remove docke container use:
 ```sh
 docker compose -f docker-compose-stage.yml down
 ```

<hr>

## Run in production 

the production phase actually done by <a href="https://github.com/AliBigdeli">Ali Bigdeli</a> and credit to him and his great <a href="https://github.com/AliBigdeli/Ultimate-Django3.2-Template">repo</a> , he did a fantastic job and check his repo for more information on production phase and other great work he is done.

<hr>

## bonus:

  actually this project has another docker compose file and it is docker-compose-locust.yml
  It is for stress/load testing your web app before deployment to make sure your web app can handle the work load as you thought
  check <a href="https://locust.io/">locust</a> for more information.
  Now back to our thing.
  
  You have to  be in the same directory of docker-compose-locust.yml file then run:
   
   ```sh
   docker compose -f docker-compose-locust.yml up --build
   ```
   
   and browse 127.0.0.1:8089
   
 ##### To stop docker containers use:
 ```sh
 docker compose -f docker-compose-locust.yml stop
 ```
 ##### To remove docke container use:
 ```sh
 docker compose -f docker-compose-locust.yml down
 ```

<hr>

And thats it .

Feel free to ask me any question

saleh.mohammadzadeh@gmail.com

