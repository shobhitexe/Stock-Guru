# Stock Guru
Stock Guru is a web application that can forecast the closing price of stocks for the next 30 days. Nowadays many people invest in stocks and require to make informed decisions to gain profits. Stock Guru can assist such individuals by predicting the trend of the closing price of stocks using Deep Learning LSTM model. Since the stock market is highly volatile and unpredictable, Stock Guru was developed to analyze how well the LSTM model can forecast closing prices of stocks
<br>
<br>

## Features
1. Maintain portfolio of invested stocks 
2. Participate in discussions and post queries regarding stock market 
3. Maintain wishlist to keep track of stocks 
4. Forecast closing price values of various stocks for next 30 days
    * Live stock data is fetched from yahoo finance using python yfinance library
    * LSTM deep learning model is used to make predictions
<br>

## Tech Stack
1. Front-End 
    * HTML used for structuring the web application
    * CSS used for styling the web application
    * Javascript used for bulding a dynamic web application
    
2. Back-End
    * Python django framework used for creating the web application
<br>

## Installation
1. Instructions to visit web application
   * Visit link : https://stockguruweb.pythonanywhere.com/

2. Instructions to RUN the project locally
   * Download the project folder
   * Install necessary dependencies by typing `pip install -r requirements.txt` in command prompt in the folder containing requirements.txt file
   * In the root directory of project, type `python manage.py runserver` in command prompt
   * Django will serve the web application on localhost and will provide the link in command prompt
   * Visit the link and explore the web application
<br>

## Screenshots

### Landing Page
![land](https://user-images.githubusercontent.com/73059947/148243369-cd2c8a9e-51c8-425e-a48e-e09f2d0f0887.png)
<br>
<br>
<br>

### Discussion Page
![discuss](https://user-images.githubusercontent.com/73059947/148243456-2c88b234-997d-4021-bdbe-dd14c6455579.png)
<br>
<br>
<br>

### Portfolio and Watchlist Page
![portfolio](https://user-images.githubusercontent.com/73059947/148243553-2df0952f-16d3-4239-b6bc-1072887ebd92.png)
<br>
<br>
<br>

### Create Post Page
![post](https://user-images.githubusercontent.com/73059947/148243705-54b5e036-5e1f-42ad-8a37-06e2de90e189.png)
<br>
<br>
<br>

### Stock Price Prediction Page
![predict](https://user-images.githubusercontent.com/73059947/148243864-65352adc-a6b6-4856-9ff5-ff001f2393f7.png)
<br>
<br>
<br>

### Result Page
![result](https://user-images.githubusercontent.com/73059947/148244003-bd51915f-d74e-4050-9e76-f48f908e92c8.png)
