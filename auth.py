import hashlib

class AuthManager:
    def __init__(self, filename="users.txt"):
        self.filename = filename
        self.users = self._load_users()

    def _load_users(self):
        # Default user if file not found
        users = {"admin": hashlib.sha256("admin123".encode()).hexdigest()}
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    u, p = line.strip().split(",")
                    users[u] = p
        except FileNotFoundError:
            self._save_users(users)
        return users

    def _save_users(self, users):
        with open(self.filename, "w") as f:
            for u, p in users.items():
                f.write(f"{u},{p}\n")

    def login(self, username, password):
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        if username in self.users and self.users[username] == hashed_pw:
            return True
        return False
