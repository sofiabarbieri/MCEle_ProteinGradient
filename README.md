# MCEle_ProteinGradient


### General Info
***

MCele_ProteinGradient is a MonteCarlo tool developed to reproduce the dynamics of protein gradient formation in the C. elegans embryo.
In particular, it focuses on PLK-1 and MEX-5 proteins.

## Requirements
***

* cmake: version > 3.1
* make
* gcc
* Python
* Matplotlib
* numpy
* scipy
* CERN ROOT
* Boost C++ libraries - including boost.python module

## System/Package versions tested
***

* OS: Ubuntu18 - Fedora33
* cmake: 3.17.4
* make: 4.2.1 
* gcc: 10.3.1 20210422
* Python: 2.7.18
* Matplotlib: 2.2.5
* numpy: 1.16.6
* scipy: 1.2.3
* CERN ROOT: 6.22/07 
* Boost C++ libraries - including boost.python module: 1.69
***
The software may run with other versions. Python3 is NOT supported.


## Installation
***
To install, please follow the instructions below:
```
$ git clone https://github.com/sofiabarbieri/MCEle_ProteinGradient.git

$ mkdir install
$ mkdir build
$ cd build
$ cmake ../
$ make
$ make install
$ cd ../install
```
Installation takes 1-2 minutes.

## Run instruction
***
To run the code
```
$ python main.py 
```
Several parameters are expected:
```
-p (--particles) <number> : number of particles to create
-b (--bound) : enable rebound at embryo's boundaries
--plk1 : enable plk1
--threeD : enable 3D 
--drawMovie : make GIF of protein dynamics
--settings <filename> : settings filename
-f (--slice) : enable slice
```
Example:
```
python main.py -p 1000000 --bound --plk1 --threeD --slice --settings settingsTemplate 
```
In prodution several runs can be launched in parallel (predefined 10 runs), by executing the runner.sh bash script.
As a title of example a run as the example before (10^6 paricles for both MEX-5 and plk1) has a memory footprint of about 800 MB.

## Output
***
The simulation output is saved in the ./logs/X directory where X is the date and time at the beginning of the run.
Several variables and information are reported, refer to the Supplementary material to know more.
In case several runs with same settings are launched (as for example, by using the runner.sh script), results can be summaryzed by using the analyze.py script, which produces mean and std dev over the runs.
```
python  analyze.py -f log_k_mex5.txt -o mex5.txt
```
where -f is the filename to parse and average over the runs, and -o is the output file to generate.
***
Average running time on normal desktop machine is of the order of few hours per run.

## Sample data
***
A sample output data is available in the logs directory, as well as a setting file ready to be used.
## Output data description
***
Conc_idY_XXX: 2D distribution of the protein XXX (Y component) as a function of time  (rows) and space along the embryo axis (columns) within the volume slice
log_k_XXX: extrapolated gradient value from the linear fit for the protein XXX
log_mex5_ratio_slow_fast: ratio between slow and fast component for MEX-5 protein along the embryo axis as a function of time within the volume slice
log_profileAP_XXX: normalized particle concentration for protein XXX along the line ROI within the volume slice
log_v_XXX: average velocity for particle XXX along the embryo axis as a function of time within the volume slice
summary_parameter: summary of the input parameters used for the simulation run.
***
## Data analysis script provided
***
For averaging results over multiple runs launched with same input parameters, run, in the shell, in the logs package directory (or in output directory), the Python macro: analyzer.py:
```
python analyzer.py -f log_k_mex5.txt -o mex5.txt
```
this provides the output file (e.g.) mex-5.txt with a column for the average values and a column for standard deviations (STDEV) for each timeframe, of the parameters in the input files (e.g.) log_k_mex5.txt
To analyze results that have a distribution in time ans space (2D matrices), run the Python macro analyzerConc.py, in the output folder
```
 python  analyzerConc.py -f log_v_plk1.txt -o v_plk1
```
this provides the output files (e.g.) v_plk1_MEAN.txt and (e.g.) v_plk1_STDDEV.txt (extensions ias added by the macro), respectively containing the matrix of the mean values and the STDEV over the runs of the values from the input files (e.g.) log_v_plk1.txt.
3D plots of the output files can be otained by running:
```
python plotter_3D_t_X.py -i v_plk1_MEAN.txt
```
this provides the distribution as a function of time and space of the parameter in the input file, along with the 2D distributions.


