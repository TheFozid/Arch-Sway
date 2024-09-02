#!/usr/bin/env python

import subprocess
from pyquery import PyQuery  # install using `pip install pyquery`
import json

# weather icons ☀󰖙󰖙󰖨🌒󰖔☁󰅟󰖐🌧❄🌪 🌧️ Nerd Fonts 
weather_icons = {
    "sunnyDay": '<span size="medium">☀️</span>',
    "clearNight": '<span size="medium">🌜</span>',
    
    "cloudyFoggyDay": '<span size="medium">☁️</span>',
    "cloudyFoggyNight": '<span size="medium">☁️</span>',
    "rainyDay": '<span size="medium">🌧️</span>',
    "rainyNight": '<span size="medium">🌧️</span>',
    "snowyIcyDay": '<span size="medium">❄️☀️</span>',
    "snowyIcyNight": '<span size="medium">❄️🌜"</span>',
    "severe": '<span size="medium">🌧️🌬️</span>',
    "default": "-",
}

# to get your own location_id, go to https://weather.com & search your location.
# once you choose your location, you can see the location_id in the URL(64 chars long hex string)
# like this: https://weather.com/en-IN/weather/today/l/c3e96d6cc4965fc54f88296b54449571c4107c73b9638c16aafc83575b4ddf2e
location_id = "874a6d973612cc8f223855924e450c778c256adaa5ddcc6770e8dfdef984e6e9"  # TODO
#location_id = "c3e96d6cc4965fc54f88296b54449571c4107c73b9638c16aafc83575b4ddf2e"

# get html page
url = "https://weather.com/en-GB/weather/today/l/" + location_id
html_data = PyQuery(url=url)

url2 = "https://weather.com/en-GB/weather/tenday/l/" + location_id
html_data2 = PyQuery(url=url2)

url3 = "https://weather.com/en-GB/weather/hourbyhour/l/" + location_id
html_data3 = PyQuery(url=url3)

# current temperature
temp = html_data("span[data-testid='TemperatureValue']").eq(0).text()
# print(temp)

# current status phrase
status = html_data("div[data-testid='wxPhrase']").text()
status = f"{status[:22]}.." if len(status) > 23 else status
# print(status)

# current status phrase
insight = html_data("section[aria-label='Precipitation intensity card']").text().split(".")[0]#.split("@")[1]
insight = insight.replace("\n.","")
insight = insight.replace(".","")
insight = f"{insight}.."
# print(status)

# status code
status_code = html_data("#regionHeader").attr("class").split(" ")[2].split("-")[2]
# print(status_code)

# status icon
icon = (
    weather_icons[status_code]
    if status_code in weather_icons
    else weather_icons["default"]
)
# print(icon)

# temperature feels like
temp_feel = html_data(
    "div[data-testid='FeelsLikeSection'] > span > span[data-testid='TemperatureValue']"
).text()
temp_feel_text = f"Feels like {temp_feel}C"
# print(temp_feel_text)

# min-max temperature
temp_min = (
    html_data("div[data-testid='wxData'] > span[data-testid='TemperatureValue']")
    .eq(1)
    .text()
)
temp_max = (
    html_data("div[data-testid='wxData'] > span[data-testid='TemperatureValue']")
    .eq(0)
    .text()
)
temp_min_max = f"🌡️High/Low\t{temp_max}C / {temp_min}C"
# print(temp_min_max)

# wind speed
wind_text = html_data3("span[data-testid='Wind']").text()#.split("\n")[1].split(" ")[0]
wind_text = wind_text.replace("NNE ","🢇 ")
wind_text = wind_text.replace("NNW ","🢆 ")
wind_text = wind_text.replace("SSE ","🢄 ")
wind_text = wind_text.replace("SSW ","🢅 ")
wind_text = wind_text.replace("ENE ","🢇 ")
wind_text = wind_text.replace("WNW ","🢆 ")
wind_text = wind_text.replace("ESE ","🢄 ")
wind_text = wind_text.replace("WSW ","🢅 ")
wind_text = wind_text.replace("NE ","🢇 ")
wind_text = wind_text.replace("NW ","🢆 ")
wind_text = wind_text.replace("SE ","🢄 ")
wind_text = wind_text.replace("SW ","🢅 ")
wind_text = wind_text.replace("W ","🢂 ")
wind_text = wind_text.replace("E ","🢀 ")
wind_text = wind_text.replace("N ","🢃 ")
wind_text = wind_text.replace("S ","🢁 ")
wind_text = f"{wind_text}"
# print(wind_text)

# humidity
humidity = html_data("span[data-testid='PercentageValue']").text()
humidity_text = f"💧 {humidity}"
# print(humidity_text)

# uv
uv = html_data("span[data-testid='UVIndexValue']").text()
uv = f"☀️ {uv}"
# print(uv)

# uv
sunrise = html_data("div[data-testid='SunriseValue']").text()
sunrise = sunrise.replace("Sun Rise\n","")
sunrise = f"☀️🢁 {sunrise}"
# print(uv)

# uv
sunset = html_data("div[data-testid='SunsetValue']").text()
sunset = sunset.replace("Sunset\n","")
sunset = f"{sunset}☀️🢃"
# print(uv)

# visibility
visbility = html_data("span[data-testid='VisibilityValue']").text()
visbility_text = f"👀 {visbility}"
# print(visbility_text)

# air quality index
air_quality_index = html_data("text[data-testid='DonutChartValue']").text()
# print(air_quality_index)

prediction1 = html_data("section[aria-label='Hourly Forecast']")(
    "div[data-testid='SegmentPrecipPercentage'] > span"
).text()
prediction1 = prediction1.replace("Chance of Rain","\t")
prediction1 = f"\n☔{prediction1}" if len(prediction1) > 0 else prediction1

prediction2 = html_data("section[aria-label='Hourly Forecast']")(
	"div[data-testid='SegmentHighTemp'] > span"
).text()
prediction2 = prediction2.replace(" ","C\t")
prediction2 = prediction2.replace("°C","°")
prediction2 = prediction2.replace("°","°C")
prediction2 = f"\n 🌡️ \t{prediction2}" if len(prediction2) > 0 else prediction2

prediction3 = html_data("section[aria-label='Daily Forecast']")(
    "div[data-testid='SegmentPrecipPercentage'] > span"
).text()
prediction3 = prediction3.replace("Chance of Rain","\t")
prediction3 = f"\n☔{prediction3}" if len(prediction3) > 0 else prediction3

prediction4 = html_data("section[aria-label='Daily Forecast']")(
	"div[data-testid='SegmentHighTemp'] > span"
).text()
prediction4 = prediction4.replace("° /","°/")
prediction4 = prediction4.replace("- /","-/")
prediction4 = prediction4.replace(" ","\t")
prediction4 = f"\n 🌡️ \t{prediction4}" if len(prediction4) > 0 else prediction4

predictiontitle = html_data2("section[aria-label='10-Day Weather']")(
	"div[data-testid='DetailsSummary'] > h2"
).text()
predictiontitle = predictiontitle.replace("Tonight","Today")
from string import digits
s = predictiontitle
predictiontitle = predictiontitle.maketrans('', '', digits)
predictiontitle = s.translate(predictiontitle)
predictiontitle = predictiontitle.replace("  "," ")
predictiontitle = predictiontitle.replace(" ","\t")
predictiontitle = f"\nDaily\t{predictiontitle}"

predictiontitle1 = html_data3("section[aria-label='Hourly Weather']")(
	"div[data-testid='DetailsSummary'] > h2"
).text()
predictiontitle1 = predictiontitle1.replace(":00 ","h\t")
predictiontitle1 = predictiontitle1.replace("\t0h","\t00h")
predictiontitle1 = predictiontitle1.replace("\t1h","\t01h")
predictiontitle1 = predictiontitle1.replace("\t2h","\t02h")
predictiontitle1 = predictiontitle1.replace("\t3h","\t03h")
predictiontitle1 = predictiontitle1.replace("\t4h","\t04h")
predictiontitle1 = predictiontitle1.replace("\t5h","\t05h")
predictiontitle1 = predictiontitle1.replace("\t6h","\t06h")
predictiontitle1 = predictiontitle1.replace("\t7h","\t07h")
predictiontitle1 = predictiontitle1.replace("\t8h","\t08h")
predictiontitle1 = predictiontitle1.replace("\t9h","\t09h")
predictiontitle1 = f" {predictiontitle1}"
predictiontitle1 = predictiontitle1.replace(" 0h","00h")
predictiontitle1 = predictiontitle1.replace(" 1h","01h")
predictiontitle1 = predictiontitle1.replace(" 2h","02h")
predictiontitle1 = predictiontitle1.replace(" 3h","03h")
predictiontitle1 = predictiontitle1.replace(" 4h","04h")
predictiontitle1 = predictiontitle1.replace(" 5h","05h")
predictiontitle1 = predictiontitle1.replace(" 6h","06h")
predictiontitle1 = predictiontitle1.replace(" 7h","07h")
predictiontitle1 = predictiontitle1.replace(" 8h","08h")
predictiontitle1 = predictiontitle1.replace(" 9h","09h")
predictiontitle1 = predictiontitle1.replace(" ","")
predictiontitle1 = f"Hourly\t{predictiontitle1}"


location1 = html_data2("span[data-testid='PresentationName']").text()
location1 = f"{location1}"

# tooltip text
tooltip_text = str.format(
    "{}\t{} {}\n{}\n{}\n\n{}\n{}\n{}\n\n{}{}{}\n{}{}{}\n\n{}",
    f'<span size="xx-large">{temp}C</span>',
    f'<span size="xx-large">{icon}</span>',
    f'<span size="xx-large">{status}</span>',
    f"<small>{temp_feel_text}</small>\t<big>{location1}</big>",
    f'<span size="medium">{insight}</span>',
    f"<big>{temp_min_max}</big>",
    f"<big>🌬️ {wind_text[:8]}\t{humidity_text}</big>",
    f"<big>{visbility_text}\tAQI {air_quality_index}\t{uv}</big>",
    f"{predictiontitle1[:27]}",
    f"<big>{prediction1}</big>",
    f"<big>{prediction2}</big>",
    f"<big>{predictiontitle[:29]}</big>",    
    f"<big>{prediction3}</big>",
    f'<span size="medium">{prediction4}</span>',
    f"{sunrise}\t\t\t\t{sunset}",
)

# print waybar module data
out_data = {
    "text": f"{icon} {temp}C {wind_text[:8]}",
    "alt": status,
    "tooltip": tooltip_text,
    "class": status_code,
}
print(json.dumps(out_data))
