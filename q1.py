from abc import abstractmethod
import tkinter as tk
import sqlite3 as sl

class CommandHistory():
    """
    Class for keep track of commands history
    """
    def __init__(self):
        self.history = []

    def push(self, command):
        self.history.append(command)

    def pop(self):
        self.history.pop()

class Client():
    """
    Class for implementing Client GUI to use the bank application
    """
    def __init__(self):
        self.ws = tk.Tk()
        self.ws.title('Cliente GUI')
        self.ws.geometry('800x600')
        self.ws.config(bg="#ffffd7")

        # tk.Frames
        frame = tk.Frame(self.ws, padx=20, pady=20)
        frame.pack(expand=True)

        # tk.Labels
        tk.Label(
            frame, 
            text="Cliente GUI",
            font=("Times", "24", "bold")
            ).grid(row=0, columnspan=4, pady=10)

        tk.Label(
            frame, 
            text='Conta',
            font=("Times", "14")
            ).grid(row=1, column=0, pady=5)

        tk.Label(
            frame, 
            text='Senha', 
            font=("Times", "14")
            ).grid(row=2, column=0, pady=5)

        tk.Label(
            frame, 
            text='Conta destinatária',
            font=("Times", "14")
            ).grid(row=3, column=0, pady=5)

        tk.Label(
            frame, 
            text='Valor',
            font=("Times", "14")
            ).grid(row=4, column=0, pady=5)

        # tk.Entry
        account = tk.Entry(frame, width=30)
        password = tk.Entry(frame, width=30)
        receiver = tk.Entry(frame, width=30)
        amount = tk.Entry(frame, width=30)

        account.grid(row=1, column=1)
        password.grid(row=2, column=1)
        receiver.grid(row=3, column=1)
        amount.grid(row=4, column=1)


        # tk.Button 
        balance_button = tk.Button(
            frame, 
            text="Consultar saldo", 
            padx=20, pady=10, 
            relief=tk.RAISED, 
            font=("Times", "14", "bold"), 
            command=lambda: self.balance_handler(account.get(), password.get())
            )

        balance_button.grid(row=5, column=0, pady=10)

        # tk.Buttons
        extract_button = tk.Button(frame, text="Consultar extrato", padx=0, pady=10, relief=tk.RAISED, font=("Times", "14", "bold"),
            command=lambda: self.extract_handler(account.get(), password.get()))
        extract_button.grid(row=5, column=1, pady=10)

        transfer_button = tk.Button(frame, text="Transferir", padx=0, pady=10, relief=tk.RAISED, font=("Times", "14", "bold"),
            command=lambda: self.transfer_handler(account.get(), password.get(), receiver.get(), amount.get()))
        transfer_button.grid(row=5, column=2, pady=10)

        register_button = tk.Button(frame, text="Cadastrar", padx=0, pady=10, relief=tk.RAISED, font=("Times", "14", "bold"),
            command=lambda: self.register_handler(account.get(), password.get(), amount.get()))
        register_button.grid(row=5, column=3, pady=10)

    def balance_handler(self, account, password):
        """
        Balance implementation, which calls BalanceCommand
        """
        app = Application()
        balance_command = BalanceCommand(app, self)
        balance_command.account = account
        balance_command.password = password
        b = balance_command.execute()
        if isinstance(b, str):
            msg = b
        else:
            msg = "Seu saldo é " + str(b)
        popup = tk.Toplevel()
        popup.wm_title("Saldo")
        l = tk.Label(popup, text=msg)
        l.grid(row=0, column=0)
        exit = tk.Button(popup, text="Ok", command=popup.destroy)
        exit.grid(row=1, column=0)
    
    def extract_handler(self, account, password):
        """
        Extract implementation, which calls ExtractCommand
        """
        app = Application()
        extract_command = ExtractCommand(app, self)
        extract_command.account = account
        extract_command.password = password
        e = extract_command.execute()
        if e == "Conta ou senha inválidos":
            msg = "Conta ou senha inválidos"
        else:
            msg = "Seu extrato é " + str(e)
        popup = tk.Toplevel()
        popup.wm_title("Extrato")
        l = tk.Label(popup, text=msg)
        l.grid(row=0, column=0)
        exit = tk.Button(popup, text="Ok", command=popup.destroy)
        exit.grid(row=1, column=0)

    def transfer_handler(self, account, password, receiver, amount):
        """
        Transfer implementation, which calls TransferCommand
        """
        app = Application()
        transfer_command = TransferCommand(app, self)
        transfer_command.account = account
        transfer_command.password = password
        transfer_command.receiver = receiver
        transfer_command.amount = amount
        t = transfer_command.execute()
        if isinstance(t, str):
            msg = t
        else:
            msg = "Transferência feita com sucesso!"
        popup = tk.Toplevel()
        popup.wm_title("Transferência")
        l = tk.Label(popup, text=msg)
        l.grid(row=0, column=0)
        exit = tk.Button(popup, text="Ok", command=popup.destroy)
        exit.grid(row=1, column=0)

    def register_handler(self, account, password, amount):
        """
        Registration implementation, which calls RegisterCommand
        """
        app = Application()
        register_command = RegisterCommand(app, self)
        register_command.account = account
        register_command.password = password
        register_command.amount = amount
        r = register_command.execute()
        if isinstance(r, str):
            msg = r
        else:
            msg = "Conta cadastrada!"
        popup = tk.Toplevel()
        popup.wm_title("Conta cadastrada")
        l = tk.Label(popup, text=msg)
        l.grid(row=0, column=0)
        exit = tk.Button(popup, text="Ok", command=popup.destroy)
        exit.grid(row=1, column=0)
    
    def main_loop(self):
        self.ws.mainloop()   


class Application():
    """
    Bank app class, which implements the funcionalities and communicates with database
    """
    def __init__(self):
        self.history = CommandHistory()
        con = sl.connect('app.db')
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY,
                        account integer,
                        password text,
                        balance real,
                        extract text
                    )''')
        con.close()

    def login(self, account, password):
        """
        Login method
        """
        if len(self.get_account(account)) == 0:
            return False
        acc = self.get_account(account)[0]
        return password == acc['password']

    def deserialize(self, serialized_data):
        """
        Deserialize auxiliar method
        """
        account = {}
        account['id'] = serialized_data[0]
        account['account'] = serialized_data[1]
        account['password'] = serialized_data[2]
        account['balance'] = serialized_data[3]
        account['extract'] = serialized_data[4]
        return account

    def register(self, account, password, amount):
        """
        Account registrator method
        """
        if len(self.get_account(account)) > 0:
            return "Conta já existente"
        con = sl.connect('app.db')
        cur = con.cursor()
        table = 'accounts'
        columns = '(account, password, balance, extract)'
        cur.execute("INSERT INTO {0}{1} VALUES (?, ?, ?, ?)".format(table, columns), (int(account), password, float(amount), ''))
        con.commit()
        con.close()
        return True

    def get_account(self, account):
        """
        Get account by number of account
        """
        con = sl.connect('app.db')
        cur = con.cursor()
        table = 'accounts'
        cur.execute("SELECT * FROM {0} WHERE account=?".format(table), (account,))
        accounts = cur.fetchall()
        con.close()
        if len(accounts) > 0:
            return [self.deserialize(accounts[0])]
        return []

    def get_balance(self, account, password):
        """
        Get balance of acount if password is correct
        """
        if self.login(account, password):
            acc = self.get_account(account)[0]
            return acc['balance']
        else:
            return "Conta ou senha inválidos"

    def get_extract(self, account, password):
        """
        Get extract of acount if password is correct
        """
        if self.login(account, password):
            acc = self.get_account(account)[0]
            return acc['extract']
        else:
            return "Conta ou senha inválidos"

    def transfer(self, account, password, receiver, amount):
        """
        Transfer amount from account to receiver if password is correct
        """
        amount = float(amount)
        if self.login(account, password):
            acc = self.get_account(account)[0]
            if acc['balance'] < amount:
                return "Saldo insuficiente"
            new_balance = acc['balance'] - amount
            con = sl.connect('app.db')
            cur = con.cursor()
            table = 'accounts'
            cur.execute("UPDATE {0} SET balance = {1} WHERE account=?".format(table, new_balance), (account,))
            con.commit()
            
            acc = self.get_account(receiver)
            if len(acc) == 0:
                return "Conta destinatária inexistente"
            new_balance = acc[0]["balance"] + amount
            cur.execute("UPDATE {0} SET balance = {1} WHERE account=?".format(table, new_balance), (receiver,))
            con.commit()
            con.close()
            return True
        return "Conta ou senha inválidos"


class Command():
    """
    Command abstract class
    """
    def __init__(self, app, client):
        self.app = app
        self.client = client

    @abstractmethod
    def execute(self):
        pass


class BalanceCommand(Command):
    """
    Balance command class (inherits from Command abstract class)
    """
    def execute(self):
        return self.app.get_balance(self.account, self.password)


class ExtractCommand(Command):
    """
    Extract command class (inherits from Command abstract class)
    """
    def execute(self):
        return self.app.get_extract(self.account, self.password)


class TransferCommand(Command):
    """
    Transfer command class (inherits from Command abstract class)
    """
    def execute(self):
        return self.app.transfer(self.account, self.password, self.receiver, self.amount)


class RegisterCommand(Command):
    """
    Register command class (inherits from Command abstract class)
    """
    def execute(self):
        return self.app.register(self.account, self.password, self.amount)

def run():
    client = Client()
    client.main_loop()

if __name__ == '__main__':
    run()