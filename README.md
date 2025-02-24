# MosamaticWeb4
New and simplified version of Mosamatic using Briefcase

# To-do
- CopyFilesTask: 
    - Figure out how to handle output fileset. Perhaps let task manager create it
      and pass it to task so it just has to copy the files to its directory. But 
      also, each file has to be explicitly added to the fileset. How do I do that?
      Perhaps the task can just return a list of files so the task manager can 
      build an output set from them. 
      https://chatgpt.com/c/67bc71bd-3b8c-800b-a195-0adbf595c609 
- DecompressDicomFilesTask
- RescaleDicomFilesTask
- MuscleFatSegmentationL3Task
- CalculateMetricsTask

# Done