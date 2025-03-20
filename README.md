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

## Validation 
- **Validation:** Statistical analysis, correlation checks and machine learning techniques will confirm relatioships. 
- Conduct regression & predictive modelling

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
- **Contributors:** *[To be updated]*


## Conclusion 
This project provides valuable insights into pollution trends and their relationships with weather conditions. The findings can assist in environmental policymaking and awareness campaigns. 
(MORE TO BE ADDED AS ANALYSIS PROGRESSES)