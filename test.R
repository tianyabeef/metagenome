# venn <- function(A=A,B=B){
# source('/data_center_01/pipeline/16S_ITS_pipeline_v3.0/src/template/labels2colors.R')
# library(VennDiagram)
# library(grid)
# pdf("D:/Workspaces/metagenome/test.pdf")
# plot(A,B)
# dev.off()
# }
# myfunc = function(){
#   return(c(1,2,3,4,5,6,7,8,9,10))
# }
# 
# getname = function(){
#   return("chart title")
# }
library(MASS)
Iris <- data.frame(rbind(iris3[,,1], iris3[,,2], iris3[,,3]),
                   Sp = rep(c("s","c","v"), rep(50,3)))
train <- sample(1:150, 75)
table(Iris$Sp[train])
## your answer may differ
##  c  s  v
## 22 23 30
z <- lda(Sp ~ ., Iris, prior = c(1,1,1)/3, subset = train)
predict(z, Iris[-train, ])$class
