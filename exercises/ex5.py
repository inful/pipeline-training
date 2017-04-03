#
# Initial template shamelessly copied from
# http://www.ruffus.org.uk/tutorials/new_tutorial/introduction_code.html#new-manual-introduction-code
#
import os
import glob
from ruffus import *

# The starting data files would normally exist beforehand!
# We create some empty files for this example
starting_files = ["a_R1.fastq", "a_R2.fastq",
                  "b_R1.fastq", "b_R2.fastq",
                  "c_R1.fastq", "c_R2.fastq"]

raw_data_dir = 'raw_data'
if not os.path.isdir(raw_data_dir):
    os.mkdir(raw_data_dir)

for ff in starting_files:
    if not os.path.exists(ff):
        open(os.path.join(raw_data_dir, ff), "w")


#
# Exercise 5
#


@transform(glob.glob(os.path.join(raw_data_dir, '*.fastq')),
           formatter('.+/(?P<SAMPLE>[^/]+)_R(?P<READ>[12]).fastq'),
           '{subpath[0][1]}/{SAMPLE[0]}/{basename[0]}{ext[0]}',
           '{SAMPLE[0]}')
def organize_inputs(input_file, output_file, sample_name):
    # create sample dir if it does not exist
    if not os.path.isdir(sample_name):
        os.mkdir(sample_name)

    if not os.path.exists(output_file):
        os.symlink(os.path.join('..', input_file), output_file)


#
# Exercise 4
#
@collate(organize_inputs,
         regex('(.+)_R[12].fastq'),
         [r'\1.trimmed.fq1', r'\1.trimmed.fq2'])
def trim_reads(_, output_fastqs):
    for o in output_fastqs:
        open(o, 'w')


#
# Mapping fq1,fq2->sam
#
@transform(trim_reads, suffix('.trimmed.fq1'), '.sam')
def map_dna_sequence(input_files,
                     output_file):
    assert (len(input_files) == 2)
    open(output_file, "w")


#
# Compression sam->bam
#
@transform(map_dna_sequence,  # Input = previous stage
           suffix(".sam"),    # suffix = .sam
           ".bam")            # Output  suffix = .bam
def compress_sam_file(input_file,
                      output_file):
    open(input_file)
    open(output_file, "w")


#
# Statistics bam->statistics
#
@transform(compress_sam_file,   # Input = previous stage
           suffix(".bam"),      # suffix = .bam
           ".statistics",       # Output  suffix = .statistics
           "use_linear_model")  # Extra statistics parameter
def summarise_bam_file(input_file,
                       output_file):
    """
    Sketch of real analysis function
    """
    open(input_file)
    open(output_file, "w")


#
# Joint-call: bam, ... ,bam -> vcf
#
@merge(compress_sam_file, 'all_samples.vcf')
def joint_call_variants(input_bams, output_vcf):
    vcf = open(output_vcf, 'w')
    vcf.write('\n'.join([os.path.basename(f) for f in input_bams]))
    vcf.close()


#
# Split multisample VCF: vcf -> vcf,..., vcf
#
@split(joint_call_variants, '*/*.vcf')
def split_multisample_vcf(input_vcf, output_vcfs):
    # first cleanup after previous runs
    for f in output_vcfs:
        os.unlink(f)

    # next, read bam names from input VCF and create single sample vcfs
    with open(input_vcf) as f:
        for l in f.readlines():
            open('{sample}/{sample}.vcf'.format(sample=l.strip()[:-4]), 'w')


#
# Filter: vcf -> filtered.vcf
#
@transform(split_multisample_vcf, suffix('.vcf'), '.filtered.vcf')
def filter_single_sample_vcf(input_vcf, output_vcf):
    open(input_vcf)
    open(output_vcf, 'w')


pipeline_printout()
pipeline_run()
