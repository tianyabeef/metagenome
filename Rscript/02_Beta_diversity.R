arg <- commandArgs("T");
if (length(arg) != 4){
	stop("argument number error:\n
	      $0 <fun.rscript> <profile> <group> <method>\n");
}
fun.Rscript  <- arg[1];
profile.file <- arg[2];
group.file   <- arg[3];
method       <- arg[4];
source(fun.Rscript);
profile.data <- read.table(profile.file, check.names = F, header = T,sep="\t",quote="",row.names=1);
sample.group <- read.table(group.file,   check.names = F, row.names = 1,sep="\t",quote="");
profile.data <- profile.data[,rownames(sample.group)]
dist.data    <- Dist(t(profile.data), method = method);
Anosim(dist.data, sample.group[,1], method = method);
Nmds(  dist.data, sample.group[,1], method = method);
Pcoa(  dist.data, sample.group[,1], method = method);
