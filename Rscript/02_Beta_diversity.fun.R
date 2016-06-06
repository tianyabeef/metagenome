Dist <- function(profile.data, method){
	dist.data <- tryCatch(dist(profile.data, method = method), error = function(e) {NA});
	if (class(dist.data) == "dist"){
		dist.data;
	}else {
		library(vegan);
		vegdist(profile.data, method = method);
	}
}
Anosim <- function(dist.data, sample.list, method){
	library(vegan);
	anosim.data <- anosim(dist.data, sample.list, permutations = 9999);
	class.dist  <- anosim.data$class.vec;
	names.class <- c(attr(class.dist, "levels")[which(attr(class.dist, "levels") != "Between")], "Between");
	cols.class  <- c(topo.colors(length(names.class) - 1), "orange");
	class.dist  <- factor(class.dist, levels = names.class);
	pdf(paste(method, ".anosim.box.pdf", sep = ""));
	boxplot(dist.data ~ class.dist, pch = 20, col = cols.class,
		ylim = c(min(dist.data), max(dist.data) * 1.1),
		main = paste("Distance of", method, "within and between groups"));
	text(x = length(names.class), y = max(dist.data) * 1.05, adj = 1,
	     labels = paste("P-value of anosim:", anosim.data$signif));
	dev.off();
	anosim.info <- c(anosim.data$statistic, anosim.data$signif)
	cat(anosim.data$statistic)
	write(anosim.info, file = paste(method, ".anosim.tsv", sep = ""))
}
Nmds <- function(dist.data, sample.list, method){
	library(vegan);
	nmds <- metaMDS(dist.data);
	pdf(paste(method, ".nmds.pdf", sep = ""));
	layout(matrix(c(1,1,1,3,
			1,1,1,3,
			1,1,1,3,
			2,2,2,0), byrow = T, ncol = 4));
	if (length(attr(sample.list,"levels")) > 7) {
	  col.sample <- topo.colors(length(attr(sample.list,"levels")))
	}else {
	  col.sample <- c("lightblue", "salmon", "orange", "lightpink", "seagreen", "orchid", "royalblue")
	}
	par(mar = c(5, 5, 5, 5));
	if (length(sample.list) <= 10) {
	  nmds.cex <- 4
	}else if (length(sample.list) <= 30){
	  nmds.cex <- 2
	}else {
	  nmds.cex <- 1
	}
	plot(nmds$points, pch = 20, col = col.sample[sample.list],
	     main = paste("NMDS by distance of", method, "between samples"),
	     xlab = "NMDS1", ylab = "NMDS2",
	     cex = nmds.cex)
	if (length(sample.list) <= 10) {
	  for (i in 1 : length(sample.list)){
	    text(x = nmds$points[i, 1], y = nmds$points[i, 2], labels = labels(dist.data)[i], xpd = T)
	  }
	}
	par(mar = c(3, 5, 2, 5));
	boxplot(nmds$points[,1] ~ sample.list, pch = 20, col = col.sample, notch = F, horizontal = T);
	par(mar = c(5, 2, 5, 3));
	boxplot(nmds$points[,2] ~ sample.list, pch = 20, col = col.sample, notch = F);
	dev.off();
}
Pcoa <- function(dist.data, sample.list, method){
	library(ade4);
	pcoa <- dudi.pco(dist.data, scannf = F, nf = 2);
	pdf(paste(method, ".pcoa.pdf", sep = ""));
	layout(matrix(c(1,1,1,3,
			1,1,1,3,
			1,1,1,3,
			2,2,2,0), byrow = T, ncol = 4));
	if (length(attr(sample.list,"levels")) > 7) {
	  col.sample <- topo.colors(length(attr(sample.list,"levels")));
	}else {
	  col.sample <- c("lightblue", "salmon", "orange", "lightpink", "seagreen", "orchid", "royalblue")
	}
	par(mar = c(5, 5, 5, 5));
	pcoa.eig <- signif(pcoa$eig, digits = 3);
	if (length(sample.list) <= 10) {
	  pcoa.cex <- 4
	}else if (length(sample.list) <= 30){
	  pcoa.cex <- 2
	}else {
	  pcoa.cex <- 1
	}
	plot(pcoa$li, pch = 20, col = col.sample[sample.list],
	     main = paste("PCoA by distance of", method, "between samples"),
	     xlab = paste("PCoA1: ", pcoa.eig[1] * 100, "%", sep = ""),
	     ylab = paste("PCoA2: ", pcoa.eig[2] * 100, "%", sep = ""),
	     cex = pcoa.cex)
	if (length(sample.list) <= 10) {
	  for (i in 1 : length(sample.list)){
	    text(x = pcoa$li[i, 1], y = pcoa$li[i, 2], labels = labels(dist.data)[i], xpd = T)
	  }
	}
	par(mar = c(3, 5, 2, 5));
	boxplot(pcoa$li[,1] ~ sample.list, pch = 20, col = col.sample, notch = F, horizontal = T);
	par(mar = c(5, 2, 5, 3));
	boxplot(pcoa$li[,2] ~ sample.list, pch = 20, col = col.sample, notch = F);
	dev.off();
}
