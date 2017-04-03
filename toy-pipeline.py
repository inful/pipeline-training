#
# Shamelessly copied from
# http://www.ruffus.org.uk/tutorials/new_tutorial/introduction_code.html#new-manual-introduction-code
#
from ruffus import *

# The starting data files would normally exist beforehand!
# We create some empty files for this example
starting_files = ["a.fasta", "b.fasta", "c.fasta"]

for ff in starting_files:
    open(ff, "w")


#
# STAGE 1 fasta->sam
#
@transform(starting_files,    # Input = starting files
           suffix(".fasta"),  # suffix = .fasta
           ".sam")            # Output  suffix = .sam
def map_dna_sequence(input_file,
                     output_file):
    open(input_file)
    open(output_file, "w")


#
# STAGE 2 sam->bam
#
@transform(map_dna_sequence,  # Input = previous stage
           suffix(".sam"),    # suffix = .sam
           ".bam")            # Output  suffix = .bam
def compress_sam_file(input_file,
                      output_file):
    open(input_file)
    open(output_file, "w")


#
# STAGE 3 bam->statistics
#
@transform(compress_sam_file,   # Input = previous stage
           suffix(".bam"),      # suffix = .bam
           ".statistics",       # Output  suffix = .statistics
           "use_linear_model")  # Extra statistics parameter
def summarise_bam_file(input_file,
                       output_file,
                       extra_stats_parameter):
    """
    Sketch of real analysis function
    """
    open(input_file)
    open(output_file, "w")

#
# 1. Add a dummy variant calling task (.bam -> .vcf)
#

@transform(compress_sam_file,
           suffix(".bam"),
           ".vcf")
def variant_calling(input_file,
                    output_file):
    open(input_file)
    open(output_file, "w")

#
# 2. Add a task to our toy pipeline to jointly call variants from all BAM files. The (mock) result should
# be written to a single file, e.g. abc.vcf.
#

@merge(compress_sam_file, 'abc.vcf')
def jointly_call_variants(input_files, output_file):
    out=open(output_file,"w")
    out.write('\n'.join(input_files))


#
# 3. Add a task to split the joint called VCF created in previous exercise into single-sample VCFs.
# And another task to filter each of these VCFs, e.g. a.vcf -> a.filtered.vcf.
@split(jointly_call_variants,'*.vcf')
def split_vcf(input_file, output_files):
    input = open(input_file).read().split('\n')
    for o in input:
        open(o.split('.')[0]+'.vcf',"w")


@transform(split_vcf,
           suffix(".vcf"),
           ".filtered.vcf")
def filter_vcf(input_file, output_file):
    open(output_file,"w")
#
# 4. Let's upgrade to pair end sequencing. Replace each input fasta file with two,
# e.g. *a.fasta* with *a_R1.fastq* and *a_R2.fastq*.
# Add a trimming step that will take pairs of FASTQ files (R1 and R2) and output pairs of trimmed read files.
# Adjust the mapping step so that it takes pairs of fastq files.
# *Hint*: you can use *@collate* and *regex/formatter* to bin the read-pairs
#

@split(starting_files,
       '*.fastq')
def create_fastq(input,output):
    for i in input:
        print i
        open(i.split('.')[0] + '_R1.fastq', "w")
        open(i.split('.')[0] + '_R2.fastq', "w")


@collate(create_fastq, regex(r"(.+)_R.\.(.+)$"), r'\1.read')
def trim_read(infiles, output):
    open(output,"w")

#
# 5. We are creating now a substantial number of files. Let's organize them into folders.
# Refactor creation of FASTQ files so that they are all placed in one *raw_data/* directory.
# Now, add a task (*organize_inputs*) to copy or link the FASTQ files from for each sample from *raw_data/* into
# separate directory with sample's name e.g. a/ for files a_R1.fastq and a_R2.fastq.
# *Hint*: *Formatter* will let you extract sample name from the input filename
# To finish separating files, reimplement splitting VCF to place single-sample VCFs into sample-specific folders.
#


pipeline_run()
