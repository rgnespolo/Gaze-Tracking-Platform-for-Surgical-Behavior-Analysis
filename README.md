# Gaze-Tracking Platform for Surgical Behavior Analysis
An Open-Source Hardware-Agnostic Gaze-Tracking Platform for Surgical Behavior Analysis of Ophthalmologists

## Why this exist?
Research-grade eye gaze trackers are expensive and not widely available. Also, the software employed for data analysis is not open-source. This code make it possible to any researcher to extract gaze data from the overlay data provided by manufacturers and to perform features extraction such as:
- Identification of saccades, fixations, and smooth pursuit;
- Dynamic generation of areas of interest (AOI) via Deep learning;
The code is also compatible with any set of x,y coordinates extracted from any eye tracking method such as https://github.com/brownhci/WebGazer

This project would not be possible without the previous work from:
- https://github.com/dbolya/yolact
- https://github.com/tmalsburg/saccades

Please cite both works when implementing this framework in your research.

## What will you find here?
- The folder *data extraction* contains the code that extracts, via computer vision, the gaze data from the overlay provided by the manufacturer. 
- *features_extraction* contains the code used in the paper *An Open-Source Hardware-Agnostic Gaze-Tracking Platform for Surgical Behavior Analysis of Ophthalmologists*. Inside this folder, *saccades_fixation* contains the modified code from [Saccade and Fixation Detection in R](https://github.com/tmalsburg/saccades).
- *sample_data* contains data retrieved from ophthalmologists while watching a short video containing six cataract and vitreoretinal surgical phases, together with the tooltip tracking data for the vitrector. The surgical phases are  ['rhexis', 'phaco', 'cortex removal', 'core_vitrectomy', 'membrane_peeling', 'laser'].
- *YOLACT_adapted* shows the files modified from the [Original YOLACT++ model](https://github.com/dbolya/yolact) to track and segment instruments and retinal features.

## Requirements
For the extraction of features, set up a Python3 environment and install the additional packages:
```python
pip install opencv-python numpy matplotlib scipy pandas
```
For the YOLACT++ model, please follow the original requirements here: https://github.com/dbolya/yolact#installation

## Running the code
To reproduce the results of the paper, the following steps need to be taken:
- Record the gaze overlay information with the OBStudio Screen recorder.
- Run *extract_gaze_coord_from_overlay.py* located in the folder *data_extraction*
- Choose the desired feature to be extracted running any of the codes from the folder *features_extraction*