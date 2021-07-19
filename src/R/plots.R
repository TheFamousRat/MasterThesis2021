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

#Change done per point at each iteration
perPointMovement_noGNF_0_02 <- c(
                0.00434462943,
                0.00104465167,
                0.00057599991,
                0.00040223215,
                0.00033717956,
                0.00032264463,
                0.00028748607,
                0.00025252480,
                0.00025745063,
                0.00023802395)
plot(perPointMovement_noGNF_0_02, 
     xlab = "Iteration number", ylab = "Movement per point",
     type = "l")

