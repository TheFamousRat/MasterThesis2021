library("readr")

plotFaceColorData <- function(data, faceIdx) {
  faceRows <- which(data$faceIdx == faceIdx)
  lines(data[faceRows,1], data[faceRows,2], type = "p", col = hsv(faceIdx/max(data$faceIdx)))
}

distFunc <- function(col1, col2) {
  (cos(col1[1]) * col1[2] - cos(col2[1]) * col2[2])^2 + (sin(col1[1]) * col1[2] - sin(col2[1]) * col2[2])^2
}

pi <- 3.14159264

faceColorData <- read_csv("/home/home/thefamousrat/facePixels.csv")
faceColorData$H <- faceColorData$H * (2*pi)

col1 <- sin(faceColorData$H) * faceColorData$S
col2 <- cos(faceColorData$H) * faceColorData$S
projectedColorData <- as.data.frame(cbind(col1, col2, faceColorData$faceIdx))
colnames(projectedColorData) <- c("proj1", "proj2", "faceIdx")

plot(NULL, xlim = c(-0.4,0.4), ylim = c(-0.5,0.5), xlab = "Xproj", ylab = "Yproj")
abline(a = 0, b = 0)
lines(c(0,0),c(-10000,10000))

plotFaceColorData(projectedColorData, 5)
plotFaceColorData(projectedColorData, 90)
