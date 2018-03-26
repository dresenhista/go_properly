---
title: 'House Pricing problem: Calgary'
author: "Andresa Andrade"
date: "March 26, 2018"
output:
  html_document: default
  pdf_document: default
---

```{r setup, include=FALSE}

```

## Trying to solve the House Pricing problem: Calgary
##Problem

At a high level we are building a residential real estate marketplace in which we will be buying and selling homes (for which we will be setting the price). Our model needs to tell us which homes to buy, and provide us with comfort that for the homes we do buy, we know what price we can resell them for and how long it will take to do so. 


In this folder you can see the sample data from Calgary (just historical sales data from the MLS). **The goal is to take  an initial (v0) model that helps us decide what the value of a house should be.**

We also need to write a simple report (can be bullet points) detailing your technical decisions, how those decisions would impact the business, and the type of additional work I would do to improve upon the model with more time. 


##Steps to model
Before we start, I need to point it out two personnal preferences: I usually like doing modeling with dataframe structures. And I am using R and python in this project: Python to clean the data and R to model it.


1. Read the json type of file and translate into dataframes we will be using the cleaning_file.py file in this directory to perform this step

2.Import the desired files into R. It is best practice to split the data into training and testing. For the purposes of this project I decided to use one file to test and one to train, but you can use as many as you want, but they should not overlap. In other words, whatever was used to train should not be used to test. This will avoid bias towards the model.

3. Perform a statistics methodology that can predict price. Here there are a fre methodologies that can be used. I chose Multilinear Regression because it is a simple method and it seems to be predicting well the price of the houses.

4. With the model diagnostic metrics, decide which features to keep in the model. Here I perfomed a Backwards methodology where I started with all the metrics and then I removed one at time based on higher p-values. One important point is that we need to understand data correlation. Linear regression is a calculation that uses the determinant of the independent variables, if we have a variable that is a linear combination of others (i.e. correlated to others), the determinant will be 0 and the model is not going to convert.

5. Now that all the tests are passing, it's time to take a step forward and test if the model works for other data. This helps us to avoid overfitting. I used the file #2 to test.

6. Last but not least let's see how far away we got the price from what was solf for.

#In the future

Ideally we want to add more data in one data frame because the outliers might become actual data with its own attributes. We would also want to predict given a price, and the houses feature, how long it will take to sell with some percentages below the listing price. For example, if the seller is willing to go as low as 90% of the listing, it will take 30 days to sell, but if the seller agrees to go to 70% of the listing then it might sell in 5 days.

We would also want to understand how the houses are distribuited by zip code per attribute, for example, houses in one single neighborhood might be more modern and therfore has a specific price point.

last but not least, economic indicator such as employment rate, growing economy are things that are related to the real estate market.



## Data overview
The data we are working on looks like the sample below:
```{r, echo=FALSE}
training= readRDS('training.RDS')
head(training)
```



And before we start, it is important to understand outliers and how the sold.Price values are distribuited. A box plo9t helps to see that:
```{r, echo=FALSE}
boxplot(training$Sold.Price)
```

We can see that there are a few houses skewed towards the $2M value. In the distribution this is even more evident:

```{r, echo=FALSE}
plot(density(training$Sold.Price), main="Density Plot: Sold Price", 
     ylab="Frequency", sub=paste("Skewness:", round(e1071::skewness(training$Sold.Price), 2))) 

polygon(density(training$Sold.Price), col="blue")
```

Now we have an idea that we are working with outliers, idealy we want to treat the outliers because they will affect the model. For now, I will leave them there for study purposes.

#Modeling
Now that we know the data distribution, we should start modeling. I have done some work removing the correlated variables and also the ones with low p-value and this is what we got:

```{r, echo=FALSE}
data_names = names(training)
data_size = length(training)

regression_function = paste(data_names[1], '~', paste(data_names[2:data_size], collapse = '+'))
regression_function = as.formula(regression_function)



linearMod <- glm(regression_function, data=training)
#print(linearMod) 
summary(linearMod)
```

we can see that all the coefficients pass the relevance test (p-value<0.05) and this is the set of variables with higher R2 (that measures the quality of the model)

This way our model is something like:
```{r}
print(linearMod) 
```


##Testing
Finally, now let's go out to the "real data" and see how good we predict. The testing set is the file #2 therefore was not used in to model the regression and it's completely unknown data for the model. And has the sold price, which allows us to see how wrong/right we are.

```{r, echo=FALSE}
testing= readRDS('testing.RDS')

testing$sold_price_new<-predict(linearMod, type = "response", newdata= testing)

testing$percentage<-abs((testing$sold_price_new-testing$Sold.Price)/testing$Sold.Price)
plot(testing$percentage, main='% distribution of % of error')

```

With the exception of one house, the model is predicting the price correctly (with less than 5% of error) for the whole testing set. Let's see what is happening with that one house:

```{r, echo=FALSE}
#print(testing(testing$percentage>10))
testing[testing$percentage>=10,]
```
Basically when the realtor typed the number of parking spots there was a mistake (it is almost impossible one house to have 1423 parking spots) and therefore the model is having a hard time to predict the price.


We can also take a look at the distributions of correctness of my model using the table below:

```{r, echo=FALSE}
pred<-abs((testing$sold_price_new-testing$Sold.Price)/testing$Sold.Price)
pred_table<-table(round(pred,2))
print(pred_table)
```


Out of 489 records I have gotten 128 correct. 148 with 1% of error and etc. Pretty good.
