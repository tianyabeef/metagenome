source("/data_center_01/pipeline/huangy/metagenome/Rscript/labels2colors.R")
library("grid");
library("VennDiagram");
args <- commandArgs("T")
print(args)
data <- read.table(args[1], header = T, check.names = F,quote="",row.names=1,sep="\t")
group <- read.table(args[2],header=F,check.names=F,quote="",row.names=1,sep="\t")
data = data[,rownames(group)]
color_list = group2corlor(group)
sample_colors = color_list[[1]]
group_colors = color_list[[2]]
group_names = color_list[[3]]
group = color_list[[4]]

  
rnames = rownames(data)
#print(class(data))
#data = as.data.frame(data)
#print(class(data))
numberlist = as.list(data)
modifylist <-function(list){
  numberlistnames = names(list)
  newlist = list()
  for (i in numberlistnames){
    newlist[[i]] = rnames[which(list[[i]] > 0)]
  }
  newlist
}
  
newlist = modifylist(numberlist)
#profile[which(profile > 0)]  <- 1
#f <- function(x, y){
#  y[which(x != 0)]
#}
#list.venn <- lapply(profile, f, y = rownames(profile))
#col = c("red", "yellow", "green", "blue", "purple", "orange")
i = ncol(data)
venn.diagram(newlist, imagetype = "png", fill = group_colors, paste("venn", i, "png", sep = "."), margin = 0.05);
