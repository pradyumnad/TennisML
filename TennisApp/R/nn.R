library(neuralnet)
library(caret)

attach(us_open)

# splitdf function will return a list of training and testing sets
splitdf <- function(dataframe, seed=NULL) {
  if (!is.null(seed)) set.seed(seed)
  index <- 1:nrow(dataframe)
  trainindex <- sample(index, trunc(3*length(index)/4))
  trainset <- dataframe[trainindex, ]
  testset <- dataframe[-trainindex, ]
  list(trainset=trainset,testset=testset)
}

dataMain =  splitdf(us_open)

formula = Won ~ X1st.serve.points.won.Norm + X2nd.serve.points.won.Norm + Break.points.won.Norm
net <- neuralnet(formula,
                 hidden = 5, lifesign = "minimal", algorithm = "backprop",
                 data = dataMain$trainset, learningrate = 0.01, stepmax = 1e5)
print.nn(net)
plot.nn(net)

net2 <- neuralnet(formula,
                 hidden = 0, lifesign = "minimal", linear.output = TRUE,
                 data = dataMain$trainset, stepmax = 1e5)
print.nn(net2)
plot.nn(net2)
