
# Minimal web-based todo list

This is an example that demonstrates how to loop through listed HTML elements with JQuery, and 
how to send requests to flask that contain lists.

In this example, you will see how to:

* Send POST requests with AJAX,
* Loop through multiple HTML input fields, collect their values, and store them in a Javascript dictionary,
* Convert a Javascript dictionary to a JSON, and send it to a backend interface (Flask,)
* Parse JSON input data in with Flask,
* Loop through HTML input fields and update their values.

## Getting started

As long as you have Docker and compose set up, just do:

```
docker compose up
```

The default port is `5001`.
You can modify it in `docker-compose.yml` or set up an override file.

### Web service
Just go to `localhost:5001` (if you're not running docker locally, replace `localhost` with the correct hostname, if you're not
binding to port `5001`, replace that as well.)

You should see a webpage that looks like the following:

![Empty page](assets/empty.png)


Click the :heavy_plus_sign: button to add items to the list.
Then enter any value.

![Empty page](assets/one_item.png)

And upon clicking "Save", jQuery will send a POST request to `/insert`, which takes in the list,
inserts it into the database (MongoDB; database: todo ; collection: lists).
Empty list items will be ignored.

![Empty page](assets/multiple_items.png)

If you go ahead and refresh, you should get an empty list again:

![Empty page](assets/empty.png)

Upon clicking "Fetch", jQuery will send a *GET* request to `/fetch` with no data, and gets back the _newest_
entry in the database, and populates the page with it.

![Empty page](assets/fetched_items.png)

### Database
We're using MongoDB (v 5.0.5), just like project 5.


## What's this for?
This example has Javascript for loops, sends POST requests with variable length data (in JSON) sent to the backend, and sends
GET requests to fetch said data back from the server, and populates the HTML with it.

Despite its simplicity, it has a few bells and whistles that you WON'T use in project 5, such as the :heavy_plus_sign: and
:heavy_multiplication_x: buttons. You'll stick to the fixed 20 rows there.

But what you can do is to look at the HTML, Javascript (both in one HTML file) and Flask and how they interact, and use that to
finish your [project 5](https://github.com/UO-CIS322/project-5).


## Authors
Created by [Ali Hassani](https://alihassanijr.com) for [CS 322](https://classes.cs.uoregon.edu/23W/cis322/).
