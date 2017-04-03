#
#   Initial template shamelessly copied from http://www.ruffus.org.uk/tutorials/new_tutorial/introduction_code.html#new-manual-introduction-code
#

#   The starting data files would normally exist beforehand!
#       We create some empty files for this example
#
#

starting_files = ["a.fasta", "b.fasta", "c.fasta"]

import os

for ff in starting_files:
    if not os.path.exists(ff):
        open(ff, "w")

from ruffus import *


#
#   STAGE 1 fasta->sam
#
@transform(starting_files,   # Input = starting files
           suffix(".fasta"), # suffix = .fasta
           ".sam")           # Output  suffix = .sam
def map_dna_sequence(input_file,
                     output_file):
    ii = open(input_file)
    oo = open(output_file, "w")


#
#   STAGE 2 sam->bam
#
@transform(map_dna_sequence, # Input = previous stage
           suffix(".sam"),   # suffix = .sam
           ".bam")           # Output  suffix = .bam
def compress_sam_file(input_file,
                      output_file):
    ii = open(input_file)
    oo = open(output_file, "w")


#
#   STAGE 3 bam->statistics
#
@transform(compress_sam_file,  # Input = previous stage
           suffix(".bam"),     # suffix = .bam
           ".statistics",      # Output  suffix = .statistics
           "use_linear_model") # Extra statistics parameter
def summarise_bam_file(input_file,
                       output_file,
                       extra_stats_parameter):
    """
    Sketch of real analysis function
    """
    ii = open(input_file)
    oo = open(output_file, "w")


#
#   Exercise 2
#
@merge(compress_sam_file, 'all_samples.vcf')
def joint_call_variants(input_bams, output_vcf):
    vcf = open(output_vcf, 'w')
    vcf.write('\n'.join(input_bams))
    vcf.close()


#
#   Exercise 3
#
@split(joint_call_variants, 'Sample_*.vcf')
def split_multisample_vcf(input_vcf, output_vcfs):
    # first cleanup after previous runs
    for f in output_vcfs:
        os.unlink(f)

    # next, read bam names from input VCF and create single sample vcfs
    with open(input_vcf) as f:
        for l in f.readlines():
            open('Sample_%s.vcf' % l.strip(), 'w')


@transform(split_multisample_vcf, suffix('.vcf'), '.filtered.vcf')
def filter_single_sample_vcf(input_vcf, output_vcf):
    unfiltered = open(input_vcf)
    filtered = open(output_vcf, 'w')


pipeline_printout()
pipeline_run()
