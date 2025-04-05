import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QListWidgetItem
)
from PyQt5.QtCore import QTimer

GET_URL = "http://127.0.0.1:5000/team"
POST_URL = "http://127.0.0.1:5000/teams"
PUT_DELETE_URL = "http://127.0.0.1:5000/teams"

class TeamManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Team Manager")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.coach_input = QLineEdit()
        self.city_input = QLineEdit()

        layout.addWidget(QLabel("Team Name"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Coach"))
        layout.addWidget(self.coach_input)
        layout.addWidget(QLabel("City"))
        layout.addWidget(self.city_input)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.update_button = QPushButton("Update")
        self.delete_button = QPushButton("Delete")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        self.team_list = QListWidget()
        layout.addWidget(self.team_list)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_team)
        self.update_button.clicked.connect(self.update_team)
        self.delete_button.clicked.connect(self.delete_team)
        self.team_list.itemClicked.connect(self.populate_fields)

        self.selected_team_id = None
        self.teams_data = []

        # ✅ Load teams after UI is fully initialized
        QTimer.singleShot(100, self.load_teams)

    def load_teams(self):
        self.team_list.clear()
        self.teams_data.clear()
        self.selected_team_id = None
        try:
            response = requests.get(GET_URL)
            print("DEBUG Raw Text Response:", response.text)
            response.raise_for_status()
            data = response.json()
            print("DEBUG Parsed JSON:", data)

            if not isinstance(data, list):
                raise ValueError(f"Expected list, got {type(data)}: {data}")

            for team in data:
                if all(k in team for k in ("id", "name", "coach", "city")):
                    item_text = f"{team['name']} - {team['coach']} ({team['city']})"
                    item = QListWidgetItem(item_text)
                    item.setData(1000, team['id'])
                    self.team_list.addItem(item)
                    self.teams_data.append(team)

        except Exception as e:
            print("ERROR in load_teams:", repr(e))
            QMessageBox.critical(self, "Error", f"Failed to load teams: {str(e)}")

    def populate_fields(self, item):
        self.selected_team_id = item.data(1000)
        team = next((t for t in self.teams_data if t['id'] == self.selected_team_id), None)
        if team:
            self.name_input.setText(team['name'])
            self.coach_input.setText(team['coach'])
            self.city_input.setText(team['city'])

    def add_team(self):
        data = {
            "name": self.name_input.text(),
            "coach": self.coach_input.text(),
            "city": self.city_input.text()
        }
        try:
            response = requests.post(POST_URL, json=data)
            if response.status_code == 201:
                self.clear_inputs()
                self.load_teams()
            else:
                self.show_error(response)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_team(self):
        if not self.selected_team_id:
            QMessageBox.warning(self, "Select Team", "Please select a team to update.")
            return
        data = {
            "name": self.name_input.text(),
            "coach": self.coach_input.text(),
            "city": self.city_input.text()
        }
        try:
            response = requests.put(f"{PUT_DELETE_URL}/{self.selected_team_id}", json=data)
            if response.status_code == 200:
                self.clear_inputs()
                self.load_teams()
            else:
                self.show_error(response)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_team(self):
        if not self.selected_team_id:
            QMessageBox.warning(self, "Select Team", "Please select a team to delete.")
            return
        try:
            response = requests.delete(f"{PUT_DELETE_URL}/{self.selected_team_id}")
            if response.status_code == 200:
                self.clear_inputs()
                self.load_teams()
            else:
                self.show_error(response)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def clear_inputs(self):
        self.name_input.clear()
        self.coach_input.clear()
        self.city_input.clear()
        self.selected_team_id = None
        self.team_list.clearSelection()

    def show_error(self, response):
        try:
            msg = response.json().get("error", f"Status Code: {response.status_code}")
        except:
            msg = f"Status Code: {response.status_code}"
        QMessageBox.warning(self, "Error", msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TeamManager()
    window.show()
    sys.exit(app.exec_())
