# Stock Guru
## Features
1. Forecast Closing Price values of various stocks for next 30 days
* Live stock data is fetched from yahoo finance using python yfinance library to make predictions
* LSTM deep learning model has been used to make predictions
2. Maintain Portfolio of invested stocks 
3. Maintain Wishlist to keep track of stocks 
4. Participate in discussions and post queries regarding stock market 
## Tech Stack Used
1. FrontEnd 
* HTML used for structuring the webapp
* CSS used for styling the webapp
* Javascript used for bulding a dynamic webapp
2. BackEnd
* Python django framework for creating the webapp
## Project Components
1. Libraries
* absl-py==1.0.0
* argcomplete==1.12.3
* argon2-cffi==21.3.0
* argon2-cffi-bindings==21.2.0
* asgiref==3.4.1
* astor==0.8.1
* astunparse==1.6.3
* attrs==21.2.0
* backcall==0.2.0
* beautifulsoup4==4.4.1
* bleach==4.1.0
* cached-property==1.5.2
* cachetools==4.2.4
* certifi==2021.10.8
* cffi==1.15.0
* charset-normalizer==2.0.9
* chart-studio==1.1.0
* click==8.0.3
* colorama==0.4.4
* colorlover==0.3.0
* convertdate==2.3.2
* cufflinks==0.17.3
* cycler==0.11.0
* debugpy==1.5.1
* decorator==5.1.0
* defusedxml==0.7.1
* Django==3.2.10
* django-crispy-forms==1.13.0
* djangorestframework==3.13.1
* entrypoints==0.3
* flatbuffers==2.0
* fonttools==4.28.5
* gast==0.2.2
* google-auth==2.3.3
* google-auth-oauthlib==0.4.6
* google-pasta==0.2.0
* greenlet==1.1.2
* grpcio==1.43.0
* gunicorn==20.1.0
* h5py==3.6.0
* hijri-converter==2.2.2
* holidays==0.11.3.1
* html-table-parser==0.1.0
* html-table-parser-python3==0.2.0
* idna==3.3
* importlib-metadata==4.10.0
* importlib-resources==5.4.0
* ipykernel==6.6.0
* ipython==7.30.1
* ipython-genutils==0.2.0* 
* ipywidgets==7.6.5
* jedi==0.18.1
* Jinja2==3.0.3
* joblib==1.1.0
* jsonschema==4.3.2
* jupyter==1.0.0
* jupyter-client==7.1.0
* jupyter-console==6.4.0
* jupyter-core==4.9.1
* jupyterlab-pygments==0.1.2
* jupyterlab-widgets==1.0.2
* keras==2.7.0
* Keras-Applications==1.0.8
* Keras-Preprocessing==1.1.2
* kiwisolver==1.3.2
* korean-lunar-calendar==0.2.1
* libclang==12.0.0
* lxml==4.7.1
* Markdown==3.3.6
* MarkupSafe==2.0.1
* matplotlib==3.5.1
* matplotlib-inline==0.1.3
* mistune==0.8.4
* multitasking==0.0.10
* mysqlclient==2.1.0
* nbclient==0.5.9
* nbconvert==6.3.0
* nbformat==5.1.3
* nest-asyncio==1.5.4
* notebook==6.4.6
* nsepy==0.8
* numpy==1.21.5
* oauthlib==3.1.1
* opt-einsum==3.3.0
* packaging==21.3
* pandas==1.3.5
* pandas-datareader==0.10.0
* pandocfilters==1.5.0
* parso==0.8.3
* pickleshare==0.7.5
* Pillow==8.4.0
* plotly==5.5.0
* prometheus-client==0.12.0
* prompt-toolkit==3.0.24
* protobuf==3.19.1
* psycopg2==2.9.2
* pyasn1==0.4.8
* pyasn1-modules==0.2.8
* pycparser==2.21
* Pygments==2.10.0
* PyMeeus==0.5.11
* PyMySQL==1.0.2
* pyparsing==3.0.6
* pyrsistent==0.18.0
* python-dateutil==2.8.2
* python-dotenv==0.19.2
* pytz==2021.3
* pyzmq==22.3.0
* qtconsole==5.2.2
* QtPy==1.11.3
* requests==2.26.0
* requests-futures==1.0.0
* requests-oauthlib==1.3.0
* retrying==1.3.3
* rsa==4.8
* scikit-learn==1.0.1
* scipy==1.7.3
* Send2Trash==1.8.0
* six==1.16.0
* sklearn==0.0
* SQLAlchemy==1.4.28
* sqlparse==0.4.2
* tenacity==8.0.1
* tensorboard==2.7.0
* tensorboard-data-server==0.6.1
* tensorboard-plugin-wit==1.8.0
* tensorflow-cpu==2.7.0
* tensorflow-cpu-estimator==1.15.1
* tensorflow-estimator==2.7.0
* tensorflow-io-gcs-filesystem==0.23.1
* termcolor==1.1.0
* terminado==0.12.1
* testpath==0.5.0
* threadpoolctl==3.0.0
* tornado==6.1
* tqdm==4.62.3
* traitlets==5.1.1
* typing_extensions==4.0.1
* urllib3==1.26.7
* wcwidth==0.2.5
* webencodings==0.5.1
* Werkzeug==2.0.2
* whitenoise==5.3.0
* widgetsnbextension==3.5.2
* wrapt==1.13.3
* yfinance==0.1.68
* zipp==3.6.0

2. UI Components
* Button 
* Form
* Icon
* Input Field
* Navigation Bar
* Selection field
## Installation
1. Instructions to visit web app
* visit link : https://stockguruweb.pythonanywhere.com/

2. Instructions to RUN the project locally
* Download the project folder
* Install necessary dependencies by typing `pip install -r requirements.txt` in command prompt in the folder containing requirements.txt file
* In the root directory of project, type `python manage.py runserver` in command prompt
* Django will serve the webapp at localhost and will provide the link in command prompt
* Visit the link and explore the webapp

## Screenshots
### Covid 19 Trend Predictor
![predict](https://user-images.githubusercontent.com/73059947/125186505-51090380-e248-11eb-8abc-e46cbb35d440.jpg)


### Covid 19 Tweet Sentiment Analyzer
![sentiment](https://user-images.githubusercontent.com/73059947/147418228-5c51cc75-848b-4d2f-9d7a-af7267ceef6e.png)


### Covid 19 Fake News Detector
![fakenews](https://user-images.githubusercontent.com/73059947/147418279-4346fc83-5192-4f0c-b66d-722de3f79d9f.png)


### Covid 19 Article Summarizer
![summarize](https://user-images.githubusercontent.com/73059947/147418295-426b52f1-31f4-4661-878f-8f46457c8ba0.png)


### Covid 19 Chatbot
![chatbot](https://user-images.githubusercontent.com/73059947/147418238-ed9f105e-fdc6-4279-88d2-86b33336ab34.png)
