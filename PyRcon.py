import mysql.connector
import tkinter as tk
from tkinter import messagebox, simpledialog

class UnrealRcon:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def disconnect(self):
        if self.socket:
            self.socket.close()

    def send_command(self, command):
        if not self.socket:
            raise Exception("Socket is not connected")
        
        # Build RCON packet
        packet = struct.pack('<ii', len(command) + 10, -1) + bytes(command, 'utf-8') + b'\x00\x00'
        packet += struct.pack('<i', len(command) + 10)

        self.socket.send(packet)

        # Receive response
        response = self.socket.recv(4096)
        return response[8:-2].decode('utf-8')  # Remove packet header and footer

class PlayerNotesGUI:
    def __init__(self, master, player_id, steam_id, player_name, db_connection):
        self.master = master
        self.player_id = player_id
        self.steam_id = steam_id
        self.player_name = player_name
        self.db_connection = db_connection

        self.notes_text = tk.Text(master, height=10, width=50)
        self.notes_text.pack()

        self.load_notes()

        self.save_button = tk.Button(master, text="Save Notes", command=self.save_notes)
        self.save_button.pack()

    def load_notes(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT notes FROM player_notes WHERE player_id = %s", (self.player_id,))
        result = cursor.fetchone()
        if result:
            self.notes_text.insert(tk.END, result[0])

    def save_notes(self):
        notes = self.notes_text.get("1.0", tk.END)
        cursor = self.db_connection.cursor()
        cursor.execute("REPLACE INTO player_notes (player_id, steam_id, player_name, notes) VALUES (%s, %s, %s, %s)",
                       (self.player_id, self.steam_id, self.player_name, notes))
        self.db_connection.commit()
        messagebox.showinfo("Notes Saved", "Notes have been saved successfully.")
        self.master.destroy()

class RconGUI:
    def __init__(self, master):
        self.master = master
        master.title("Unreal Engine RCON GUI")

        self.rcon = UnrealRcon('your_server_ip', 27015, 'your_rcon_password')

        self.label = tk.Label(master, text="Unreal Engine RCON GUI")
        self.label.pack()

        self.player_list_button = tk.Button(master, text="Player List", command=self.show_player_list)
        self.player_list_button.pack()

        self.disconnect_button = tk.Button(master, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack()

    def show_player_list(self):
        try:
            self.rcon.connect()
            response = self.rcon.send_command("listplayers")
            players = response.split('\n')
            for player in players:
                player_info = player.split()
                player_id = player_info[0]
                steam_id = player_info[2]
                player_name = player_info[1]
                player_notes_button = tk.Button(self.master, text=f"Notes for {player_name}",
                                                command=lambda id=player_id, steam_id=steam_id, name=player_name: self.open_notes_window(id, steam_id, name))
                player_notes_button.pack()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.rcon.disconnect()

    def open_notes_window(self, player_id, steam_id, player_name):
        notes_window = tk.Toplevel(self.master)
        notes_window.title(f"Player Notes for {player_name}")
        db_connection = mysql.connector.connect(
            host="your_mysql_host",
            user="your_mysql_username",
            password="your_mysql_password",
            database="your_database_name"
        )
        PlayerNotesGUI(notes_window, player_id, steam_id, player_name, db_connection)

    def disconnect(self):
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    gui = RconGUI(root)
    root.mainloop()
