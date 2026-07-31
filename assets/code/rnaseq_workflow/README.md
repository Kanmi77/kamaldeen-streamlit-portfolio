# Reproducible RNA-seq Workflow Template

This cleaned template packages the workflow stages documented in the portfolio evidence:

1. FastQC quality control
2. Cutadapt paired-end trimming
3. STAR reference indexing and alignment
4. featureCounts gene-level quantification
5. DESeq2 differential-expression analysis
6. Snakemake orchestration with a Conda environment

## Important scope note

The uploaded source report documents execution evidence, including a six-sample/two-condition setup, a 1,378-row DESeq2 result matrix and an MA plot. Raw FASTQ files, reference files and the full count matrix are not distributed in the public portfolio package. Therefore, this repository folder is a cleaned, reusable workflow template rather than a claim that the supplied template was rerun against those original files.

## Run

Place FASTQ and reference files at the paths specified in `config.yaml`, update sample metadata if required, then run:

```bash
snakemake --use-conda --cores 4
```

## Outputs

- FastQC reports
- trimmed paired-end reads
- coordinate-sorted STAR BAM files and logs
- featureCounts matrix
- DESeq2 result table
- MA plot
