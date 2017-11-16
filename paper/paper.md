---
title: 'Retriever: Data Retrieval Tool'
tags:
  - data retrieval, data processing, python, data, data science, datasets
authors:
 - name: Henry Senyondo
   orcid: 0000-0001-7105-5808
   affiliation: 1
 - name: Benjamin D. Morris
   orcid: 0000-0003-4418-1360
 - name: Akash Goel
   orcid: 0000-0001-9878-0401
   affiliation: 3
 - name: Andrew Zhang
   orcid: 0000-0003-1148-7734
   affiliation: 4
 - name: Akshay Narasimha
   orcid: 0000-0002-3901-2610
   affiliation: 5
 - name: Shivam Negi
   orcid: 0000-0002-5637-0479
   affiliation: 6
 - name: David J. Harris
   orcid: 0000-0003-3332-9307
   affiliation: 4
 - name: Deborah Gertrude Digges
   orcid: 0000-0002-7840-5054
   affiliation: 10
 - name: Kapil Kumar
   orcid: 0000-0002-2292-1033
   affiliation: 7
 - name: Amritanshu Jain
   orcid: 0000-0003-1187-7900
   affiliation: 5
 - name: Kunal Pal
   orcid: 0000-0002-9657-0053
   affiliation: 8
 - name: Kevinkumar Amipara
   orcid: 0000-0001-5021-2018
   affiliation: 9
 - name : Prabh Simran Singh Baweja
   orcid: 0000-0003-3997-4470
 - name: Ethan P. White
   orcid: 0000-0001-6728-7745
   affiliation: 1, 2
affiliations:
 - name: Department of Wildlife Ecology and Conservation, University of Florida
   index: 1
 - name: Informatics Institute, University of Florida
   index: 2
 - name: Delhi Technological University, Delhi
   index: 3
 - name: The University of Florida
   index: 4
 - name: Birla Institute of Technology and Science, Pilani
   index: 5
 - name: Manipal Institute of Technology, Manipal
   index: 6
 - name: National Institute of Technology, Delhi
   index: 7
 - name: RWTH Aachen University, Aachen, Germany
   index: 8
 - name: Sardar Vallabhbhai National Institute of Technology, Surat
   index: 9
 - name: PES Institute of Technology, Bengaluru
   index: 10


date: 16 September 2017 
bibliography: paper.bib
---

# Summary

The Data Retriever automates the first steps in the data analysis workflow by downloading, cleaning, and standardizing tabular datasets, and importing them into relational databases, flat files, or programming languages [@Morris2013]. The automation of this process reduces the time for a user to get most large datasets up and running by hours to days.The retriever uses a plugin infrastructure for both datasets and storage backends. New datasets that are relatively well structured can be added adding a JSON file following the Frictionless Data tabular data metadata package standard [@frictionlessdata_specs]. More complex datasets can be added using a Python script to handle complex data cleaning and merging tasks and then defining the metadata associated with the cleaned tables. New storage backends can be added by overloading a general class with details for storing the data in new file formats or database management systems. The retriever has both a Python API and a command line interface. An R package that wraps the command line interface and a Julia package that wraps the Python API are also available.

The 2.0 and 2.1 releases add extensive new functionality. This includes the Python API, the use of the Frictionless Data metadata standard, Python 3 support, JSON and XML backends, and autocompletion for the command line interface.

# References