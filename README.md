#  PyRCON GUI

This Python application provides a graphical user interface (GUI) for managing an Unreal Engine server using the Remote Console (RCON) protocol. It allows you to perform actions such as viewing the player list, kicking players, banning players, changing maps, and managing player notes.

## Setup

### Requirements

- Python 3.x
- MySQL Server
- MySQL Connector/Python (`mysql-connector-python`)

### Installation Steps

1. **Clone this repository to your local machine:**

   ```bash
   git clone https://github.com/yourusername/Unreal-Engine-RCON-GUI.git
### Install the required Python packages using pip:

pip install mysql-connector-python

### Set up the MySQL database:

Log in to your MySQL server.
Create a new database for the application.
sql

CREATE DATABASE your_database_name;
Create a table to store player notes:
sql
CREATE TABLE player_notes (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    steam_id VARCHAR(255) NOT NULL,
    player_name VARCHAR(255) NOT NULL,
    notes TEXT
);

host="your_mysql_host",
user="your_mysql_username",
password="your_mysql_password",
database="your_database_name"

### Usage
Run the Python script rcon_gui.py:

bash
Copy code
python rcon_gui.py
The GUI window will open, providing options to interact with the Unreal Engine server.

Click on "Player List" to view the list of players currently on the server.

Click on "Notes for [Player Name]" to view or edit the notes for a specific player. Notes are saved automatically upon closing the notes window.

Use the "Kick Player", "Ban Player", and "Change Map" buttons to perform corresponding actions on the server.

Click on "Disconnect" to close the application and disconnect from the server.

css
Copy code

Feel free to use this README file content directly in your project repository.
