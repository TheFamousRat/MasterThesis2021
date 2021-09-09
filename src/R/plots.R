library(xtable)
library(dplyr)
library(tidyr)
library(ggplot2)

setwd("/home/home/thefamousrat/Documents/KU Leuven/Master Thesis")

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
xtable(resultsMat, digits = 3)

#PCA on textures
pcaValsLog <- c(0.15526956, 0.13124713, 0.090926036, 0.06852879, 0.05909133, 0.051406555, 0.047981057, 0.034766242, 0.027514804, 0.024329547, 0.021077152, 0.018266017, 0.016796073, 0.0155253755, 0.013568923, 0.011431426, 0.010057417, 0.009848934, 0.008573699, 0.008315387, 0.0076876506, 0.0067769727, 0.0064510778, 0.0060714097, 0.0055477535, 0.005329972, 0.005047527, 0.004824242, 0.004342545, 0.004211764, 0.0038194906, 0.0036196155, 0.0034153298, 0.003243732, 0.0030939681, 0.0029034675, 0.0027122486, 0.002642314, 0.0025916903, 0.0024982211, 0.0022982354, 0.0022209862, 0.0021419944, 0.0020408663, 0.0019771168, 0.0019649127, 0.0018603638, 0.0018107618, 0.0017579086, 0.0015730568, 0.0015280626, 0.0015101816, 0.0014616194, 0.001413637, 0.0013303533, 0.0013139043, 0.001247929, 0.0012288433, 0.0012103728, 0.0011731948, 0.0011558734, 0.0011321366, 0.0010698198, 0.0010588273, 0.0010452742, 0.0010322036, 0.0010114284, 0.0009743269, 0.0009481403, 0.0009159885, 0.00089820684, 0.00089018623, 0.0008548616, 0.00082130055, 0.00081084704, 0.00080620823, 0.0007905884, 0.0007555192, 0.0007370753, 0.00072917383, 0.0007202939, 0.00070170243, 0.00068188185, 0.000656667, 0.0006537709, 0.0006472436, 0.0006445838, 0.00062964694, 0.0006085856, 0.0005950207, 0.00058544724, 0.0005753121, 0.00055914035, 0.000547649, 0.00053950347, 0.0005275389, 0.0005110799, 0.00050403696, 0.00049400755, 0.0004857507)
pcaValsCow <- c(0.18492323, 0.15663385, 0.09416301, 0.06376371, 0.059175223, 0.04497298, 0.03979334, 0.02982013, 0.025599062, 0.022325862, 0.019715175, 0.0173712, 0.0153338825, 0.0119658625, 0.010296889, 0.0093040215, 0.00902711, 0.008823778, 0.008513799, 0.006955577, 0.0065091625, 0.005705274, 0.0053235516, 0.0050987694, 0.004731616, 0.0042400677, 0.004161375, 0.004048906, 0.003776505, 0.0036192476, 0.0034565208, 0.0033013183, 0.0030903833, 0.0029773067, 0.002702583, 0.0026278351, 0.0024780044, 0.0024622707, 0.0023795178, 0.0022718816, 0.0021597876, 0.002068012, 0.0019913572, 0.0018542358, 0.001740564, 0.0017101292, 0.0016186057, 0.0015637177, 0.001533593, 0.0014994194, 0.0014816903, 0.0014058257, 0.0013790983, 0.0013199823, 0.0012881634, 0.0012653857, 0.0012376156, 0.0012233427, 0.0011444679, 0.0011373318, 0.0010722855, 0.0010601975, 0.0010243937, 0.0010097182, 0.0009876142, 0.0009523156, 0.0009420531, 0.0008963133, 0.0008818372, 0.0008681832, 0.00085049786, 0.00083769637, 0.00082347536, 0.0008145567, 0.0007901443, 0.00078883977, 0.00075249106, 0.00072487985, 0.00068879995, 0.0006719787, 0.000664773, 0.00065262057, 0.00064580305, 0.0006338554, 0.0006235884, 0.00061573525, 0.000599912, 0.0005908426, 0.00057806546, 0.0005716839, 0.0005618845, 0.0005455056, 0.000544149, 0.00053060823, 0.0005229996, 0.00051478937, 0.0005002148, 0.00049653917, 0.00047054252, 0.00046322992)
pcaValsMascaron <- c(0.18538205, 0.13484131, 0.10560707, 0.058396142, 0.05413921, 0.047791775, 0.04001496, 0.029717311, 0.026642438, 0.024139522, 0.020239986, 0.017965224, 0.016243063, 0.01269989, 0.011858527, 0.010707461, 0.010438994, 0.009813152, 0.008636137, 0.007066869, 0.0067889523, 0.006296887, 0.0057807444, 0.005459567, 0.0051577953, 0.0048230323, 0.004419287, 0.0042449837, 0.004014321, 0.0038762486, 0.0036256046, 0.0034599553, 0.0033523615, 0.0029367665, 0.0028271705, 0.0027074534, 0.0026106017, 0.0024875249, 0.0024028795, 0.0023047794, 0.0022042063, 0.002099199, 0.0020488976, 0.0019720274, 0.0019578012, 0.0019249164, 0.0018201891, 0.001756244, 0.0015953658, 0.001557523, 0.0015218357, 0.0014960046, 0.0014688306, 0.0013243244, 0.0012978761, 0.0012842546, 0.0012467802, 0.0012335159, 0.0011784872, 0.0011496389, 0.0011312219, 0.0010937816, 0.0010560624, 0.0010470117, 0.0010332442, 0.0009864656, 0.00097352173, 0.00093914487, 0.0009349525, 0.0009168173, 0.00086326286, 0.00085320754, 0.00084951223, 0.0008238736, 0.0007871166, 0.000783181, 0.0007750252, 0.0007465957, 0.00071483094, 0.0007108575, 0.000684485, 0.0006772158, 0.000665204, 0.0006582078, 0.0006405871, 0.000639045, 0.00061292393, 0.00061078387, 0.0005974668, 0.0005950324, 0.00057970197, 0.0005701357, 0.0005539355, 0.0005322442, 0.0005274863, 0.00051698636, 0.00050477573, 0.00050271, 0.0004878874, 0.00047937833)

plot(cumsum(pcaValsLog), type = "l", col = "red")
lines(cumsum(pcaValsCow), type = "l", col = "blue")
lines(cumsum(pcaValsMascaron), type = "l", col = "green")

##Times for the LRR with values of weight
getLRRData <-function(LRRTimes, faceCount) {
  x <- 1000.0 * LRRTimes / faceCount
  cat(paste(round(mean(x), 3), " \\pm", round(1.96 * sd(x), 3)))
}

#Log
logFacesCount <- 4387
log_0_0w <- c(102.7813332080841, 127.54133367538452, 134.97315645217896, 100.98757433891296, 92.12555193901062, 95.75744318962097)
log_0_01w <- c(79.18097996711731, 77.13677883148193, 69.38012266159058)
log_0_1w <- c(87.2138922214508, 118.84234476089478, 105.52409744262695, 62.618215799331665, 83.53808188438416, 101.25018882751465, 94.76512551307678, 80.56025075912476)
log_0_5w <- c(119.58829474449158, 121.45886611938477, 128.97431206703186, 85.69205403327942, 76.47698783874512, 107.25627493858337, 111.17348885536194)
log_1_0w <- c(115.52145218849182, 126.47952699661255, 115.22836780548096, 82.84313225746155, 97.75865006446838, 109.84130716323853, 93.31606125831604)
log_10_0w <- c(130.10519409179688, 110.32883739471436, 95.36199903488159, 86.13138151168823, 83.35458731651306, 67.08086895942688, 89.56362080574036)

getLRRData(log_0_0w, logFacesCount)
getLRRData(log_0_01w, logFacesCount)
getLRRData(log_0_1w, logFacesCount)
getLRRData(log_0_5w, logFacesCount)
getLRRData(log_1_0w, logFacesCount)
getLRRData(log_10_0w, logFacesCount)

#Mascaron
mascaronFacesCount <- 4815
mascaron_0_0w <- c(91.10781216621399, 113.03260111808777, 104.20079565048218)
mascaron_0_01w <- c(84.79101800918579, 89.23634266853333, 95.27992105484009)
mascaron_0_1w <- c(84.0866367816925, 88.25917720794678, 103.61575770378113)
mascaron_0_5w <- c(94.14801287651062, 105.15330219268799, 125.34038424491882)
mascaron_1_0w <- c(114.24745321273804, 95.16082310676575, 107.39345908164978)
mascaron_10_0w <- c(109.47727799415588, 108.62599873542786, 93.65240693092346)

getLRRData(mascaron_0_0w, mascaronFacesCount)
getLRRData(mascaron_0_01w, mascaronFacesCount)
getLRRData(mascaron_0_1w, mascaronFacesCount)
getLRRData(mascaron_0_5w, mascaronFacesCount)
getLRRData(mascaron_1_0w, mascaronFacesCount)
getLRRData(mascaron_10_0w, mascaronFacesCount)

#Cow
cowFacesCount <- 4965
cow_0_0w <- c(83.70483779907227, 82.45345306396484, 93.32482862472534)
cow_0_01w <- c(94.8536229133606, 74.42958068847656, 79.57779788970947)
cow_0_1w <- c(90.37957310676575, 84.23308968544006, 84.53332924842834)
cow_0_5w <- c(107.21420454978943, 79.04356384277344, 78.30926632881165)
cow_1_0w <- c(103.33472466468811, 82.43171572685242, 80.17290544509888)
cow_10_0w <- c(80.70999908447266, 79.19786715507507, 99.00771307945251)

getLRRData(cow_0_0w, cowFacesCount)
getLRRData(cow_0_01w, cowFacesCount)
getLRRData(cow_0_1w, cowFacesCount)
getLRRData(cow_0_5w, cowFacesCount)
getLRRData(cow_1_0w, cowFacesCount)
getLRRData(cow_10_0w, cowFacesCount)

###Tests
t.test.from.summary.data <- function(mean1, sd1, n1, mean2, sd2, n2) {
  data1 <- scale(1:n1)*sd1 + mean1
  data2 <- scale(1:n2)*sd2 + mean2
  t.test(data1, data2)
}

testSignificanceRepeatedTests <- function(means0, sd0, means1, sd1, faceCount) {
  pVals <- sapply(1:length(means0), function(i) {
    tTest <- t.test.from.summary.data(means0[i], sd0[i], faceCount, means1[i], sd1[i], faceCount)
    tTest$p.value
  })
  print(pVals)
  c(-2.0 * sum(log(pVals)), pchisq(-2.0 * sum(log(pVals)), df=2 * length(means0), lower.tail=FALSE))
}

##Significance tests : LRR vs No LRR, 0_0w vs best weight
#Cow
cow_noLRR_means <- c(
  11.196016853773362,
  11.571083502466742, 
  11.24780997117815
)
cow_noLRR_sd <- c(11.18089128143478, 11.629154409548905, 11.440828527427842)
cow_0_0w_means <- c(
  11.006295692453032,
  11.668258973932014,
  11.32135338589678
)
cow_0_0w_sd <- c(10.763826022003823, 11.89456895345606, 11.700143703429434)
cow_wNot0_means <- c(
  11.010460615302868,
  11.604761797940164,
  11.356546325254365
)
cow_wNot0_sd <- c(10.784691398383899, 11.900407850338972, 11.685480744050325)

testSignificanceRepeatedTests(cow_noLRR_means, cow_noLRR_sd, cow_0_0w_means, cow_0_0w_sd, cowFacesCount)
testSignificanceRepeatedTests(cow_wNot0_means, cow_wNot0_sd, cow_0_0w_means, cow_0_0w_sd, cowFacesCount)

#Log
log_noLRR_means <- c(
  12.844810200281644,
  13.79269790853962,
  13.963531985132942
)
log_noLRR_sd <- c(12.713262712734636, 14.310241143916443, 13.997412160924567)
log_0_0w_means <- c(
  10.645136301508826,
  11.131103489609528,
  10.747539165640948
)
log_0_0w_sd <- c(11.357545238446974, 12.559616943265764, 12.007902805550108)
log_wNot0_means <- c(
  10.642879352915799,
  11.130120083762401,
  10.745134970080725
)
log_wNot0_sd <- c(11.33468686989747, 12.557562969615402, 12.004966523056613)

testSignificanceRepeatedTests(log_noLRR_means, log_noLRR_sd, log_0_0w_means, log_0_0w_sd, logFacesCount)
testSignificanceRepeatedTests(log_wNot0_means, log_wNot0_sd, log_0_0w_means, log_0_0w_sd, logFacesCount)

#Mascaron
mascaron_noLRR_means <- c(
  15.1165390694907, 
  15.717699268326765, 
  16.045201138240003
)
mascaron_noLRR_sd <- c(12.55663675706313, 12.792305020836674, 13.34655298417345)
mascaron_0_0w_means <- c(
  14.230288603233769,
  14.37920311098936,
  14.56561024948353
)
mascaron_0_0w_sd <- rep(11.636795526939155, 11.569159914025636, 12.735828300042066)
mascaron_wNot0_means <- c(
  14.209295363101358,
  14.38758862572498,
  14.557426343540175
)
mascaron_wNot0_sd <- c(11.651392905046386, 11.585372026995968, 12.721262764506756)

testSignificanceRepeatedTests(mascaron_noLRR_means, mascaron_noLRR_sd, mascaron_0_0w_means, mascaron_0_0w_sd, mascaronFacesCount)
testSignificanceRepeatedTests(mascaron_wNot0_means, mascaron_wNot0_sd, mascaron_0_0w_means, mascaron_0_0w_sd, mascaronFacesCount)

#REAL test of significance (using repeated p-values)
mascaron_0_0w_means <- c(14.230288603233769, 14.37920311098936, 14.56561024948353)
mascaron_0_0w_sd <- c(11.636795526939155, 11.569159914025636, 12.735828300042066)
mascaron_0_01w_means <- c(14.209295363101358, 14.38758862572498, 14.557426343540175)
mascaron_0_01w_sd <- c(11.651392905046386, 11.585372026995968, 12.721262764506756)
mascaron_noLRF_means <- c(15.1165390694907, 15.717699268326765, 16.045201138240003)
mascaron_noLRF_sd <- c(12.55663675706313, 12.792305020836674, 13.34655298417345)

testSignificanceRepeatedTests(mascaron_0_0w_means, mascaron_0_0w_sd, mascaron_0_01w_means, mascaron_0_01w_sd, mascaronFacesCount)
testSignificanceRepeatedTests(mascaron_0_0w_means, mascaron_0_0w_sd, mascaron_noLRF_means, mascaron_noLRF_sd, mascaronFacesCount)

##On the LRR times
#Cow
cow_0_0w_means <- c(83.70483779907227, 82.45345306396484, 93.32482862472534) / cowFacesCount
cow_0_0w_sd <- c(0.03290814181669366, 0.03290814181669366, 0.03290814181669366)
cow_0_01w_means <- c(94.8536229133606, 74.42958068847656, 79.57779788970947) / cowFacesCount
cow_0_01w_sd <- c(0.03290814181669366, 0.03290814181669366, 0.03290814181669366)

testSignificanceRepeatedTests(cow_0_0w_means, cow_0_0w_sd, cow_0_01w_means, cow_0_01w_sd, cowFacesCount)

#Log
log_0_0w_means <- c(100.98757433891296, 92.12555193901062, 95.75744318962097) / logFacesCount#c(102.7813332080841, 127.54133367538452, 134.97315645217896, 100.98757433891296, 92.12555193901062, 95.75744318962097)
log_0_0w_sd <- c(0.03290814181669366, 0.03290814181669366, 0.03290814181669366)
log_0_01w_means <- c(79.18097996711731, 77.13677883148193, 69.38012266159058) / logFacesCount
log_0_01w_sd <- c(0.03290814181669366, 0.03290814181669366, 0.03290814181669366)

testSignificanceRepeatedTests(log_0_0w_means, log_0_0w_sd, log_0_01w_means, log_0_01w_sd, logFacesCount)

#Mascaron
mascaron_0_0w_means <- c(91.10781216621399, 113.03260111808777, 104.20079565048218) / mascaronFacesCount
mascaron_0_0w_sd <- c(0.03290814181669366, 0.03290814181669366, 0.03290814181669366)
mascaron_0_01w_means <- c(84.79101800918579, 89.23634266853333, 95.27992105484009) / mascaronFacesCount
mascaron_0_01w_sd <- c(0.03290814181669366, 0.03290814181669366, 0.03290814181669366)

testSignificanceRepeatedTests(mascaron_0_0w_means, mascaron_0_0w_sd, mascaron_0_01w_means, mascaron_0_01w_sd, mascaronFacesCount)

##Scores of denoising over time
png(filename = "img/scoreVsIteration.png", width = 450, height = 360)
  lwdUsed <- 2
  
  plotIts <- function(dataPerIts, color) {
    lines(x = 1:length(dataPerIts) - 1, y = dataPerIts, 
          type = "b", col = color, lwd = lwdUsed)
  }
  
  plot(NULL, xlim = c(0,8), ylim = c(10,30), 
       xlab = "Iteration number", ylab = "Average angular difference with the ground truth")
  
  #Cow
  cowPerfIts <- c(13.443814611907248, 10.986353250588095, 12.408438215490063,
                  13.709970076990086, 14.848936720281596, 15.812259961471755,
                  16.684694132371636, 17.45413778369777, 18.799647504705806)
  plotIts(cowPerfIts, "red")
  
  #Log
  logPerIts <- c(18.964159680532656, 14.385898587836655, 15.849574126984766,
                  17.47740789979116, 18.987527698581214, 20.356063037745315,
                 21.479649766654063, 22.568627314593286, 23.508926813389408)
  plotIts(logPerIts, "green")
  
  #Mascaron
  mascaronPerfsIts <- c(18.964159680532656, 13.77808881578137, 14.547348117627985, 
                        16.020280733838298, 17.47964076005213, 18.7320458774723,
                        19.78654685323554, 20.75851836032753, 22.385613394404626)
  plotIts(mascaronPerfsIts, "blue")
  
  legend("topleft", legend = c("Cow", "Log", "Mascaron"), col = c("red", "green", "blue"), lwd = lwdUsed)
dev.off()

#View spread of nuclear norms before recovery
library(readr)
library(dplyr)

readNucNorms <- function(filepath, color, weight) {
  ret <- as.matrix(read_csv(filepath, col_names = FALSE))
  print(mean(ret))
  print(sd(ret))
  print(quantile(ret))
  limX <- c(40, 250)
  hist(ret, breaks = seq(limX[1], limX[2], 5), 
       col = color,
       xlim = limX, ylim = c(0, 800), 
       xlab = "Initial nuclear norm",
       main = paste("w = ", toString(weight), sep = ""),
       cex.axis = 1.5, cex.main = 2.0, cex.lab = 1.5)
  
  normMean <- mean(ret)
  normSd <- sd(ret)
  allBreaks <- seq(limX[1], limX[2], length.out = 100)
  lines(allBreaks, 20000.0 * dnorm(allBreaks, normMean, normSd), col = "black", lwd = 3.0, lty = 4)
  
  ret
}


png(filename = "img/nucNormSpreads.png", width = 1000, height = 500)
  par(mfrow = c(2, 3))
  nucVals_0_0 <- readNucNorms("/home/home/thefamousrat/nucVals_0_0.csv", "red", 0.0)
  nucVals_0_1 <- readNucNorms("/home/home/thefamousrat/nucVals_0_1.csv", "red", 0.1)
  nucVals_0_5 <- readNucNorms("/home/home/thefamousrat/nucVals_0_5.csv", "red", 0.5)
  nucVals_1_0 <- readNucNorms("/home/home/thefamousrat/nucVals_1_0.csv", "red", 1.0)
  nucVals_10_0 <- readNucNorms("/home/home/thefamousrat/nucVals_10_0.csv", "red", 10.0)
  nucVals_100_0 <- readNucNorms("/home/home/thefamousrat/nucVals_100_0.csv", "red", 100.0)
dev.off()

#Nuclear norm vs LRR time)
library(readr)

loadLRRTimes <- function(filepath) {
  LRRTimeVsNucNorm <- as.data.frame(as.matrix(read_csv(filepath, col_names = FALSE)))
  LRRTimes <- 1000.0 * LRRTimeVsNucNorm[,2]
  LRRTimes <- sample(LRRTimes, size = 15000, replace = TRUE)
  confint(lm(LRRTimes ~ 1), level=0.95) - mean(LRRTimes)
}

setwd("/home/home/thefamousrat/LRRTimes/")

#Cow
loadLRRTimes("LRRTimeVsNucNorm_plastovaKrava_noisy_3_0_0w.csv")
loadLRRTimes("LRRTimeVsNucNorm_plastovaKrava_noisy_3_0_01w.csv")
loadLRRTimes("LRRTimeVsNucNorm_plastovaKrava_noisy_3_0_1w.csv")
loadLRRTimes("LRRTimeVsNucNorm_plastovaKrava_noisy_3_0_5w.csv")
loadLRRTimes("LRRTimeVsNucNorm_plastovaKrava_noisy_3_1_0w.csv")
loadLRRTimes("LRRTimeVsNucNorm_plastovaKrava_noisy_3_10_0w.csv")

#Log
loadLRRTimes("LRRTimeVsNucNorm_log1dec_noisy_3_0_0w.csv")
loadLRRTimes("LRRTimeVsNucNorm_log1dec_noisy_3_0_01w.csv")
loadLRRTimes("LRRTimeVsNucNorm_log1dec_noisy_3_0_1w.csv")
loadLRRTimes("LRRTimeVsNucNorm_log1dec_noisy_3_0_5w.csv")
loadLRRTimes("LRRTimeVsNucNorm_log1dec_noisy_3_1_0w.csv")
loadLRRTimes("LRRTimeVsNucNorm_log1dec_noisy_3_10_0w.csv")

#Mascaron
loadLRRTimes("LRRTimeVsNucNorm_mascaron_noisy_3_0_0w.csv")
loadLRRTimes("LRRTimeVsNucNorm_mascaron_noisy_3_0_01w.csv")
loadLRRTimes("LRRTimeVsNucNorm_mascaron_noisy_3_0_1w.csv")
loadLRRTimes("LRRTimeVsNucNorm_mascaron_noisy_3_0_5w.csv")
loadLRRTimes("LRRTimeVsNucNorm_mascaron_noisy_3_1_0w.csv")
loadLRRTimes("LRRTimeVsNucNorm_mascaron_noisy_3_10_0w.csv")

#Times for denoising step
vertUpdtTimes <- (1000.0 / mascaronFacesCount) * c(0.405670166015625, 0.44023585319519043, 0.43997907638549805, 0.4400310516357422, 0.43946099281311035)
mean(vertUpdtTimes)
1.96 * sd(vertUpdtTimes)

gnfTimes <- (1000.0 / mascaronFacesCount) * c(7.050998687744141, 7.292544364929199, 7.313310861587524, 7.129786252975464, 7.412519216537476)
mean(gnfTimes)
1.96 * sd(gnfTimes)