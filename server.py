from fastapi import FastAPI, HTTPException
from requests_html import HTMLSession

app = FastAPI()
session = HTMLSession()

def scrape_weather_data(place):
    url = f'https://www.google.com/search?q=weather+{place}'
    request = session.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
    
    # Check if the request was successful
    if request.status_code != 200:
        raise HTTPException(status_code=request.status_code, detail=f"Failed to retrieve data. Status code: {request.status_code}")

    try:
        temperature = request.html.find('span#wob_tm', first=True).text
        unit = request.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
        description = request.html.find('div.VQF4g', first=True).find('span#wob_dc', first=True).text

        return {"place": place, "temperature": temperature, "unit": unit, "description": description}
    except AttributeError:
        raise HTTPException(status_code=500, detail="Failed to retrieve weather data.")

@app.get("/search-weather")
def search_weather(place: str):
    weather_data = scrape_weather_data(place)
    return weather_data
