library(xtable)
library(dplyr)
library(tidyr)
library(ggplot2)

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

#Measuring time taken per iteration per process

timeLRR <- c(
  107.06075239181519,
  80.00615644454956,
  114.45999431610107,
  115.90985012054443,
  111.1321132183075
)

timeGNF <- c(
  5.81937575340271,
  5.785311937332153,
  6.294022560119629,
  5.857945203781128,
  5.993727207183838
)

timeVertUpdt <- c(
  0.6548118591308594,
  0.6727843284606934,
  0.7142558097839355,
  0.673433780670166,
  0.7092750072479248
)

timePatchBuild <- c(
  82.74385, 
  82.03625, 
  86.47193, 
  89.99233, 
  81.81464
)

timeTot <- c(
  192.37850737571716,
  167.12086725234985,
  209.4059705734253,
  208.32616639137268,
  118.27149844169617
)

itNum <- 1:5

timeMat <- as.data.frame(cbind(itNum,timeLRR, timeGNF, timeVertUpdt, timePatchBuild))
colnames(timeMat) <- c("Iteration_Number", "Low Rank Recovery", "Guidance Normal Filter", "Vertex updating", "Patch rebuilding")

timeMat %>% 
  pivot_longer(-"Iteration_Number", names_to = "Variable", values_to = "Value") %>%
  ggplot(aes(x=Iteration_Number, y = Value, fill = Variable)) +
  geom_bar(position = "stack", stat="identity")

#Results (angular difference)

log1dec_ref <- c(
  19.129024544200906,
  10.645136301508826,
  10.643851657444722,
  10.645105040096226,
  10.64317172843923,
  10.635621666823749
)

plastovaKrava_ref <- c(
  14.202552020467484,
  11.291116471877467,
  11.269017907379377,
  11.295077262194283,
  11.308241374945881,
  11.322033897418606
)

mascaron_ref <- c(
  20.153349207899495,
  14.82994238536759,
  14.830028216665811,
  14.819804765357619,
  14.860004565241697,
  14.847421457608537
)


resultsMat <- as.matrix(cbind(log1dec_ref, plastovaKrava_ref, mascaron_ref))
xtable(t(resultsMat), digits = 3)
