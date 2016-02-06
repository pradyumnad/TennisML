us_open <- read.csv("~/Desktop/us_open.csv")

# Plotting Aces
plot(us_open$Aces, col=us_open$Won+2, pch=19)
plot(us_open$Aces.Norm, col=us_open$Won+2, pch=19)

plot(us_open$X1st.serves.in.Norm, col=us_open$Won+2, pch=19)

#First serves won
plot(us_open$X1st.serve.points.won.Norm, col=us_open$Won+2, pch=19)

#Second serves won
plot(us_open$X2nd.serve.points.won.Norm, col=us_open$Won+2, pch=19)
