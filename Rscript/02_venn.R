source('/data_center_01/pipeline/16S_ITS_pipeline_v3.0/src/template/labels2colors.R')
library(VennDiagram)
library(grid)
X = read.table("@#{for_plot}",sep='\t',row.names=1,header=F,check.names=F,quote="")
group=read.table("@#{group_file}",header=F,row.names=1,check.names=F,quote="")

g = c()
for(i in 1:nrow(X)){
	a = X[i,]
	a = as.vector(a)
	a = strsplit(a,' ')
	g = c(g,a)
}
gnum = nrow(X)
colors=labels2colors(group[,1])
g1=unique(group)
g_order=g1[order(g1),1]
gcols=unique(colors)
gcols_order=gcols[order(g1)]
A=as.character(g_order)
tmp = cbind(A,gcols_order)
rownames(tmp)=A

if(gnum==2){
	group_name = c('@#{group_name1}','@#{group_name2}')
        gcols_order_finaly =tmp[group_name,2]
	venn.plot <- venn.diagram(
		x = list('@#{group_name1}'=g[1][[1]],'@#{group_name2}'=g[2][[1]]),
		filename = "@#{tiff_file}",
		col = "black",
		fill = gcols_order_finaly,
		cat.col = gcols_order_finaly,
		cat.cex = 1.5,
		cat.fontface = "bold",
		margin = 0.14
	)
}else if(gnum==3){
	group_name = c('@#{group_name1}','@#{group_name2}','@#{group_name3}')
        gcols_order_finaly =tmp[group_name,2]	
	venn.plot <- venn.diagram(
		x = list('@#{group_name1}'=g[1][[1]],'@#{group_name2}'=g[2][[1]],'@#{group_name3}'=g[3][[1]]),
		filename = "@#{tiff_file}",
		col = "black",
		fill = gcols_order_finaly,
		cat.col = gcols_order_finaly,
		cat.cex = 1.5,
		cat.fontface = "bold",
		margin = 0.14
	)	
}else if(gnum==4){
	group_name = c('@#{group_name1}','@#{group_name2}','@#{group_name3}','@#{group_name4}')
        gcols_order_finaly =tmp[group_name,2]
	venn.plot <- venn.diagram(
		x = list('@#{group_name1}'=g[1][[1]],'@#{group_name2}'=g[2][[1]],'@#{group_name3}'=g[3][[1]],'@#{group_name4}'=g[4][[1]]),
		filename = "@#{tiff_file}",
		col = "black",
		fill = gcols_order_finaly,
		cat.col = gcols_order_finaly,
		cat.cex = 1.5,
		cat.fontface = "bold",
		margin = 0.14
	)	
}else if(gnum==5){
	group_name = c('@#{group_name1}','@#{group_name2}','@#{group_name3}','@#{group_name4}','@#{group_name5}')
	gcols_order_finaly =tmp[group_name,2] 	
	venn.plot <- venn.diagram(
		x = list('@#{group_name1}'=g[1][[1]],'@#{group_name2}'=g[2][[1]],'@#{group_name3}'=g[3][[1]],'@#{group_name4}'=g[4][[1]],'@#{group_name5}'=g[5][[1]]),
		filename = "@#{tiff_file}",
		col = "black",
		fill = gcols_order_finaly,
		cat.col = gcols_order_finaly,
		cex = c(1.5, 1.5, 1.5, 1.5, 1.5, 1, 0.8, 1, 0.8, 1, 0.8, 1, 0.8,1, 0.8, 1, 0.55, 1, 0.55, 1, 0.55, 1, 0.55, 1, 0.55, 1, 1, 1, 1, 1, 1.5),
		cat.cex = 1.5,
		cat.fontface = "bold",
		margin = 0.14
	)	
}
