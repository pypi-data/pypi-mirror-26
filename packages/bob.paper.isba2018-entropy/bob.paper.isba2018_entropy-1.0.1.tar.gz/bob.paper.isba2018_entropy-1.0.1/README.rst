==========================================================================================
Towards Quantifying the Entropy of Fingervein Patterns across Different Feature Extractors
==========================================================================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It contains the source code to reproduce the following paper::


    @inproceedings{Krivokuca_ISBA2018_2018,
              title = {Towards Quantifying the Entropy of Fingervein Patterns across Different Feature Extractors},
             author = {Krivoku{\'{c}}a, Vedrana and Marcel, S{\'{e}}bastien},
          booktitle = "{2018 IEEE 4th International Conference on Identity, Security, and Behavior Analysis (ISBA)}",
              month = "Jan",
               year = {2018}
    }

If you use this package and/or its results, please cite both the package and the corresponding paper_.  Also, please ensure that you include the two original Bob references (Bob_) in your citations.


Software Installation
---------------------

The first thing you must do is to install all the required software to reproduce the experiments in this paper.  Note that the installation instructions are based on conda_ and that we offer pre-compiled binary installations of Bob using conda for Linux and MacOS 64-bit operating systems only.  Windows, as well as 32-bit architectures, are currently not supported.  Keeping this in mind, proceed with the installation as follows:

1. `Install Miniconda`_.
2. Download the paper source code and extract the files into your working directory.
3. Navigate to your working directory as follows:

   .. code-block:: sh

      $ cd [path_to_your_working_directory]

4. Install the paper source code and create a conda environment containing all the necessary package dependencies, using the following command:

   .. code-block:: sh

      $ conda env create -f environment.yml

5. Activate the environment as follows:

   .. code-block:: sh

      $ source activate bob.paper.isba2018_entropy.env


Downloading the Databases
-------------------------

The next thing you must do is to download the two fingervein databases used in our experiments: VERA and UTFVP.  Please refer to the following websites to do this:

* VERA_
* UTFVP_

Take note of the directories in which you have stored the downloaded databases.  Then, create a textfile named ``.bob_bio_databases.txt`` and **store it in your home directory.**  Inside this textfile, insert the following two lines:

.. code-block:: sh

   [YOUR_VERAFINGER_DIRECTORY] = path_to_vera_database
   [YOUR_UTFVP_DIRECTORY] = path_to_utfvp_database

Make sure you replace ``path_to_vera_database`` with the path to your downloaded VERA database and ``path_to_utfvp_database`` with the path to your downloaded UTFVP database.


Running the Experiments
-----------------------

You are now ready to run the experiments to reproduce the results in Table 2 and Figure 2 from our paper!  The experiments are run in two parts:

1. Extract the fingervein features and compute the Hamming distance (HD) between every pair of feature vectors from different fingers, by executing the following commands (one at a time) in your terminal:

   .. code-block:: sh

      $ verify.py vera-wld   # WLD feature extractor on the VERA fingervein database 
      $ verify.py vera-rlt   # RLT feature extractor on the VERA fingervein database  
      $ verify.py vera-mc    # MC feature extractor on the VERA fingervein database  
      $ verify.py utfvp-wld  # WLD feature extractor on the UTFVP fingervein database 
      $ verify.py utfvp-rlt  # RLT feature extractor on the UTFVP fingervein database  
      $ verify.py utfvp-mc   # MC feature extractor on the UTFVP fingervein database 

   Please be aware that it might take a while for each of the above experiments to complete.  This is particularly true for the RLT extractor and for the UTFVP database in general.

   By default, all experimental results will be stored in the ``bob.paper.isba2018_entropy/results/`` directory, under the database-specific and extractor-specific sub-directories.  For example, the results for the MC extractor on the VERA database will be stored in the ``bob.paper.isba2018_entropy/results/vera/mc/`` directory.  

   Inside each extractor's results directory, you will find the following sub-directories: ``preprocessed``, ``extracted``, ``models``, ``Full`` for VERA and ``full`` for UTFVP, and ``gridtk_logs``.  These directories store the results of the full fingervein recognition pipeline, starting from preprocessing the images in the database to calculating the HDs between different fingervein feature vectors.  In particular:

   * ``preprocessed``: contains the preprocessed finger images;
   * ``extracted``: contains the extracted fingervein features;
   * ``models``: contains the enrolled fingervein features;
   * ``Full/nonorm/scores-dev`` (VERA) or ``full/nonorm/scores-dev`` (UTFVP): textfile that contains the HD between every possible pair of extracted fingervein feature vectors (``Full`` or ``full`` is the name of the matching protocol used, which in this case just means that the HD is calculated between all possible pairs of finger samples);
   * ``gridtk_logs``: contains messages logging the full experimental procedure.

   While the above directories are useful for you to inspect the output of each stage of the experimental process, the only results you need to worry about for now will be produced in part 2 of the experimental procedure. 

2. Calculate the entropy of the fingervein features from each extractor on each database, based on the previously-computed HDs (those calculated between the fingervein patterns from **different** fingers **only**), by executing the following commands (one at a time) in your terminal:

   .. code-block:: sh

      $ calculate_entropy.py -d 'vera' -e 'wld'   # WLD feature extractor on the VERA fingervein database 
      $ calculate_entropy.py -d 'vera' -e 'rlt'   # RLT feature extractor on the VERA fingervein database 
      $ calculate_entropy.py -d 'vera' -e 'mc'    # MC feature extractor on the VERA fingervein database
      $ calculate_entropy.py -d 'utfvp' -e 'wld'  # WLD feature extractor on the UTFVP fingervein database
      $ calculate_entropy.py -d 'utfvp' -e 'rlt'  # RLT feature extractor on the UTFVP fingervein database 
      $ calculate_entropy.py -d 'utfvp' -e 'mc'   # MC feature extractor on the UTFVP fingervein database


   There are two outputs for each command in this step of the experiment.  The first output is the set of statistics, including the mean, standard deviation, degrees of freedom, and entropy for the corresponding HD distribution, as per the results in Table 2 of the paper.  These statistics are printed in the ``statistics.txt`` textfile of the results directory corresponding to each feature extractor and database.  For example, for the MC extractor on the VERA database, these results are stored in ``bob.paper.isba2018_entropy/results/vera/mc/statistics.txt``.  

   The second output is the HD distribution plot with the corresponding binomial distribution overlaid, as per the results in Figure 2 of the paper.  This plot is stored in the ``HD_distribution.pdf`` file, which is located in the same place as the corresponding ``statistics.txt`` textfile.  

   Note that, if you wish to work with just one extractor and one database at a time, you do not have to run all the commands from steps 1 and 2.  For example, if you are only interested in the results for the RLT extractor on the UTFVP database, you would execute the following commands in your terminal (in the specified order):

   .. code-block:: sh

      $ verify.py utfvp-rlt                       # Extract the RLT features and calculate the HDs on the UTFVP fingervein database 
      $ calculate_entropy.py -d 'utfvp' -e 'rlt'  # Calculate the entropy of the RLT features on the UTFVP fingervein database 


Contact
-------

If you have any questions or issues relating to this software package, please contact our development `mailing list`_.


.. Links:
.. _Bob: https://www.idiap.ch/software/bob
.. _conda: https://conda.io
.. _Install Miniconda: https://conda.io/docs/user-guide/install/index.html
.. _paper: https://publidiap.idiap.ch/index.php/publications/show/3721
.. _VERA: https://www.idiap.ch/dataset/vera-fingervein
.. _UTFVP: http://scs.ewi.utwente.nl/downloads/show,Finger%20Vein/
.. _mailing list: https://www.idiap.ch/software/bob/discuss