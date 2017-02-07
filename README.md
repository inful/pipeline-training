# pipeline-training


## Ruffus

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


In the example above only one decorator was used - *transform*. It is probably the most frequently used one in the variant calling pipeline too. ([here](http://www.ruffus.org.uk/tutorials/new_tutorial/transform.html) and [here](http://www.ruffus.org.uk/tutorials/new_tutorial/transform_in_parallel.html) are docs on it). Other decorators used in the pipeline are *@follows*, *@posttask*, *@mkdir*, *@jobs_limit*, *@merge / @collate* (merge several tasks' outputs, aka fan-in), and *@split / @subdivide* (fan-out). All *Ruffus* decorators are listed [here](http://www.ruffus.org.uk/decorators/decorators.html), and explained with examples in various chapters of the [manual](http://www.ruffus.org.uk/tutorials/new_tutorial/manual_contents.html). 

Go through the code of genotyping pipeline in GitLab, and note all decorators used. Read about them in the manual. Please note, that for every chapter in the manual there is example code you can use to play with the feature (as with the toy example pipeline above). I encourage you to do so:)


-----


In the previous step, you have probably encountered functions like *suffix*, *formatter*, *regex*, *add_inputs*. These are [indicators](http://www.ruffus.org.uk/decorators/indicator_objects.html) (as I just learned:) which help to manipulate decorator parameters (input/output names). Read about the ones you came across in the pipeline, especially *touch_file* and *formatter*. [Here](http://www.ruffus.org.uk/tutorials/new_tutorial/output_file_names_code.html) is example code for the more complicated formatter.


-----
