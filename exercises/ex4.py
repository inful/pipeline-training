#
#   Initial template shamelessly copied from http://www.ruffus.org.uk/tutorials/new_tutorial/introduction_code.html#new-manual-introduction-code
#

#   The starting data files would normally exist beforehand!
#       We create some empty files for this example
#
#

#
# Exercise4: extended the list of input files
#
starting_files = ["a_R1.fastq", "a_R2.fastq", 
		  "b_R1.fastq", "b_R2.fastq",
		  "c_R1.fastq", "c_R2.fastq"]

import os
for ff in starting_files:
    if not os.path.exists(ff):
	open(ff, "w")


from ruffus import *


#
#   Exercise 4
#
@collate(starting_files, 
	regex('(.+)_R[12].fastq'), 
	[r'\1.trimmed.fq1', r'\1.trimmed.fq2'])
def trim_reads(input_fastqs, output_fastqs):
    for o in output_fastqs:
        open(o,'w')
	

#
#   Mapping fq1,fq2->sam
#
@transform(trim_reads, suffix('.trimmed.fq1'), '.sam')
def map_dna_sequence(input_files,
                    output_file):
    assert(len(input_files) == 2)
    oo = open(output_file, "w")

#
#   Compression sam->bam
#
@transform(map_dna_sequence,                   # Input = previous stage
            suffix(".sam"),                    #         suffix = .sam
            ".bam")                            # Output  suffix = .bam
def compress_sam_file(input_file,
                      output_file):
    ii = open(input_file)
    oo = open(output_file, "w")

#
#   Statistics bam->statistics
#
@transform(compress_sam_file,                  # Input = previous stage
            suffix(".bam"),                    #         suffix = .bam
            ".statistics",                     # Output  suffix = .statistics
            "use_linear_model")                # Extra statistics parameter
def summarise_bam_file(input_file,
                       output_file,
                       extra_stats_parameter):
    """
    Sketch of real analysis function
    """
    ii = open(input_file)
    oo = open(output_file, "w")


#
#   Joint-call: bam, ... ,bam -> vcf
#
@merge(compress_sam_file, 'all_samples.vcf')
def joint_call_variants(input_bams, output_vcf):
    vcf = open(output_vcf, 'w')
    vcf.write('\n'.join(input_bams))
    vcf.close()

#
#   Split multisample VCF: vcf -> vcf,..., vcf
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

#
# Filter: vcf -> filtered.vcf
#
@transform(split_multisample_vcf, suffix('.vcf'), '.filtered.vcf')
def filter_single_sample_vcf(input_vcf, output_vcf):
    unfiltered = open(input_vcf)	
    filtered   = open(output_vcf, 'w')


pipeline_run()
