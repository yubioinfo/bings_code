library(tools)

args=commandArgs(T)

if(length(args) == 0 ){

cat("Usage: Rscript install_Rpkg.R package1 package2 package3 ...")
cat("\n")
quit("no")

}

path <- c("/work/software/R/contrib")

install.packages(args, contriburl=paste("file:",path,sep=''),type="source")