*This is human-made notes intended to dissect and understand parts of the thesis.*


## Shared Files:
- [ACU Records](https://docs.google.com/spreadsheets/d/1_9Jq7HEWO1OAJWzGnufByKantJ-8XXO7khHhAd49V1A/edit?gid=0#gid=0)

## Things to do for now:
- ~*Complete site inspection data.*~
- Complete experimental process for all hypothesis involving fault injection 
- Prepare letters for tomorrow.

## Sampling Data
1 Unit -> V Visits -> 10 Trials per visit (1 minute recording: 10 mins total) -> 6 Windows per trial (1 Window = 10 seconds) -> 100 Samples per Window (10 Samples/Date point per second) 

Formula: N Units x V Visits x 10 Trials x 6 Windows x 100 Samples

The number of units that will be tested ideally will be 35 units and will be visited 3 times. 
Therefore, there will be 6300 windows. 

If the number of units that will be tested will be 20 units and will also be visited 3 times. The number of windows will be 3600 windows.

If 1-2 units are used for the fault injection. The number of windows will be 180-360 windows.

## Database Structure
### raw_data.csv
*This file collects the raw data from the sensors. This is used for windowing and feature extraction. This is the first stage of the data processing. One row corr*

The metadata consists of the following:
- unit_id
- unit_type
- visit_id
- trial_id
- window_index
- phase (normal)
- fault_type (blank)
- pair_id (blank)
- timestamp
- location
- setpoint


The raw channels will consist of the following: 
- ambient_temp
- ambient_rh
- inlet_temp
- outlet_temp
- coil_temp
- current
- airflow

Vibration will be recorded separately in a raw file. 




### **healthy_windows.csv**
*This file will be used to train the anomaly. One row corresponds to a window. This is the second stage of the data processing.*

The metadata columns will consist of the following:
- unit_id
- unit_type
- visit_id
- trial_id
- window_index
- phase (normal)
- fault_type (blank)
- pair_id (blank)
- timestamp
- location
- setpoint

The data will collect the following:
- ambient temp mean
- ambient temp std
- ambient rh mean
- ambient rh std
- inlet temp mean
- inlet temp std
- outlet temp mean
- outlet temp std
- coil temp mean
- coil temp std
- delta T mean 
- delta T std
- current mean
- current std
- airflow mean
- airflow std


### injected_windows.csv
*This file will be used to score pre-injection, post-injection, and recovery data (optional). One row corresponds to a window. This is the second stage of the data processing.*

It has the same feature columns as healthy_windows, plus:
- *phase* = pre, post, or recovery
- *fault_type* = blocked_return_air, reduced_refrigerant, or misaligned_fan
- *pair_id* = links the pre and post trials 

However getting the data is different. Visits will be 3 based on the fault_type. One pair corresponds to three phases. Two trials corresponds to one pair while still having 6 windows, so there will be 16 trials and 8 pairs. Therefore the new formula will be:

Formula: N Units x 3 Visits/Faults x 8 Trials/Pairs x 3 Phases x 6 Windows x 100 Samples

*For example: An injected unit is recorded for 1 minute for before injecting (pre-phase) 8 times. So a total of 8 minutes per injected unit. Another 8 minutes after injecting and after recovery.*

The metadata columns will consist of the following:
- unit_id
- unit_type
- visit_id
- trial_id
- window_index
- phase 
- fault_type 
- pair_id 
- timestamp
- location
- setpoint

The data will collect the following:
- ambient temp mean
- ambient temp std
- ambient rh mean
- ambient rh std
- inlet temp mean
- inlet temp std
- outlet temp mean
- coil temp std
- delta T mean 
- delta T std
- current mean
- current std
- airflow mean
- airflow std

### Trial Score


The metadata columns will include the following:
- unit_id, unit_type, visit_id, trial_id
- phase, fault_type, pair_id
- timestamp, location

The data will collect the following:
- score ambient
- score thermal
- score current
- score vibration
- score airflow

### Additional Notes
#### Parametric Tests 
[Wilcoxon Signed Rank Test](https://www.youtube.com/watch?v=NZsL2eDQiDQ)
Wilcoxon-Tests whether there is difference between two dependent samples. This is a non-parametric counterpart to the t-test for dependent samples. 

> The data do not have to be normally distributed. 

#### Fourier Transform 
[How the Fourier Transform Converts Sound into Frequencies](https://towardsdatascience.com/everything-you-need-to-know-about-fourier-transform/)






