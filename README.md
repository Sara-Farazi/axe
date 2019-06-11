# Axe (means Image in Farsi)

Axe is my project for the shopify internship challenege described here. Here is how I created the project: 

## Find dataset
I found a useful image dataset on Kaggle. It's a collection of ~30K images from Flickr with descriptions of what's in each picture. 

## Transform the data
I wrote a few scripts and extracted / cleaned the data for my project's purposes. These scripts can be found in `bootstrap/` in the repo. Here's a short description of each one: 

1. `create_compressed_images.py`: This script reads all of the image files in the dataset and compresses them. These compressed images will later come in handy when I want to return search results. Having compressed versions means I don't incur a lot of network cost on a client that just wants to see small thumbnails in search results. 

2. `populate_images_db.py`: This script creates a database with descriptions about an image, its size on disk and its dimensions. Even though I didn't implement a search using image dimensions in my project, the concept is very similar to other aspects of my search. 

3. `populate_posting_list_db.py`: This creates a table called `posting_list` which maps terms to images they're found in. I use this later to respond to queries efficiently!

## Define and implement the project
According to the project descriptions provided by Shopify, I decided I was going to work on implementing a "search" function. The search function includes the following: 

The project is a web based application implemented using django. It provides a few simple pages: 1) a home page where users can input their search terms and criteria, 2) a results page where users interact with search results, 3) a queries page that shows a quick history of query processing times. 

Users can provide a text query, a minimum and maximum size (in KBs) and Axe will return a (potentially long) list of results. I return results in pages of 16 images so as to not overwhelm the user with too many search results. These 16 items are only the compressed versions of these images allowing the page to load faster. Users can choose to load and look at the full quality version of each image result. I also cache the results of each query so the response will be faster the next time someone searches for a similar query. 

In order to provide some visibilty into how my implementation improves query response time, I implemented a very simple page that shows a history of query processing times.

Users can also select any number of their results and download those selected images in the form of a zip archive file. 

## Things I didn't get to implement 
We can talk about these items if we have time. 

### Search for similar images
Get the terms related to each image and calculate the similarity between two images based on their descriptions (based on a similarity method metric like cosine similarity). This would allow the user to search for similar images of an image. 

### Search by location
The dataset I used didn't have the information needed to implement this, but if I did, it would open up a lot of possiblities: Search on a map, search using location name ("man with a god in Asia"). 

### Improve code quality
Refactor (extract functions, classes), use Django's features to better organize the code (e.g. Django forms, input validation), error handling, and writing tests (?).
