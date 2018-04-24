# Kaleo Data Science Assesment

Welcome! We're excited to see what you can do with your computer, some data, and an open ended question! (Maybe some coffee too, if you're like us...)

Our goal here is threefold:

1. We want to assess your potential as a rockstar data scientist and engineer
2. We want you to have fun! Think of this as an example of something you might need to work on one day. 
3. We want to know that you can function at the command line and with GitHub.

## The Task

The task has three parts -- data collection, data exploration / algorithm development, then finally predictive modeling. 

**Feel free to develop in any mainstream language that you deem appropriate for this problem.**

### Part 1 -- Collection

We want you to scrape the web and **collect all of the articles** under the following wikipedia categories:

* [Machine Learning](https://en.wikipedia.org/wiki/Category:Machine_learning)
* [Business Software](https://en.wikipedia.org/wiki/Category:Business_software)

More specifically, we would love it if you build a script that ingested some sort of file that specified which categories to chug along and crawl. Something like:

```
https://en.wikipedia.org/wiki/Category:Machine_learning
https://en.wikipedia.org/wiki/Category:Business_software
```

We want your code to be modular enough that any valid category from Wikipedia can be scraped by your code.

At minimum, you'll need to store the article text, but do store whatever other metadata you deem useful. Feel free to store this in whatever format suits you, be it MySQL, Mongo, a Pandas dataframe whatever! It'll be indexed later on to perform **Part 2**.

We only require that we can run this section by typing

```bash
me@my-macbook$ ./download /path/to/optional/list_of_categories
```

### Part 2 -- Search

This is where you can flex your creative data munging chops! We want to be able to pass you a search query at the command line and be returned a set of relevant articles. You have some license here! This could be any/all/none of:

* Return a snippet of text from the top 5 related articles to the search query.
* Return the full text from the top related article with related words colored in red.
* Anything else you deem cool! This part is up to you.

We require that we can query this section with the commands such as

```bash
me@my-macbook$ ./search enterprise software
me@my-macbook$ ./search cloud computing platform
```

### Part 3 -- Predictive Model

In this part, we want you to build a predictive model from the data you've just indexed. Specifically, when a new article from wikipedia comes along, we would like to be able to predict what category the article should fall into. We expect a training script of some sort that is runnable and will estimate a model **using proper data science principles**. Something like this:

```bash
me@my-macbook$ ./train-model
```

Finally, we want a command line interface (call it `./predict`) for predicting the class of new articles! The command line utility should read in the model from `./train-model` and a URL from a wikipedia page, and predict the category which that article should belong to. For example, output might look like:

```bash
me@my-macbook$ ./predict https://en.wikipedia.org/wiki/Support_vector_machine
Predicted Category: Machine_learning
Confidence: 0.9
```

## Infrastructure

You are allowed to use any mainstream language you like! We'll leave it to your judgement as to the decision of mainstream or not.

You can have as many helper files / directories as you want, but keep the project clean! Please develop on either a Mac or a Unix/Linux box, and include a script that we can call

```bash
me@my-macbook$ ./install.sh
```

that will install any software we might need to run your masterpiece. **Do let us know what platform your script expects (Mac / Linux)**

## Evaluation

You'll be evaluated on the following criteria:

* **Readibility / Style:** is the code approachable, clear, and extensible/modifiable by another engineer?
* **Documentation:** is the code adequately and informatively documented?
* **Algorithms:** are you doing everything brute force and re-inventing the wheel?
* **Creativity:** does the output of your script show insight? Is it useful, relevant?

There is no fixed deadline, but we expect this to be doable in a weekend afternoon or so (± O(1) hr)



