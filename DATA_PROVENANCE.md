# Data provenance and visualisation rules

This portfolio build uses uploaded data and report tables only. No result values are invented.

## Xylanase project

Source files are the uploaded CSV exports. Counts, percentages and deltas shown in the app are calculated directly from those files.

- Negative FoldX ΔΔG is described as predicted stabilisation, not experimental proof.
- Integrated scores are shown as supplied in the candidate-ranking file.
- Molecular-dynamics temperature changes are calculated as 373 K minus 333 K.
- Boxplot outliers may be hidden in static images only to improve readability; underlying tables remain downloadable.

## Afelele project

Physicochemical values come from `01_physicochemical_numeric(1).csv`. Heavy-metal and taxonomy values were transcribed from the uploaded project report, specifically Table 4.1 and Figures/Appendix Tables 4.2-4.6.

- Surface-water concentrations use mg/L; sediment concentrations use mg/kg. They are not combined on one common quantitative axis.
- "ND" remains not detected and is not converted to zero.
- The physicochemical comparison image uses within-parameter normalisation only for visual pattern comparison. Actual means, standard deviations and units remain available in tables.
- Taxonomy visuals use reported sequence-read counts and percentages derived from those counts.

The project is presented as a research project in the public portfolio.


## RNA-seq workflow evidence

**Source:** `Book report.pdf` (uploaded biomedical-data analysis report).

Publicly represented evidence:

- six paired-end sample identifiers across two conditions;
- documented use of FastQC, Cutadapt, STAR, featureCounts, DESeq2 and Snakemake;
- DESeq2 console output reporting a 1,378-row result matrix with six standard result fields;
- source-generated MA plot;
- command-line and rule-based implementation screenshots.

Transformation rules:

- source screenshots were cropped only to improve legibility;
- the workflow overview and metric graphic summarise documented facts;
- no significant-gene counts, pathway claims or biological conclusions were inferred;
- the downloadable Snakemake package is labelled as a cleaned reusable template because original FASTQ, reference and full count/result files were not supplied.


## Breast cancer diagnostic data analysis

**Source:** `Breast_cancer_DS.xlsx` and the accompanying dashboard PDF supplied by the user. The workbook identifies the source as the UCI Machine Learning Repository.

Publicly represented evidence:

- 568 records actually present in the workbook;
- 357 benign and 211 malignant diagnoses;
- one missing `Area Mean` value, retained without imputation;
- no duplicate Patient IDs detected;
- descriptive group means and Pearson correlations calculated from the supplied rows;
- corrected Excel workbook and cleaned 568-row CSV.

Transformation rules:

- the unused constant `Column1` field was removed;
- the original `Risk - Level` field was renamed `Radius Band`;
- Radius Band is derived from Radius Mean: Low < 12, Medium 12 to < 14, High ≥ 14;
- the bands are descriptive only and are not presented as clinical risk scores;
- the original 569-record claim was replaced with the uploaded-row count of 568;
- the original `Average Radius Mean` KPI was removed because it displayed a sum rather than an average;
- no diagnosis model, prognosis, clinical prediction or patient-level recommendation was created.
