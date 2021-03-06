#Experiments performed on the low-rank recovery duration
dataPointsCount <- 2084
clusterSize <- c(5, 10, 15, 20, 25, 30, 35, 40, 45)
durations <- c(12.030336380004883,
                11.266276597976685,
                12.995521068572998,
                17.926254987716675,
                21.67914390563965,
                28.443479537963867,
                32.07054662704468,
                37.63736867904663,
                47.94002437591553)
durations <- durations / dataPointsCount
lowRankRecoveryTimes <- data.frame(clusterSize, durations)
plot(lowRankRecoveryTimes$clusterSize, lowRankRecoveryTimes$durations, 
     xlab = "Cluster Size", ylab = "Time per patch",
     type = "l")
