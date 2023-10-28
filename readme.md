# Scraping affiliate articles
## **Problem Statement**

As an affiliate manager, I want to know what types of articles and topics generate sales and whether in the long term, these sales are profitable in the long term after paying off commissions to my affiliates.


On a regular basis, I will receive reports of sales, revenue, and retention dimensioned by referrer URL. I will generally group these referrer URLs by the key words within their URL paths into categories based on the theme or topic.


This is a very time consuming and manual process, and is not scalable.


## **Why is this important**

We have noticed over time that sales generated from certain types of articles bring about better long term customers.

Preliminary analysis show that the difference in long term revenue from the worst performing topics vs the best performing topics is a factor of atleast 2x, while we pay the same commissions throughout.

## What is this application

This application is a webscraper that scrapes articles from predetermined domains, limited to certain level 1 URL paths.


The output of this application is the ContentItem object that can be found in /affiliates/affiliates/items.py.

The ContentItem object contains the main body of the webpage's article, ignoring links and special characters.

## What is done with the output

The data in this project is used as an input for a topic model, to determine the latent topics within each affiliate article.

These topics are then used as a feature in predicting long term revenue from user subscriptions generated from each of the articles.