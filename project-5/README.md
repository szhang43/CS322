# UOCIS322 - Project 5 #

## Info

Name: Sophia Zhang\
e-mail: sophiaz@uoregon.edu

## Overview
RUSA ACP Control Time Calculator (with flask and AJAX)\
This project consists of a web application that is based on RUSA's online 
calculator. This includes implementing the algorithm to compute open and close 
times, and sending the information back to the website for users to see. 


## The Application

Once you have ran the website, it should bring you to a page called ACP Brevet Times. 
Where you can specify the distance, the race start time, and as well as entering different break points. 
At each break point you enter should update you with the opening and close times of each check point. You will 
notice that there are two buttons which are submit and display where submit allows you to store your data entry. 
And display will fetch your previous entry back onto the screen.

## Running Docker 

To run docker simple open your terminal and type in the command: 

```
docker compose up
```
Then following each re-build, include --build like so: 
```
docker compose up --build
```
This will allow you to re run your programm without building a new container



### Running Docker Testing w. Docker Compose

To run the test files: 
``` 
docker compose exec $SERVICENAME bash
```
This will put you in an interactive bash in your container,
Then run: 
```
./run_tests.sh
```
