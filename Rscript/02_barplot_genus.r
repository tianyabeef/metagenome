tax_level="genus"
profile <- read.table("../profile/genus.profile", header = T, check.names = F,quote="",sep="\t",row.names=1);
number  <- 15;
## reorder
#neworder = as.character(unlist(read.table("species/top20/20150717/bar/sample.order.list")))
#profile = profile[, neworder]
## unknown change
#colnames(profile) = gsub("M", "m", colnames(profile))
## reorder taxonomy
rowsums <- rowSums(profile);
profile <- as.matrix(profile[order(-rowsums), ]);
for (i in colnames(profile)){
	order  <- rev(order(profile[, i]));
	number <- min(number, length(order));
	profile[-(order[1:number]), i] <- 0;
}
Others  <- 1 - apply(profile, 2, sum);
profile <- rbind(profile, Others);
profile <- profile[which(apply(profile, 1, sum) > 0), ];
profile <- as.matrix(profile);
## picture parameters
palette <- c("red",        "gray",          "cornflowerblue", "chartreuse3",
	     "yellow",     "honeydew4",     "indianred4",     "khaki",
	     "lightblue1", "lightseagreen", "lightslateblue", "magenta",
	     "blue",       "orange2",       "purple",         "black");
color <- colorRampPalette(palette, interpolate = "spline", space = "Lab");
space <- 0.5;
width <- 2;
## calculate size

## draw picture
pdf("genus.barplot.pdf", height = 15, width = 15);
layout(matrix(c(1, 2), nrow = 2));
par(oma   = c(2, 2, 2, 2),
    mar   = c(5, 5, 5, 5));
#barplot(table, col = colorvector(colornumber), xaxt = "n", space = spa, width = width)
if (ncol(profile) > 15) {
  barplot(profile, col = color(nrow(profile)), space = space, width = width, las = 2)
}else {
  barplot(profile, col = color(nrow(profile)), space = space, width = width)
}
#text(seq(from = width - 0.3,length = ncol(profile), by=2 * space + width),par("usr")[3] - 0.15,srt=90,adj=0.5,labels=gsub("^Q", "", colnames(table)),xpd=T,font=1,cex=2, pos = 1)
mtext("15 Main Genus in Each Sample", side = 3, line = 1, cex = 2)
## legend
par(mar   = c(5, 5, 2, 5));
plot(0, type = "n", xaxt = "n", yaxt = "n", bty ="n", xlab = "", ylab = "");
legend("top", pch = 15, col = rev(color(nrow(profile))), legend = rev(rownames(profile)), bty = "n", pt.cex = 2, ncol = 3);
#text(seq(from = spa+0.5*width - 0.1,length = ncol(table), by=spa + width),par("usr")[3] - 0.06,srt=90,adj=0.5,labels=new_order,xpd=T,font=1,cex=0.9, pos = 1)
#mtext(title,side=3,line=1)
dev.off();

