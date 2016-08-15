species.profile <- read.table("../profile/species.profile", head = T, check.names = F)
genus.profile   <- read.table("../profile/genus.profile",   head = T, check.names = F)
phylum.profile  <- read.table("../profile/phylum.profile",  head = T, check.names = F)
species.phylum  <- read.table("species.phylum",     head = F, check.names = F, row.names = 1)
genus.phylum    <- read.table("genus.phylum",       head = F, check.names = F, row.names = 1)
group.list      <- read.table(@#{group},head = F, check.names = F, row.names = 1)

topplot <- function(species.profile, genus.profile, phylum.profile, species.phylum, genus.phylum, pdf.file){
  species.profile <- species.profile[rev(order(apply(species.profile, 1, median)))[1 : 20], ]
  genus.profile <- genus.profile[rev(order(apply(genus.profile, 1, median)))[1 : 15], ]
  phylum.profile <- phylum.profile[rev(order(apply(phylum.profile, 1, median)))[1 : 4], ]
  phylum.profile <- rbind(phylum.profile, 1 - apply(phylum.profile, 2, sum))
  rownames(phylum.profile)[5] <- "Others"
  color.phylum <- c("salmon", "seagreen", "orange", "royalblue", "lightpink")
  names(color.phylum) = rownames(phylum.profile)
  species.phylum <- as.vector(species.phylum[rownames(species.profile), 1])
  species.phylum[-which(species.phylum %in% rownames(phylum.profile))] = "Others"
  #  cat(colnames(phylum.profile))
  color.species <- color.phylum[species.phylum]
  genus.phylum <- as.vector(genus.phylum[rownames(genus.profile), 1])
  genus.phylum[-which(genus.phylum %in% rownames(phylum.profile))] = "Others"
  color.genus <- color.phylum[genus.phylum]
  pdf(pdf.file, height = 10, width = 10)
  layout(matrix(c(1, 2, 2,
                  3, 3, 3), ncol = 3, byrow = T))
  # phylum
  par(mar = c(15, 5, 4, 4))
  boxplot(t(phylum.profile), cex = 0.5, pch = 19, col = color.phylum, xaxt="n")
  points(x = (1 : nrow(phylum.profile)), y = apply(phylum.profile, 1, mean), pch = 3, cex = 0.5)
  axis(1, labels = FALSE, at = (1 : nrow(phylum.profile)))
  text(labels = rownames(phylum.profile), x = (1 : nrow(phylum.profile)), y = rep((min(phylum.profile) - max(phylum.profile)) / 10, nrow(phylum.profile)), srt = 45, xpd = T, adj = 1)
  # genus
  par(mar = c(15, 0, 4, 2))
  boxplot(t(genus.profile), cex = 0.5, pch = 19, col = color.genus, xaxt="n")
  points(x = (1 : nrow(genus.profile)), y = apply(genus.profile, 1, mean), pch = 3, cex = 0.5)
  axis(1, labels = FALSE, at = (1 : nrow(genus.profile)))
  text(labels = rownames(genus.profile), x = (1 : nrow(genus.profile)), y = rep((min(genus.profile) - max(genus.profile)) / 10, nrow(genus.profile)), srt = 45, xpd = T, adj = 1)
  # species
  par(mar = c(15, 5, 1, 2))
  boxplot(t(species.profile), cex = 0.5, pch = 19, col = color.species, xaxt="n")
  points(x = (1 : nrow(species.profile)), y = apply(species.profile, 1, mean), pch = 3, cex = 0.5)
  axis(1, labels = FALSE, at = (1 : nrow(species.profile)))
  text(labels = rownames(species.profile), x = (1 : nrow(species.profile)), y = rep((min(species.profile) - max(species.profile)) / 10, nrow(species.profile)), srt = 45, xpd = T, adj = 1)
  dev.off()
}

topplot(species.profile, genus.profile, phylum.profile, species.phylum, genus.phylum, pdf.file = @#{pdfoutput})
for (grp in levels(group.list[, 1])){
  samples <- rownames(group.list)[which(group.list[, 1] == grp)]
  species.profile.grp <- species.profile[, samples]
  #cat(rownames(species.profile.grp))
  genus.profile.grp   <- genus.profile[, samples]
  phylum.profile.grp  <- phylum.profile[, samples]
  topplot(species.profile.grp, genus.profile.grp, phylum.profile.grp, species.phylum, genus.phylum, pdf.file = paste("top", grp, "pdf", sep = "."))
}