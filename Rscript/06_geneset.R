len <- read.table("gene_catalog.length", head = T, check.names = F, row.names = 1)
len[which(len[, 1] > 3000), ] = 3000
len = as.data.frame(len[which(len[, 1] > 100), ])
pdf("gene_catalog.length.pdf")
hist.result <- hist(len[, 1], breaks = 50, xlim = c(100, 3000), main = "Histogram of Length of Genes in Gene Catagory", xlab = "Length of Genes", ylab = "Number of Genes", col = "lightblue")
text(x = 3000, y = hist.result$counts[length(hist.result$counts)], labels = "length > 3000             ", pos = 3, offset = 0.5)
hist.result$counts[length(hist.result$counts)]
dev.off()
