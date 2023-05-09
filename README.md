## Udacity Data Analysis Nanodegree

---
## Project 5: Communicate data findings 
#### Created by: Juanita Smith
#### Last date: 9 May 2023

---

## Airline on-time performance

Have you ever been stuck in an airport because your flight was delayed or cancelled and wondered if you could have predicted it if you'd had more data? This is your chance to find out.

<img src="images/flights.png" alt="drawing" width="950"/>


## Dataset

> This dataset reports flights in the United States, including carriers, arrival and departure delays, with reasons for delays, from 1987 to 2008. Due to large data volume, only years 2003 - 2008 will analysed in this project.
> - See more information about the data from the data expo challenge in 2009 [here](https://community.amstat.org/jointscsg-section/dataexpo/dataexpo2009).
> - See a full description of the features [here](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EFD&Yv0x=D.)
> - Data can be downloaded from [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/HG7NV7).

Note: This is a large database over 12 GiB in size, and therefore will be excluded from GitHub.

### Dictionary:
1) Year: 1987-2008 
2) Month: 1-12 
3) DayofMonth: 1-31 
4) DayOfWeek: 1 (Monday) - 7 (Sunday) 
5) DepTime: actual departure time from gate (local, hhmm) 
6) CRSDepTime: scheduled departure time from gate (local, hhmm) 
7) ArrTime: actual arrival time at gate (local, hhmm) 
8) CRSArrTime: scheduled arrival time at date (local, hhmm) 
9) UniqueCarrier: unique carrier code 
10) FlightNum: flight number 
11) TailNum: plane tail number 
12) ActualElapsedTime: The time computed from gate departure time to gate arrival time in minutes
13) CRSElapsedTime: The time computed from gate departure time to gate arrival time in minutes
14) AirTime: in minutes 
15) ArrDelay: arrival delay, in minutes 
16) DepDelay: departure delay, in minutes 
17) Origin: origin IATA airport code 
18) Destination: IATA airport code 
19) Distance: in miles 
20) TaxiIn: The time elapsed between wheels down and arrival at the destination airport gate in minutes
21) TaxiOut: The time elapsed between departure from the origin airport gate and wheels off in minutes
22) Cancelled: 1 = yes, 0 = no 
23) CancellationCode: reason for cancellation (A = carrier, B = weather, C = NAS, D = security) 
24) Diverted: 1 = yes, 0 = no 
25) CarrierDelay: subcategory of arrDelay in minutes
26) WeatherDelay: subcategory of arrDelay in minutes 
27) NASDelay: subcategory of arrDelay in minutes 
28) SecurityDelay: subcategory of arrDelay in minutes 
29) LateAircraftDelay: subcategory of arrDelay in minutes


## Summary of Findings

**Approach:**
    
1) From **univariate** exploration, we know seasonality is the biggest reason for delays. We also know which airports and carriers experience the most delays.
2) In **bivariate** exploration, I zoomed into the relationships between the top 30 airports and carriers experiencing the most delays, to identify if there are certain airports and carriers that should be specifially avoided. A *problem quadrant* was discovered, where a group of around 10-12 carrier/airport combinations, have above average delays.
3) In **multivariate** exploration, we try to find the reasons for these above average delays in the *problem quadrant* of heatmap in step 2.
   - To find possible distinguishing factors, 4 carriers that have consistent average delays across all airports are compared with 8 carrier/airport combinations that have above average delays. These two groups are compared from various perspectives.
   - A divergent palette **vidiris_r** was used consistently, where yellow/light green is used to show average delays, and dark green/blue to show above average delays.

**Main findings:**
    
Around 77% of flights are on time, whereas 21% of flights are delayed. Only 2% of flights are cancelled or diverted which is not therefore not the main concern and were further excluded.
The top 3 reasons for delays are caused by late aircrafts (36%), NAS(32%), and carriers(26%).
Flights and delays increase every year, we see an upwards trend. We can therefore expect more delays in future during peak periods if this trend continues.

There is a strong seasonal pattern. There are 2 strong peaks, the biggest one around xmas time in December - March, and another one during summer months June - August.
Mondays, Thursdays and Fridays are the busiest times at airports, it is the most quiet on Tuesdays and Saturdays.
Delays grows progressively throughout the day, with most delays happening between 17:00-20:00   
    
The top busiest origin/departure airports (ATL, ORD, DFW and EWR) are also the top destination/arrival airports causing delays, meaning a delay in the origin is causing a delay in the destination. From a proportional perspective, JFK, PHL, EWR, ORD have over 40% of their flights delayed on departure, whilst EWR, LGA, ANC, JFK, ROC have the biggest delays at destination/arrival airports.
    
When a lane consist of a combination where both origin and destination airports are ORD, EWR, ATL, DFW, we can defintely expect delays.

There is not as much variation in the average total flights per month even in the peak periods, which suggest it's not the number of flights itself that are causing the problem. The delays happens in the peak seasons mostly during the week, which suggest the biggest driver for delays might be due to passenger throughput.
    
Main reasons for delays are late aircraft and carrier delays in origin airports. NAS delays happens mostly in destination airports, and are a consequence of delays that happened in origin airports. Destination airports have a tough time to reschedule late arriving flights especially in busy periods.
    
Of the top 30 carriers and airports causing the highest average delays, there is a specific combination of carriers/airports falling into the bottom right quadrant on the main heatmap, that cause higher that average delays. Carriers in the problem quadrant fly multiple repeat flights, but over shorter distances around 500 miles, whereas carriers on the left of the quandrant, do distances around 1000 miles. Carriers with shorter distances, have less time to catch-up any delays during flight time.
      
Avoid airports EWR, ORD, as all top carriers have above average delays at these airports
Avoid carriers YV, EV, FL, as they perform consistently bad at all top airports           

## Key Insights for Presentation

Tell the story that describe the most significant factors that predict delays:

1. Setting the scene by showing distribution of flights - 21% of flights are delayed
2. Seasonal peaks are the main reason for delays
3. All airports and carriers will have delays during seasonal peaks, however certain airports and carriers have delays above average. Highlight these airports/carriers.
5. Repetitive short-haul vs long-haul lanes are the most distinguishing factor setting airports/carriers apart. Carriers flying longer distances have more time to catch-up delays

The same plots from exploratory analysis was used, however titles and axis were further improved.
The heatmap was reduced to show only the top 20 carriers and airports instead, to make the plot fit onto the slide correctly.