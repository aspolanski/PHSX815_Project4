# PHSX815_Project4

This package simulates and compares radial velocity datasets with different per-point uncertainties.


## Description of Included Scripts:

* *data_sim.py*: Simulates the data sets and stores them as a .csv file.

* *model_fit.py*: Optimizes to find the best fit parameters to a data set. It does this with two models, one with no eccentricity and one with eccentricity. It produces the AIC score for each model.

## Usage

To simulate data:

```python
python data_sim.py -tc 2 -per 6.0 -k 30 -e 0.5 -sigma 35 -fname test_data
```

To run analysis:
```python
python model_fit.py -fname test_data
```
 

## Dependencies

This code requires:
* Python 3.7.3
* Scipy v1.6.0
* Numpy v1.19.2
* MatplotLib v3.3.2
* RadVel v1.4.3
