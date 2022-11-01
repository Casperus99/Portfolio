# Classification With Decision Tree

## Dataset
Dataset presents estimation of obesity levels in individuals from the countries of Mexico, Peru and Colombia, based on their eating habits and physical condition. The data contains 2111 records, 77% of which are generated synthetically using the Weka tool and the SMOTE filter, 23% of the data was collected directly from users through a web platform.

Source along with an article regarding this dataset can be found [here](https://www.sciencedirect.com/science/article/pii/S2352340919306985?via%3Dihub#fd1)

### Features
The data contains 16 features. A few of them are: height, weight, gender, and family history with overweight.  
Their division by type is as follows:

- Numerical: 8
- Categorical: 8
  - Nominal: 6
  - Ordinal: 2
  
### Target attribute
To label the data the BMI for each individual had to be calculated with equation (1). The results were then compared with the data provided by WHO and the Mexican Normativity.

<p align="center">
  <img src="https://user-images.githubusercontent.com/80170154/199259442-10dc9e75-eed0-4b7d-9446-c2a0d2789f76.png" />
</p>

The records are labeled with the class variable NObesity (Obesity Level), that allows classification of the data using the values of Insufficient Weight, Normal Weight, Overweight Level I, Overweight Level II, Obesity Type I, Obesity Type II and Obesity Type III depending on the calculated BMI value. 
