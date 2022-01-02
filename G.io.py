from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QLineEdit, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QFont, QIcon
from PyQt6 import QtWidgets
import requests  # Send a GET call to the API
import folium  # Creating the map with the inputted IP
import sys
import io  # to save and store the folium created html link

# Create a class to store and create all the data
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("G.io")
        self.setFixedSize(200, 250)
        self.setStyleSheet("background-color: #FFFFFF;")
        self.setWindowIcon(QIcon('icon.png'))

        # Create Button
        self.Button1 = QtWidgets.QPushButton(self)
        self.Button1.setStyleSheet(
            "QPushButton"
            "{"
            "background: #ffeaa7; border-radius: 3px; color: black; border: 2px solid #ff826e"
            "}"
            "QPushButton::pressed{background-color : #FFFFFF;"
            "}"
        )
        self.Button1.setText("IP To Map")
        self.Button1.move(50, 75)

        # Create a label
        enter_IP_label = QLabel("Enter an IP", self)
        enter_IP_label.move(63, 7)
        enter_IP_label.setFont(QFont('Arial', 12))

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(35, 40)
        self.textbox.resize(130, 20)
        self.textbox.setStyleSheet(
            "background: #ffeaa7; border-radius: 3px; border: 2px solid #ff826e"
        )

        # When button clicked, call function IP_To_Map_new_Window
        self.Button1.clicked.connect(self.IP_To_Map_new_Window)

    # Create a function for the new Dialog window and to manage the inputted IP and IP to mapmaker
    def IP_To_Map_new_Window(self):
        # Creating the new Dialog window
        newWin = QDialog(self)
        newWin.setWindowTitle("IP To Map")
        newWin.setFixedSize(1280, 720)

        # Creating a label for the map
        layout = QVBoxLayout()
        newWin.setLayout(layout)

        # Get the inputted IP from the textbox
        IP = self.textbox.text()
        # Send a GET request to the public API
        url = requests.get("http://ip-api.com/json/" + IP).json()
        if not url["status"] == "fail" and len(IP) > 0:
            # Store the latitude and the longitude to a list
            cord = (url["lat"], url["lon"])
            # Create the map with the given IP
            map = folium.Map(location=cord, zoom_start=16)
            # Add a marker
            folium.Marker(cord).add_to(map)

            # Create a virtual saving environment
            data = io.BytesIO()
            # Save the HTML file to the virtual saving environment
            map.save(data, close_file=False)

            # Creating a virtual browser to open the HTML file
            webView = QWebEngineView()
            webView.setHtml(data.getvalue().decode())

            # Add the map to the created browser
            layout.addWidget(webView)
            # Show the full built Dialog
            newWin.show()
        else:
            self.textbox.clear()

if __name__ == "__main__":
    # Create the main window
    app = QApplication(sys.argv)
    win = mainWindow()

    # Show the main window
    win.show()
    sys.exit(app.exec())
