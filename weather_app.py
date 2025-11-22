import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit

from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    # initializer for our class, runs after python creates the weather app
    # sets up everything the app needs to work
    def __init__(self):
        # calls the parent class initializer
        super().__init__()
        # label prompts user to enter name of city
        self.city_label = QLabel("Enter city name: ", self)
        # input box that allows user to type name of city
        self.city_input = QLineEdit(self)
        # button to retrieve weather info
        self.get_weather_button = QPushButton("Get Weather", self)
        # temperature lable will display temperature of city
        self.temp_label = QLabel(self)
        # emoji label will show type of weather
        self.emoji_label = QLabel(self)
        # brief description of type of weather
        self.description_label = QLabel(self)
        self.initUI()
    
    # this is where we will be designing the user interface
    def initUI(self):
        # changes name of window title
        self.setWindowTitle("Weather App")

        # declares vbox will have a vertical box layout
        vbox = QVBoxLayout()

        # adds our widgets to the vbox 
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        # passes in our vertical layout manager to set as the layout
        self.setLayout(vbox)

        # aligns all widgets to be in center of the window
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # sets the object names
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input {
                font-size: 40px;
                padding: 5px;
            }
            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temp_label {
                font-size: 75px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label {
                font-size: 50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    # this function will handle getting the weather information from the api
    def get_weather(self):
        # our weather api key
        api_key = "a3de1f101a983776abb61853a0600548"
        # captures city text inputted to look up
        city = self.city_input.text()
        print(f"{city} weather:")
        # url link from the openweathermap website which will return to us the weather from the city inputted
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        # surround our code in a try block that may raise any exceptions
        try:
            # response makes the api request with our url
            response = requests.get(url)
            # this method will raise an exception if there is any http errors
            response.raise_for_status()
            # once we get our data, we convert to json
            data = response.json()

            # if our request code = 200 it means our api request was successful and we will display our weather data
            if data["cod"] == 200:
                print("api request successful")
                self.display_weather(data)

        # catches out http errors in different cases based on status code
        except requests.exceptions.HTTPError as HTTPError:
            match response.status_code:
                case 400:
                    print("bad request:\nplease check your input")
                    self.display_error("bad request:\nplease check your input")
                case 401:
                    print("unauthorized:\ninvalid api key")
                    self.display_error("unauthorized:\ninvalid api key")
                case 403:
                    print("forbidden:\naccess is denied")
                    self.display_error("forbidden:\naccess is denied")
                case 404:
                    print("not found:\ncity not found")
                    self.display_error("not found:\ncity not found")
                case 500:
                    print("internal server error:\nplease try again later")
                    self.display_error("internal server error:\nplease try again later")
                case 502:
                    print("bad gateway:\ninvalid response from the server")
                    self.display_error("bad gateway:\ninvalid response from the server")
                case 503:
                    print("service unavailable:\nserver is down")
                    self.display_error("service unavailable:\nserver is down")
                case 504:
                    print("gateway timeout:\nno response from the server")
                    self.display_error("gateway timeout:\nno response from the server")
                case _:
                    print(f"HTTP error occured:\n{HTTPError}")
                    self.display_error(f"HTTP error occured:\n{HTTPError}")
        # catches any connection errors
        except requests.exceptions.ConnectionError:
            print("connection error:\ncheck your internet connection")
            self.display_error("connection error:\ncheck your internet connection")
        # ctaches any time out errors
        except requests.exceptions.Timeout:
            print("timeout error:\nthe request timed out")
            self.display_error("timeout error:\nthe request timed out")
        # catches any too many redirect errors
        except requests.exceptions.TooManyRedirects:
            print("too many redirects:\ncheck the url")
            self.display_error("too many redirects:\ncheck the url")
        # catches any other potential error
        except requests.exceptions.RequestException as req_error:
            print(f"request error:\n{req_error}")
            self.display_error(f"request error:\n{req_error}")

    # this function will handle displaying an error message when needed
    def display_error(self, message):
        self.temp_label.setStyleSheet("font-size: 30px;")
        self.temp_label.setText(message)

        # clears both the emoji and description after displaying an error message
        self.emoji_label.clear()
        self.description_label.clear()

    # this function will handle displaying the weather after retrieving it from the api
    def display_weather(self, data):
        # resets font size because if we print an error, then the temperature, the temperature appears with 30px font size
        self.temp_label.setStyleSheet("font-size: 75px;")

        # grabs temperature from data (located in main sub level temp)
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15 # converts to celsius
        temperature_f = (temperature_k * 9/5) - 459.67 # converts to fahrenheit
        # displays temperatures to the secondth decimal place
        print(f"kelvin: {temperature_k:.2f}°K")
        print(f"celsius: {temperature_c:.2f}°C")
        print(f"fahrenheit: {temperature_f:.2f}°F")

        # here we will access the weather id number with key "weather" at index [0] and at key "id"
        weather_id = data["weather"][0]["id"]
        print(f"weather id: {weather_id}")

        # here we will access the weather description with key "weather" at index [0] and at key "description"
        weather_description = data["weather"][0]["description"]
        print(f"weather description: {weather_description}")

        # here we will access the humidity percentage and print into the console
        humidity_percentage = data["main"]["humidity"]
        print(f"humidity: {humidity_percentage}%")

        # displays only fahrenheit in the application
        self.temp_label.setText(f"{temperature_f:.2f}°F")
        # displays the weather emoji based on the weather id value
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        # displays the weather description
        self.description_label.setText(weather_description)

    # this function will handle getting a weather id and turning it into an emoji
        # 200s = thunderstorm
        # 300s = drizzle
        # 500s = rain
        # 600s = snow
        # 700s = atmosphere
        # 800  = clear
        # 801-804 = clouds
    @staticmethod # belongs to class but doesnt require an instant specific data or method; used more as a utility tool
    def get_weather_emoji(weather_id):
        # here we display the different emojis for the different weather id's
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781: 
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""

# when running python file directly
if __name__ == "__main__":
    # creates the Qt application and handles any arguments
    app = QApplication(sys.argv)
    # construct our weather app 
    weather_app = WeatherApp()
    # show our weather app 
    weather_app.show()
    # weather app remains visible until exited
    sys.exit(app.exec_())