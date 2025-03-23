# A Comprehensive Analysis of Pollution and Weather Data (2000-2016)

This project explores pollution levels across The United Stes from 2000-2016, analysing their relationship with weather patterns. It leverages multiple datasets to uncover insights into air quality, climate trends and their broader environmental impact. 

# ![Pollution Image](https://cms.accuweather.com/wp-content/uploads/2020/02/cropped-city-under-a-cloudy-sky-2771744.jpg)


## Dataset Content

* **Pollution Data:** [Kaggle-Pollution Dataset](https://www.kaggle.com/datasets/sogun3/uspollution) 
* **Weather Data:** [Nation Centers for Envornmental Information](<https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_year/>)
* Files from NCEI: 
   -  `ghcnd-countries.txt` (Countrycodes)
   -  `ghcnd-states.txt` (Statecodes)
   -  `ghcnd-stations.txt` (Station codes)


## Business Requirements
| Requirement | Visualization |
|------------|--------------|
| Identify trends in air pollution over time and locations | Time series graphs |
| Assess the correlation between pollution and weather factors | Correlation matrices |
| Provide actionable insights for policymakers and environmental agencies | Geographic heatmaps |
| Enhance accessibility of pollution data | Interactive map visualizations in Streamlit |


## Hypothesis and how to validate?
- **Hypothesis 1:** Higher temperatures correlate with increased pollution levels. 
- **Hypothesis 2:** Urban areas exhibit higher pollution levels than rural areas. 
- **Hypothesis 3:** Weather factors such as wind speed and humidity impact pollution dispersion
- **Hypothesis 4:** CO, SO₂, NO₂, and O₃ AQI levels have decreased from 2003 to 2013 due to environmental regulations
- **Hypothesis 5:** SO₂ and NO₂ AQI levels are higher in states with more coal power plants (e.g., Texas, Pennsylvania, Illinois)
- **Hypothesis 6:** CO and NO₂ AQI levels spike during winter months due to increased heating and stagnant air
- **Hypothesis 7:** O₃ AQI levels are higher in summer months due to increased sunlight and heat

## Validation 
- **Validation 1:** Analyze the correlation between temperature and key pollutants (O₃, PM2.5, NO₂, CO) using statistical and machine learning models (e.g., linear regression, decision trees) to predict pollution levels.
- **Validation 2:** Segment data by location type (urban vs. rural) and analyze pollution patterns using descriptive statistics, visualizations (e.g., box plots, heatmaps), and clustering techniques (e.g., K-means).
- **Validation 3:** Analyze the relationship between wind speed, humidity, and pollution levels using correlation analysis, time-series methods for seasonal trends, and regression models to quantify their impact.
- **Validation 4:** Conduct a trend analysis using line plots and regression. Perform a t-test comparing pre- and post-regulation AQI levels.
- **Validation 5:** Correlate AQI levels with the number of coal power plants per state using scatter plots and correlation analysis.
- **Validation 6:** Perform a seasonal analysis of AQI data using monthly averages and t-tests comparing winter and non-winter months.
- **Validation 7:** Conduct a seasonal analysis and correlate O₃ levels with temperature data using regression analysis.

---
## Modeling Plan for Air Quality Prediction:
 We will create 4 models for predicting air quaility levels: 
 1. Ozone (O₃) 
 2. Particulate Matter (PM2.5) 
 3. Nitrogen Dioxide (NO₂)
 4. Carbon Monoxide (CO) 

 Each model will be built using machine learning techniques such as: 
 - **Linear Regression:** Baseline predictive analysis
 - **Decision Trees & Random Forest: **Capturing non-linear relationships 
 - **Neural Networks (if applicable):** For adanced forecasting
 - **Evaluation Metrics:** RMSE, MAE, R² score

## Project Plan and Roadmap  

### **Phase 1: Data Preparation**
- Add initial data structure details to README  
- Document ETL process and initial EDA  
- Merge pollution and weather datasets  
- Handle missing values (mean/median imputation)  
- Filter data for selected 10-year period and locations  

### **Phase 2: Exploratory Data Analysis (EDA)**
- Conduct descriptive statistics  
- Perform correlation analysis (pollution vs. weather)  
- Visualize pollution trends & distribution  
- Create map to display pollution data in Streamlit  
- Add weather data to Streamlit visualizations  

### **Phase 3: Statistical Analysis & Hypothesis Testing**
- Define and document key hypotheses  
- Apply machine learning transformations to key measures  
- Conduct regression & predictive modeling  

### **Phase 4: Dashboard & Application Development**
- Develop Streamlit dashboard for data exploration  
- Implement a data manipulation page  
- Integrate visualizations for interactive insights  

### **Phase 5: Deployment & Finalization**
- Deploy Streamlit app on Heroku  
- Final review, documentation, and improvements  

## **Approach & Methodology**

### **Data Handling & Management**
- **Collection**: Data gathered from pollution and weather sources  
- **Processing**: Cleaning, missing value treatment, and merging datasets  
- **Analysis**: Correlation checks, ML modeling, and visualization  
- **Interpretation**: Generating insights for real-world applications  

### **Why This Approach?**
- Ensures **accurate** and **reliable** insights  
- Balances **EDA, statistics, and machine learning** for depth  
- Supports **scalable** and **interactive** analysis via Streamlit  


## The Rationale to Map the Business Requirements to the Data Visualisations

| Requirement | Visualization |  
|------------|--------------|  
| Identify trends in air pollution over time and locations | Time series graphs |  
| Assess the correlation between pollution and weather factors | Correlation matrices |  
| Provide actionable insights for policymakers and environmental agencies | Geographic heatmaps |  
| Enhance accessibility of pollution data | Interactive map visualizations in Streamlit |  


## Analysis techniques used
- Descriptive Analysis 
- Correlation Statistics 
- Time series forecasting 
- Machine Learning models for prediction 
- Data imputation using mean and median


## Ethical considerations
* **Bias Awareness:** Ensuring data is analysed eihtout preconceived notions. 
* **Data privacy:** Compliance with ethical data collection and usage policies. 
* **Fair representation:** Ensuring all regions and populations are fairly represented. 

## Dashboard Design
- Interactive visualisations for pollution trends.
- Filters for specific regions and time periods. 
- Predictive insights on pollution levels.

## Deployment
### Heroku
- **Platform:** Streamlit
- **Hosting:** Heroku 

* The App live link is: ________ 
* **Steps:** ADD STEPS 

## Future Improvements 
- Integration of real-time pollution monitoring data
- Enhanced machine learning models for better prediction accuracy

## Main Data Analysis Libraries
| Library | Usage |
|---------|------|
| Pandas | Data processing |
| NumPy | Mathematical computations |
| Matplotlib & Seaborn | Visualizations |
| Scikit-learn | Machine learning models |
| Plotly | Interactive charts |


## Credits and Acknowledgments 
 - **Dataset:** [Kaggle - US Pollution Dataset](https://www.kaggle.com/datasets/sogun3/uspollution)
- **Weather Data:** [NCEI - Global Historical Climatology Network](https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_year/)
- **Contributors:** Paul G, Tamika, Hasnain S, Thinley


## Conclusion 
This project provides valuable insights into pollution trends and their relationships with weather conditions. The findings can assist in environmental policymaking and awareness campaigns. Our findings confirm that air quality has improved over time, with CO, SO₂, NO₂, and O₃ levels declining significantly between 2003 and 2013, likely due to stricter environmental regulations. Urban areas and states with higher industrial activity, especially those with more coal power plants, consistently show higher pollution levels.

Seasonal patterns reveal that CO and NO₂ levels spike in winter due to heating and stagnant air, while O₃ levels increase in summer, driven by higher temperatures and sunlight. Weather conditions play a crucial role in pollution dispersion, with wind speed helping to reduce pollutant concentrations and humidity sometimes trapping them closer to the surface. Additionally, machine learning models successfully predict AQI levels based on weather data, offering potential for real-time forecasting.

These insights highlight the need for continued policy efforts, public awareness, and technological advancements in air quality monitoring. Future work could integrate real-time pollution data, expand pollutant analysis, and enhance predictive models for more accurate forecasting and decision-making.
