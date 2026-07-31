#!/usr/bin/env Rscript
suppressPackageStartupMessages(library(DESeq2))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 4) {
  stop("Usage: Rscript deseq2.R <featureCounts.txt> <metadata.csv> <results.csv> <ma_plot.png>")
}

counts_file <- args[1]
metadata_file <- args[2]
results_file <- args[3]
ma_plot_file <- args[4]

fc <- read.delim(counts_file, check.names = FALSE, comment.char = "#")
count_data <- fc[, 7:ncol(fc), drop = FALSE]
rownames(count_data) <- fc$Geneid
colnames(count_data) <- sub(".*\\/", "", colnames(count_data))
colnames(count_data) <- sub("\\.Aligned\\.sortedByCoord\\.out\\.bam$", "", colnames(count_data))

metadata <- read.csv(metadata_file, row.names = 1, check.names = FALSE)
metadata <- metadata[colnames(count_data), , drop = FALSE]
stopifnot(identical(rownames(metadata), colnames(count_data)))
metadata$condition <- factor(metadata$condition)

dds <- DESeqDataSetFromMatrix(
  countData = round(as.matrix(count_data)),
  colData = metadata,
  design = ~ condition
)
dds <- dds[rowSums(counts(dds)) > 0, ]
dds <- DESeq(dds)
res <- results(dds)
res_df <- as.data.frame(res[order(res$padj), ])
res_df$gene_id <- rownames(res_df)
write.csv(res_df, results_file, row.names = FALSE)

png(ma_plot_file, width = 1200, height = 900, res = 150)
plotMA(res, alpha = 0.1, ylim = c(-8, 8))
dev.off()
