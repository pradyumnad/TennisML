us_open <- read.csv("~/Desktop/us_open.csv")
library(caret)
attach(us_open)
# define training control
train_control <- trainControl(method="cv", number=10)
# fix the parameters of the algorithm
grid <- expand.grid(.fL=c(0), .usekernel=c(FALSE))

us_open$WonL = ifelse(us_open$Won == 1, "Yes", "No")

# train the model
formula1 <- WonL ~ X1st.serve.points.won.Norm + X2nd.serve.points.won.Norm + Break.points.won.Norm
formula2 <- WonL ~ Unforced.errors.Norm

model <- train(formula1, data=us_open, trControl=train_control, method="nb", tuneGrid=grid)

print(model)

