import tkinter as tk
from tkinter import messagebox
import redis

class TransactionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Nota Transaksi")
        self.master.geometry("400x200")

        self.redis_host = '127.0.0.1'
        self.redis_port = 6379
        self.redis_db = 0
        self.r = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)

        # Label dan Entry untuk input nilai transaksi
        self.label_amount = tk.Label(master, text="Jumlah Transaksi:")
        self.label_amount.pack()

        self.entry_amount = tk.Entry(master)
        self.entry_amount.pack()

        # Tombol untuk mencatat transaksi
        self.record_button = tk.Button(master, text="Catat Transaksi", command=self.record_transaction)
        self.record_button.pack()

    def record_transaction(self):
        try:
            # Mendapatkan nilai transaksi dari Entry
            amount = float(self.entry_amount.get())

            # Menginkrementasi nilai key 'transaction_counter' untuk mendapatkan ID transaksi
            transaction_id = self.r.incr('transaction_counter')

            # Menyimpan transaksi ke Redis menggunakan key yang sesuai dengan ID transaksi
            transaction_key = f'transaction:{transaction_id}'
            self.r.hmset(transaction_key, {'amount': amount})

            messagebox.showinfo("Sukses", f"Transaksi berhasil dicatat dengan ID: {transaction_id}")

        except Exception as e:
            # Menampilkan pesan error jika terjadi masalah
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TransactionApp(root)
    root.mainloop()