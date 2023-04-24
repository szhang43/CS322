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

## With API 

* Using API in this project (Back-end)
	* A RESTful service to expose/store structured data in MongoDB.

Using the schema, build a RESTful API with the resource `/brevets/`:\
		* GET `http://API:PORT/api/brevets` should display all brevets stored in the database.\
		* GET `http://API:PORT/api/brevet/ID` should display brevet with id `ID`.\
		* POST `http://API:PORT/api/brevets` should insert brevet object in request into the database.\
		* DELETE `http://API:PORT/api/brevet/ID` should delete brevet with id `ID`.\
		* PUT `http://API:PORT/api/brevet/ID` should update brevet with id `ID` with object in request.

## Running the File 

Again similar to project 5, we can use : ```docker compose up --build```
to build our container, then going to ```http://localhost:5002/``` should display 
the webpage.