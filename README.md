To run the app, you need an API key from OpenWeatherMap and a city code. The app fetches weather forecast data and calculates the Soil Humidity Index.

The Soil Humidity Index is based on four parameters: rain, humidity, temperature, and wind speed. If the index is higher than 2, irrigation is not recommended. However, since this is a practical exam for a Python course focused on Django, the index itself is not particularly relevant.

The code displays the results in a table on the web and on the Sense HAT Simulator. On the simulator, the text appears in green if irrigation is needed and in red if it is not. Since the results are first generated on the Sense HAT Simulator, it may take up to 10 seconds for the table to appear.
