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
faceColorData$H <- faceColorData$H * (pi/180)

col1 <- sin(faceColorData$H) * faceColorData$S
col2 <- cos(faceColorData$H) * faceColorData$S
projectedColorData <- as.data.frame(cbind(col1, col2, faceColorData$faceIdx))
colnames(projectedColorData) <- c("proj1", "proj2", "faceIdx")

face1Idx <- 1000
face2Idx <- 2000
face1RowsIdx <- which(faceColorData$faceIdx == face1Idx)
face2RowsIdx <- which(faceColorData$faceIdx == face2Idx)

mean(sapply(face2RowsIdx, function (face2Idx) { 
  min(unlist(sapply(face1RowsIdx, function(face1Idx) {
    face1Data <- faceColorData[face1Idx,]
    face2Data <- faceColorData[face2Idx,]
    distFunc(face1Data, face2Data)
  })))
}))

plot(NULL, xlim = c(-1,1), ylim = c(-1,1))
sapply(seq(0,9900,100), function(a) {plotFaceColorData(projectedColorData, a)})
