.. vim: set fileencoding=utf-8 :
.. Sushil Bhattacharjee <sushil.bhattacharjee@idiap.ch>
.. Thu 15 Sep 13:43:22 2016

======================================================================================
Package for paper, presented at BioSIG-2017, on extended-range imaging for 3d-Mask PAD 
======================================================================================


If you use this package, please cite the following paper::

    @inproceedings{bhattacharjeeBiosig2017,
        author = {Sushil Bhattacharjee and S{\'{e}}bastien Marcel},
        title = {What you can't see can help you -- extended range imaging for 3d-mask presentation attack detection},
        year = {2017},
        month = sep,
        booktitle = {Proceedings of the 16th International Conference of the Biometrics Special Interest Group (BIOSIG)},
        address = {Darmstadt, Germany},
    }

This python package contains scripts to be used to reproduce results presented in the paper.
This document explains the commands to be executed in this package, to reproduce the results shown in the paper.

Reproducing results of the paper
--------------------------------
This package provides a script for producing the mean-histogram shown in the paper.
First, please install the package.
In the rest of this document, the term **$PKGHOME** will refer to the folder where the package has been installed.

To run the script, you will also need to make sure the corresponding dataset `ERPA <https://www.idiap.ch/dataset/ERPA>`_  is available on your computer.

The commands discussed below assume that your current working-directory is **$PKGHOME**.


Mean Thermal Response Plot:
===========================

Figure 5 in the paper shows distributions of the mean pixel-values of the face-region in the thermal images captured using the Xenics Gobi camera. 
To reproduce this plot, use the following command:

.. code-block:: sh

    $ ./bin/thermal_mean_hist.py -ip <input-ERPA-folder> -op <output-plot-folder>

where <input-ERPA-folder> should be the folder containing the ERPA dataset, and <output-plot-folder> should specify the folder where you want the plot to be created as a pdf file.
This command will process images from the 'Xenics_Gobi' sub-folder in the specified input-folder (<input-ERPA-folder>), and create a file called 'thermal_profile_hist.pdf' in the specified output folder.


.. _bob: https://www.idiap.ch/software/bob
.. _ERPA: https://www.idiap.ch/dataset/ERPA

