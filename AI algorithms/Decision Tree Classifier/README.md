# Decision Tree Classifier

In the project below, I investigate the effectiveness of the decision tree algorithm and its modifications on an obesity dataset. The model is implemented in Python using the scikit-learn library.

Created: 11/2022

## Dataset
Dataset presents estimation of obesity levels in individuals from the countries of Mexico, Peru and Colombia, based on their eating habits and physical condition. The data contains 2111 records, 77% of which are generated synthetically using the Weka tool and the SMOTE filter, 23% of the data was collected directly from users through a web platform.

Source along with an article describing this dataset can be found [here](https://www.sciencedirect.com/science/article/pii/S2352340919306985?via%3Dihub#fd1)

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


## Data Preprocessing

### Fixing synthetic labels

Many records are created synthetically and so their classes. This means that some of these classes could be incorrect taking into account strict formula used for labelling. Therefore it is needed to recalculate them based on both weight and height of given record. To perform this simple formula in Excel was created.

### Missing and unbalanced data

These issues has been already resolved by the authors. There are no missing values, and data is distribiuted rather equally (Fig. 1.) thanks to synthetic data.

<p align="center">
  <img src="https://user-images.githubusercontent.com/80170154/199302535-6b86e875-d737-49f1-b3ac-273c6db5d38c.png" />
</p>
<p align="center">
  Fig. 1. Balanced Distribution of data regarding the obesity levels category.
</p>

### Dealing with categorical data

Since categorical features are present and used decision tree implementation does not handle that type of data they need to be encoded. To solve this issue scikit-learn ```OneHotEncoder``` and ```OrdinalEncoder``` classes were used. Unfortunately without AI or advanced dictionaries it is hard to automate separating ordinal from nominal data. Therefore it is required to manually provide names of all ordinal features and their possible categories in correct order. Then remaining categorical data will be treated as nominal i.e. encoded with one-hot encoding.

### Features correlation with target

TO DO

## Basic clasification tree performance

TO DO

## Model modifications performance

TO DO

## Conclusions

TO DO
