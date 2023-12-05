# Indego Bike Share Data Exploration


## Sources:
* [Indego Public Data](https://www.rideindego.com/about/data/)



## Introduction:
Data exploration and visualization of Philadelphia's bike sharing network. The goal is to create a large dataset with historic trip data going back through 2017. In the future I may attempt to create a streaming dataset of the bike stations using the "live station status" endpoint.


## Data:
* [Trip Data](https://www.rideindego.com/about/data/)
* [Station Information](https://www.rideindego.com/about/data/)


### To Do:

#### Data Preparation
- [x] Script to download all .zip and .csv.zip files of trip data and station information
- [x] Clean Data
  - [x] Remove and impute null values
    - [x] Remove any virtual station trips (start_station == 3000 or end_station == 3000)
  - [x] Standardize column names and data types for merging
  - [ ] Data checks
    - [x] Data types and column names are all the same
    - [x] No unexpected null values
    - [ ] trip_id is unique
  - [ ] Merge all year's data into single dataset
    - [ ] Check for uniqueness
  - [ ] Remove trips with the same source and destination under a certain amount of time
- [ ] Add latitude and longitude to station table from trips dataset

#### Analysis
- [ ] Ride heatmap 
### Analysis Ideas:
- [ ] Does there appear to be a change in ridership with weather? If so, what is the change?
- [ ] How has ridership changed before/during/after pandemic restrictions?
- [ ] Are there certain trips that are extremely impressive? Maybe the distance and elevation change makes it impressive?
- [ ] What is the best way to view ridership over time? What are some considerations?
- [ ] Find outlier trips:
  - [ ] Deviation from average or other statistic for trip time between origin and destination.
- [ ] Who drives ridership and on what circumstances? Passholders vs. Day pass?
- [ ] Animation of rides over a 24 hour period. Inspired by [bikesharemap](/home/jagord24/dev/Zoomcamp/week_1_basics_n_setup/2_docker_sql/indego_bikes/readme.md), other resources:
  - [medium article using folium](https://justinmorganwilliams.medium.com/how-to-make-a-time-lapse-heat-map-with-folium-using-nyc-bike-share-data-1ccd2e32c2e3)