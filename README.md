# pipeline-training


## Ruffus


### Intro

*Ruffus* website with rich documentation and learning resources is [here](http://www.ruffus.org.uk).
After reading the welcome message and the short summary of the framework, go to [Ruffus' simple tutorial](http://www.ruffus.org.uk/tutorials/new_tutorial/introduction.html). Reading it carefully will allow you to grasp basic elements of pipeline building with Ruffus, framework's vocabulary and syntax. [Install Ruffus](http://www.ruffus.org.uk/installation.html) and clone this repo to get the example from the simple tutorial (downloaded from [here](http://www.ruffus.org.uk/tutorials/new_tutorial/introduction_code.html#new-manual-introduction-code)). If the example works, try to break it:)

You can play for instance with:

1. changing file suffixes

2. removing selected intermediate or result files, and running the pipeline again (where all files recreated?)

3. testing parameters of [*pipeline_run*](http://www.ruffus.org.uk/pipeline_functions.html#pipeline-functions-pipeline-run) call at the end of the example script, e.g. specify to run task *compress_sam_file*, modify verbosity level to 3 and 5. See what happens.

4. inspecting the pipeline and state of the files by running pipeline_printout function [[6]](http://www.ruffus.org.uk/pipeline_functions.html#index-1) (try different verbosity levels and deleting selected intermediate files)

5. visualizing the pipeline with [*pipeline_printout_graph*](http://www.ruffus.org.uk/pipeline_functions.html#index-2)

6. adding a dummy variant calling task (.bam -> .vcf) and invoking the pipeline.

By now you should be able to know what decorators are, how to write a linear transformation pipeline in *Ruffus*, and how to run and view the pipeline. Now you can try to identify elements from the toy pipeline in the [early version of the variant calling pipeline](https://github.com/fsroque/NGS-pipeline/blob/master/pipeline_multisample.py) (browse to the end).


-----

### Decorators

In the example above only one decorator was used - *transform*. 
It is probably the most frequently used one in the variant calling pipeline too. 
([here](http://www.ruffus.org.uk/tutorials/new_tutorial/transform.html) and [here](http://www.ruffus.org.uk/tutorials/new_tutorial/transform_in_parallel.html) are docs on it). 
Other decorators used in the pipeline are *@follows*, *@posttask*, *@mkdir*, *@jobs_limit*, *@merge / @collate* (merge several tasks' outputs, aka fan-in), and *@split / @subdivide* (fan-out). 
All *Ruffus* decorators are listed [here](http://www.ruffus.org.uk/decorators/decorators.html), and explained with examples in various chapters of the [manual](http://www.ruffus.org.uk/tutorials/new_tutorial/manual_contents.html). 

Go through the code of genotyping pipeline in GitLab, and note all decorators used. Read about them in the manual. 
Please note, that for every chapter in the manual there is example code you can use to play with the feature (as with the toy example pipeline above). 
I encourage you to do so:) 

**Exercise 2**

Add a task to our toy pipeline to jointly call variants from all BAM files. The (mock) result should be written to a single file, e.g. abc.vcf. 

*Hint:* use *@merge* decorator

**Exercise 3**

Add a task to split the joint called VCF created in previous exercise into single-sample VCFs. And another task to filter each of these VCFs, e.g. a.vcf -> a.filtered.vcf.

-----

### Indicators

While learning decorators, you probably encountered functions like *suffix*, *formatter*, *regex*, *add_inputs*. 
These are [indicators](http://www.ruffus.org.uk/decorators/indicator_objects.html) (as I just learned:) which help to manipulate decorator parameters (input/output names). 
Read about the ones you came across in the pipeline. 
[Here](http://www.ruffus.org.uk/tutorials/new_tutorial/output_file_names_code.html) is an example code for a more complicated *formatter* construct.

**Exercise 4**

Let's upgrade to pair end sequencing. Replace each input fasta file with two, e.g. *a.fasta* with *a_R1.fastq* and *a_R2.fastq*. 
Add a trimming step that will take pairs of FASTQ files (R1 and R2) and output pairs of trimmed read files. 
Adjust the mapping step so that it takes pairs of fastq files.

*Hint*: you can use *@collate* and *regex/formatter* to bin the read-pairs

**Exercise 5**

We are creating now a substantial number of files. Let's organize them into folders. Refactor creation of FASTQ files so that they are all placed in one *raw_data/* directory. 
Now, add a task (*organize_inputs*) to copy or link the FASTQ files from for each sample from *raw_data/* into separate directory with sample's name e.g. a/ for files a_R1.fastq and a_R2.fastq. 

*Hint*: *Formatter* will let you extract sample name from the input filename

If your read-trimming task was written well, you won't need to change it. 
Depending on how you implemented the organizing task, input and output file names may now be absolute paths (this could break some of the implementations downstream). 
You can observe this by running pipeline_printout().
To finish separating files, reimplement splitting VCF to place single-sample VCFs into sample-specific folders.


-----

## Docker

The pipeline can use Docker containers to isolate pipeline components from each other.
Each component of the pipeline (a tool) can have its own Dockerfile which is essentially a script for Docker describing how to automatically build a minimal Docker container with the tool in it.
To learn more about Docker read the [Getting Started](https://docs.docker.com/engine/getstarted/) tutorial provided by Docker. 
Creating Dockerfiles is covered in [step four](https://docs.docker.com/engine/getstarted/step_four/) of the tutorial, but also [here](https://docs.docker.com/engine/reference/builder/). 

1. Create you own Dockerfile, build an image, and run a container. 

2. Run the container interactively (*docker run -ti*) attaching a folder from your machine (e.g. *-v /my/folder/path:/inside/docker/path:ro*)

3. Download [XHMM CNV variant caller](http://atgu.mgh.harvard.edu/xhmm/download.shtml) and install it in a Ubuntu Docker container. Note the steps needed (copying the XHMM archive, installing libs, building the executable).

4. Use the notes from (3) to make a Dockerfile describing how to build the XHMM image automatically. 
In the end it should be possible to get the 'usage message' from XHMM by invoking *docker run pipeline/xhmm xhmm*.

-----


## SLURM

SLURM is a job scheduling system that helps to balance the load on computational clusters. When using such a system, a user can schedule a large number of jobs (computations) without worrying about the overall load on the cluster. Provided with resource needs (memory, CPU) of a single job, a scheduling system will be able to queue jobs and distribute them to separate compute nodes, so that they thrive and don't overclutter the cluster. You can read more about SLURM [here](https://slurm.schedmd.com/quickstart.html).

There is a standard for communicating with job scheduling systems, such as *SLURM*. It is called *DRMAA*. *DRMAA* support is [built into Ruffus](http://www.ruffus.org.uk/tutorials/new_tutorial/multiprocessing.html#new-manual-ruffus-drmaa-wrapper-run-job), so Ruffus pipelines can use SLURM for job scheduling (provided it is installed and set up on the machine where the pipeline runs). A pipeline developer can flexibly switch between SLURM-scheduled jobs and locally executed tasks. From the user perspective, location of job execution is completely transparent. 

As a pipeline developer, you don't need to worry about SLURM setup so much. You will need a python *drmma* package installed and can schedule jobs using SLURM by using *drmaa_wrapper* as described [here](http://www.ruffus.org.uk/tutorials/new_tutorial/multiprocessing.html#new-manual-ruffus-drmaa-wrapper-run-job). The resource intensive jobs should be tagged with required figures of CPUs and memory. This is done in parameters of *drmaa_wrapper.run_job()* function. Similarly, you can provide other batch queuing parameters, such as walltime, account name, stdout and stderr files, etc. 

The *drmaa_wrapper* creates shell scripts that are temporarily saved on the file system (you can choose to keep them for debugging purpuses), and then passed on to SLURM for scheduling. Output and error streams from the execution are saved in local files, and printed on screen when running the pipeline. For example use, have a look at a wrapper function for executing commands in the pipeline - [*run_cmd* on line 422](https://github.com/seru71/ExomeSeqGenotypingPipeline/blob/dockerized/genotyping_pipeline.py)(line 422).





