
# HomeBot
Home utility bot in discord using Python


## Dependencies
All dependancies are contained within `requirements.txt` file. To install run:
```
pip3 install -r requirements.txt
```


## How to Run
```
python3 HomeMain.py
```

Alternatively, a docker image can be built and run using the included `Dockerfile`. Eg.
```
docker built -t name-of-your-docker-image .

docker run --rm -d -e TOKEN="insert-your-token-here" name-of-your-docker-image
# A valid Discord token will need to be passed into the docker container
```


## Features
1. Airport weather data requests
   - Airport METAR reports
   - Airport TAF reports
2. F1 Standings
   - F1 Schedule
   - World Drivers Standings
   - World Constructors Standings
3. Ireland COVID-19 Data
   - Ireland new COVID-19 data


## Attribution
- [METAR/TAF](https://www.aviationweather.gov/) API from Aviation Weather Center / National Weather Service, [(NOAA)](https://www.noaa.gov/) National Oceanic and Atmospheric Administration
- [F1](https://documenter.getpostman.com/view/11586746/SztEa7bL) Data API from [Ergast](http://ergast.com/mrd/)
- [Ireland COVID-19](https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/Covid19StatisticsProfileHPSCIrelandView/FeatureServer/0/) Data from [Ireland COVID-19 Data Hub](https://covid-19.geohive.ie/)
- [COVID-19](https://www.flaticon.com/free-icon/covid-19_2785819?term=covid&page=1&position=31&page=1&position=31&related_id=2785819&origin=search) icon by [Freepik](https://www.flaticon.com/authors/freepik) from [flaticon.com](https://www.flaticon.com/)
- [Plane](https://www.flaticon.com/free-icon/plane_129500) icon by [Freepik](https://www.flaticon.com/authors/freepik) from [flaticon.com](https://www.flaticon.com/)
- [Home](https://www.flaticon.com/free-icon/home_553416?term=home&page=1&position=45) icon by [Freepik](https://www.flaticon.com/authors/freepik) from [flaticon.com](https://www.flaticon.com/)
- [F1](https://www.flaticon.com/free-icon/f1_2418779?term=f1&page=1&position=8&page=1&position=8&related_id=2418779&origin=search) icon by [Freepik](https://www.flaticon.com/authors/freepik) from [flaticon.com](https://www.flaticon.com/)


By Joseph Libasora

Last updated: 18.MAY.2023
