# UOCIS322 - Project 4 #

## Info

Name: Sophia Zhang\
e-mail: sophiaz@uoregon.edu

## Overview
RUSA ACP Control Time Calculator (with flask and AJAX)\
This project consists of a web application that is based on RUSA's online 
calculator. This includes implementing the algorithm to compute open and close 
times, and sending the information back to the website for users to see. 

## Tasks
 * Implemented acp_times.py which calculates the open and close times with the algorithm from the offical website.

 * Edit calc.html and Flask app so that the remaining arguments are passed along


## Running Docker 

To run docker simple open your terminal and type in the command: 

```
docker build -t some-image-name .
```
Where some-image-name can be any name you want, and the '.' means to run all of your files, you can specifiy a certain file by doing 

```
docker build -t some-image-name file_name
```
To run your image after you have built it, you can run: 

```
docker run -d -p 5001:5000 some-image-name
```

Here it is running the image that is just built, and 5001:5000 means the host machine 
is running on port 5001, and to map it onto port 5000. To access the application, 
open a web browser and type in :

```
http://localhost:5001
```

Make sure your port number is 5001 in credentials.

### Running Docker Testing

I have written five test cases that outline some correct brevet distance races with accetable time break points.

To run the test file:

After you have built and ran docker, you can do 
```
docker ps
``` 
to check for the ID of the container name, then copy and paste the ID to run docker exec: 
```
docker exec $CONTAINER ./run_tests.sh
```


## The Application

Once you have ran the website, it should bring you to a page called ACP Brevet Times. 
Where you can specify the distance, the race start time, and as well as entering different break points. 
At each break point you enter should update you with the opening and close times of each check point. 



