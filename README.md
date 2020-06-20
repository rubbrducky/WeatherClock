# Yet another simple weather clock using Python and a Waveshare 4.2 inch e-ink display
 
I wanted a more readable bedside clock and to learn some Python so what could be better than a weather clock project? Turned out pretty well I think, though I probably spent as much time on layout as figuring out Python. Might explain any amateurish coding mistakes :-)

Currently running on a headless Raspberry Zero W, which with HDMI, USB, unnecessary services etc disabled draws around 0.25W-0.3W at idle. A cron job runs the script every 5 minutes which is precise enough for my purposes, new weather forecast is downloaded hourly.

Requires [Waveshare's epd library](https://github.com/waveshare/e-Paper/tree/master/RaspberryPi%26JetsonNano/python/lib/waveshare_epd) and uses [Roboto bold and regular](https://fonts.google.com/specimen/Roboto). Weather forecast is fetched from [yr.no](https://hjelp.yr.no/hc/en-us/articles/360009342833-XML-weather-forecasts); symbols also from yr but pre-converted to grayscale.


# Here it is in full grayscale glory:

<img src="https://github.com/rubbrducky/WeatherClock/blob/master/clock.png">