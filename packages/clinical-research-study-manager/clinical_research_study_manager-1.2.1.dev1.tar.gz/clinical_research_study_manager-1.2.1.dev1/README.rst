Clinical Research Study Manager
===============================

Program to manage some common clinical research task from the command
line

Getting Started
---------------

This program requires python 3 and a few external packages.

Prerequisites
~~~~~~~~~~~~~

Requires python and above

::

    $ python 3.5


    $ pip install openpyxl
    $ pip install pandas
    $ pip install numpy
    $ pip install matplotlib

Installing
~~~~~~~~~~

::

    $ pip install clinical_research_study_manager

Get Help

::

    $ clinical_research_study_manager -h
    optional arguments:
      -h, --help            show this help message and exit
      -create_project Project_Name
                            Creates a new project titled Project_Name in the
                            Projects directory
      -load_project Project_Name
                            Loads Project Project_Name from the Projects directory
                            for study activities
      -list_projects        List available projects to load

Create New Project

::

    $ clinical_reseaerch_study_manager -create_project Testing
    Creating new project titled Testing
    Created patient_data[phi] for project Testing at /home/beliefs22/Clinical_Research_Manager_Projects/Projects/Testing
    Created patient_data[de_identified] for project Testing at /home/beliefs22/Clinical_Research_Manager_Projects/Projects/Testing
    Created logs for project Testing at /home/beliefs22/Clinical_Research_Manager_Projects/Projects/Testing
    Created logs/logs_with_phi for project Testing at /home/beliefs22/Clinical_Research_Manager_Projects/Projects/Testing
    Created data_visualization for project Testing at /home/beliefs22/Clinical_Research_Manager_Projects/Projects/Testing
    Created log files for project Testing
    Created Screening_Log.xlsx log for Testing at /home/beliefs22/Clinical_Research_Manager_Projects/Projects/Testing/logs/Screening_Log.xlsx
    Created Master_Linking_Log.xlsx log for Testing at /home/beliefs22/Clinical_Research_Manager_Projects/Projects/Testing/logs/logs_with_phi/Master_Linking_Log.xlsx
    Created Follow_Up_Log.xlsx log for Testing at /home/beliefs22/Clinical_Research_Manager_Projects/Projects/Testing/logs/Follow_Up_Log.xlsx
    Created Enrollment_Log.xlsx log for Testing at /home/beliefs22/Clinical_Research_Manager_Projects/Projects/Testing/logs/Enrollment_Log.xl

Load Specific Project

::


    $ clinical_research_study_manager -load_project Testing
    Opening Testing
    1. Manage Logs
    2. Query Logs
    Please choose what actions you would like to take, q to quit.

List Available Projects

::

    $ clinical_research_study_manager -list_projects
    Current Projects are:
    1 : Testing

Running the tests
-----------------

Coming Soon

Break down into end to end tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Explain what these tests test and why

::

    Coming Soon

And coding style tests
~~~~~~~~~~~~~~~~~~~~~~

Coming Soon

::

    Coming Soon

Authors
-------

**Seth Pitts**

License
-------

This project is licensed under the MIT License - see the `LICENSE.txt`_
file for details

.. _LICENSE.txt: LICENSE.txt