### Sources of information
 - Climate information 
    - https://climate-change.canada.ca/climate-data/#/hourly-climate-data
    - api.weather.gc.ca
    - https://charts.gc.ca/publications/tables-eng.html  
    - https://tides.gc.ca/en/current-predictions-station
- BC ferries 
    - bcferriesapi.ca
    - https://www.bcferries.com/routes-fares/schedules?gad_source=1&gclid=Cj0KCQiAhbi8BhDIARIsAJLOluf5FxC-s0fcjQ-jgu4AkHtKK0GZXZEcfRLQ49CM4UbSa3LCmJr8j8oaAvOcEALw_wcB
- Articles or other
   - https://www.bcferries.com/news-releases/highest-vehicle-traffic-ever-recorded-in-63-year-history
   - https://www.bcferryauthority.com/meetings-and-reports/



### Details for running the bc ferries api server locally
 - ##### Due to some values being hardcoded: 
    - DB_HOST must be db
    - the port for the api must be 8080
 - ##### Should probably change it so that the cron job in the locally running server to once every 5 or 10 minutes isntead of every minute.
