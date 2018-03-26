library(tidyverse)
library(corrplot)

#setwd("C:/localhost/99-Personal/Internal Applications/go_properly")

#function to clean dataframe
clean_dataframe<-function(df){
  df<- df%>%
    mutate(altadore = case_when(
      grepl('Altadore', Community) ~ 'Altadore',
      TRUE ~ 'Other'))%>%
    select(-X, -Property.Type, -Building.Type, -Beds.Total, - Tax.Amount, -Yr.Built, -Community, -Front.Exposure, -Basement.Development, -Construction.Type, -Exterior, -Goods.Included, -Heating.Fuel,
           -Parking, -Style, -day_sold, -postal_code, -Tot.Flr.Area.A.G...SF.)

  return(df)  
}

#we can now choose how many files we want to run the analysis
concatenate_files <- function(directory, ids) {
  # locate the files
  files <- list.files(directory, full.names=T)[ids]
  
  # read the files into a list of data.frames
  data.list <- lapply(files, read.csv)
  
  # concatenate into one big data.frame
  data.cat <- do.call(rbind, data.list)
  
  return(data.cat)
  
  # aggregate
  # data.agg <- aggregate(value ~ index, data.cat, mean)
}

path = 'Scraper\\new_data'

#loading training data where we will perform the modeling
training<- read.csv(paste(path,'\\file_1.csv', sep=''))
training<- clean_dataframe(training)
saveRDS(training, 'code\\training.RDS')

#testing model data we will test the model
testing<- read.csv(paste(path,'\\file_2.csv', sep=''))
testing<- clean_dataframe(testing)

saveRDS(testing, 'testing.RDS')

#how are the prices distributed
#from here we observe a few outliers above $1,5M
boxplot(training$Sold.Price)



#check if selling price is normal distribuited
plot(density(training$Sold.Price), main="Density Plot: Sold Price", 
     ylab="Frequency", sub=paste("Skewness:", round(e1071::skewness(training$Sold.Price), 2))) 

polygon(density(training$Sold.Price), col="blue")


#multilinear regression

data_names = names(training)
data_size = length(training)

regression_function = paste(data_names[1], '~', paste(data_names[2:data_size], collapse = '+'))
regression_function = as.formula(regression_function)



linearMod <- glm(regression_function, data=training)
#print(linearMod) 
summary(linearMod)




#testing the coefficients in the new model
testing$sold_price_new<-predict(linearMod, type = "response", newdata= testing)

pred<-abs((testing$sold_price_new-testing$Sold.Price)/testing$Sold.Price)
pred_table<-table(round(pred,2))
print(paste("Prediction Table for validation", i))
print(pred_table)


#confusion matrix
c<-table(factor(round(testing$sold_price_new),levels=3:8), testing$Sold.Price)





#print output in a text file
#out <- capture.output(summary(linearMod))
#cat("My title", out, file="regression_output.txt", sep="\n", append=TRUE)



