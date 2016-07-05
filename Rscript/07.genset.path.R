data = read.table("geneset.path.class",sep="\t",check.names = F,header = T,quote="")
data2=as.matrix(data[,4])
rownames(data2)=data[,2]
num = length(unique(factor(data[,1])))
sample_colors=rainbow(num)[factor(data[,1])]
group_colors=rainbow(num)
pdf("path.pdf",width = 10,height = 6)
#layout(mat = rbind(c(2,1)),widths = c(0.2,1),heights = 1)
par(oma = c(1,3,1,1),mar = c(1,20,0,1))
tt =barplot(t(data[,4]),horiz = T,col = sample_colors,beside = T)
text(-2,tt,labels =data[,2],xpd=T,adj = 1,col = sample_colors)
legend("topright",legend = unique(factor(data[,1])),col = group_colors,pch = 17)
dev.off()
