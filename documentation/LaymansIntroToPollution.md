# Layman's Explanation of Air Pollution Data Columns

Here’s a layman’s explanation of the column titles and their expected ranges for air pollution data:

---

## 1. NO₂ (Nitrogen Dioxide)

- **NO₂ Units**: The unit of measurement (usually parts per billion (ppb) or micrograms per cubic meter (µg/m³)).
- **NO₂ Mean**: The average NO₂ concentration over a given time period.  
    **Expected Range**: Typically 0 - 100 ppb (higher in urban areas due to traffic and industry).
- **NO₂ 1st Max Value**: The highest recorded NO₂ value within a specific time window (e.g., hourly or daily).  
    **Expected Range**: Usually 0 - 200 ppb.
- **NO₂ 1st Max Hour**: The hour when the highest NO₂ level was recorded.  
    **Expected Range**: 0 - 23 (24-hour format).
- **NO₂ AQI (Air Quality Index)**: A score representing how safe or hazardous the NO₂ level is.  
    **Expected Range**: 0 - 500 (higher values mean worse air quality).  
    **Example**:  
    - 0 - 50 (Good): Clean air.  
    - 51 - 100 (Moderate): Acceptable, but may affect sensitive groups.  
    - 101+ (Unhealthy/Hazardous): Potential health issues.

---

## 2. O₃ (Ozone)

- **O₃ Units**: The unit of measurement (parts per million (ppm) or µg/m³).
- **O₃ Mean**: The average ozone concentration over a time period.  
    **Expected Range**: 0 - 0.1 ppm (ground-level ozone).
- **O₃ 1st Max Value**: The highest recorded ozone level in the given period.  
    **Expected Range**: 0 - 0.2 ppm.
- **O₃ 1st Max Hour**: The hour when the highest ozone level was recorded.  
    **Expected Range**: 0 - 23 (24-hour format).
- **O₃ AQI**: Air Quality Index for ozone.  
    **Expected Range**: 0 - 500 (higher means worse air quality).

---

## 3. SO₂ (Sulfur Dioxide)

- **SO₂ Units**: The unit of measurement (ppb or µg/m³).
- **SO₂ Mean**: The average SO₂ concentration over time.  
    **Expected Range**: 0 - 50 ppb (higher near industrial areas).
- **SO₂ 1st Max Value**: The highest recorded SO₂ level in the given period.  
    **Expected Range**: 0 - 300 ppb.
- **SO₂ 1st Max Hour**: The hour when the highest SO₂ level was recorded.  
    **Expected Range**: 0 - 23 (24-hour format).
- **SO₂ AQI**: Air Quality Index for SO₂.  
    **Expected Range**: 0 - 500.  
    **Note**: The value `-0.000011` is likely a data error or small rounding issue.

---

## 4. CO (Carbon Monoxide)

- **CO Units**: The unit of measurement (ppm or µg/m³).
- **CO Mean**: The average CO concentration over time.  
    **Expected Range**: 0 - 10 ppm (higher in areas with vehicle emissions).
- **CO 1st Max Value**: The highest recorded CO level in the given period.  
    **Expected Range**: 0 - 50 ppm.
- **CO 1st Max Hour**: The hour when the highest CO level was recorded.  
    **Expected Range**: 0 - 23 (24-hour format).
- **CO AQI**: Air Quality Index for CO.  
    **Expected Range**: 0 - 500.  
    **Example**:  
    - 0 - 50 (Good): No health effects.  
    - 51 - 100 (Moderate): Might cause discomfort for sensitive groups.  
    - 101+ (Unhealthy to Hazardous): Breathing difficulties possible.

---

## Summary

- **Units**: Define how the pollutant is measured (ppb, ppm, µg/m³).
- **Mean**: Average pollutant level over a time period.
- **1st Max Value**: The highest observed concentration.
- **1st Max Hour**: When the peak concentration occurred.
- **AQI**: A standardized score indicating air pollution severity.
