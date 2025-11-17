import tkinter as tk
from tkinter import ttk
import speedtest
import threading

class SpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        style = ttk.Style(self.root)
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TButton', font=('Helvetica', 12, 'bold'))
        style.configure('Result.TLabel', font=('Helvetica', 12, 'bold'), foreground='blue')

        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Ping:").grid(row=0, column=0, sticky="w", pady=5)
        self.ping_result_var = tk.StringVar(value="0.00 ms")
        ttk.Label(main_frame, textvariable=self.ping_result_var, style='Result.TLabel').grid(row=0, column=1, sticky="w")

        ttk.Label(main_frame, text="Download Speed:").grid(row=1, column=0, sticky="w", pady=5)
        self.download_result_var = tk.StringVar(value="0.00 Mbps")
        ttk.Label(main_frame, textvariable=self.download_result_var, style='Result.TLabel').grid(row=1, column=1, sticky="w")

        ttk.Label(main_frame, text="Upload Speed:").grid(row=2, column=0, sticky="w", pady=5)
        self.upload_result_var = tk.StringVar(value="0.00 Mbps")
        ttk.Label(main_frame, textvariable=self.upload_result_var, style='Result.TLabel').grid(row=2, column=1, sticky="w")

        self.start_button = ttk.Button(main_frame, text="Start Test", command=self.start_test_thread)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.status_var = tk.StringVar(value="Click 'Start Test' to begin")
        ttk.Label(main_frame, textvariable=self.status_var, font=('Helvetica', 10)).grid(row=4, column=0, columnspan=2)

    def start_test_thread(self):
        self.start_button.config(state="disabled", text="Testing...")
        test_thread = threading.Thread(target=self.run_speed_test)
        test_thread.start()

    def run_speed_test(self):
        try:
            st = speedtest.Speedtest()

            self.status_var.set("Finding the best server...")
            st.get_best_server()

            self.status_var.set("Measuring download speed...")
            download_speed = st.download()
            download_mbps = round(download_speed / 1_000_000, 2)
            self.download_result_var.set(f"{download_mbps} Mbps")

            self.status_var.set("Measuring upload speed...")
            upload_speed = st.upload()
            upload_mbps = round(upload_speed / 1_000_000, 2)
            self.upload_result_var.set(f"{upload_mbps} Mbps")
            
            ping = st.results.ping
            self.ping_result_var.set(f"{ping:.2f} ms")

            self.status_var.set("Test complete!")

        except speedtest.SpeedtestException as e:
            self.status_var.set(f"Error: {e}")
        except Exception as e:
            self.status_var.set("An internet connection is required.")
        finally:
            self.start_button.config(state="normal", text="Start Test")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTestApp(root)
    root.mainloop()