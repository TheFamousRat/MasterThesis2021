library("readr")

faceColorData <- read_csv("/home/home/thefamousrat/facePixels.csv")

plotFaceColorData <- function(data, faceIdx) {
  faceRows <- which(data$faceIdx == faceIdx)
  lines(data$H[faceRows], data$S[faceRows], type = "p", col = hsv(faceIdx/max(data$faceIdx)))
}

data <- faceColorData
color <- hsv()

plot(NULL, xlim=c(0,360), ylim=c(0,1), xlab = "H", ylab = "S")
for (i in seq(0,99,10)) {
  plotFaceColorData(faceColorData, i)
}


