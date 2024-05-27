import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ComparisonGUI:
    def __init__(self, master):
        self.master = master
        master.title("Comparison of Highlight Extraction Methods")

        self.summary_report = """
        Summary Report: Comparison of Highlight Extraction Methods

        1. Existing Method (CNN):
           - Accuracy: 84.7%
           - Time Taken: 118 seconds

        2. Rule-based Method:
           - Accuracy: 93.2%
           - Time Taken: 13 seconds

        3. YOLO:
           - Accuracy: 98.4%
           - Time Taken: 181 seconds

        Conclusion:
        - The rule-based method offers a balance between accuracy and processing speed.
        - YOLO achieves high accuracy but at the cost of longer processing time.
        - The proposed rule-based method is efficient in terms of both accuracy and time taken.
        """

        # Simulated data for comparison
        methods = ['Existing Method (CNN)', 'Rule-based Method', 'YOLO']
        accuracy = [84.7, 93.2, 98.4]
        time_taken = [118, 13, 181]

        # Create a DataFrame to store the data
        data = pd.DataFrame({'Method': methods, 'Accuracy (%)': accuracy, 'Time Taken (seconds)': time_taken})

        # Plot the comparison graph
        plt.figure(figsize=(8, 4))
        plt.bar(data['Method'], data['Accuracy (%)'], color=['blue', 'green', 'orange'])
        plt.title('Comparison of Highlight Extraction Methods')
        plt.xlabel('Method')
        plt.ylabel('Accuracy (%)')
        plt.ylim(0, 100)
        plt.grid(axis='y')
        for i, acc in enumerate(data['Accuracy (%)']):
            plt.text(i, acc + 1, f"{acc}%", ha='center', va='bottom', fontweight='bold')
        self.accuracy_vs_time_canvas = FigureCanvasTkAgg(plt.gcf(), master=self.master)
        self.accuracy_vs_time_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Display summary report
        self.summary_label = tk.Label(master, text="Summary Report", font=("Helvetica", 12), padx=10, pady=10)
        self.summary_label.pack()
        self.summary_text = scrolledtext.ScrolledText(master, width=80, height=15, wrap=tk.WORD)
        self.summary_text.pack()
        self.summary_text.insert(tk.INSERT, self.summary_report)
        self.summary_text.config(state=tk.DISABLED)

        # Plot accuracy vs time graph
        self.plot_accuracy_vs_time()

    def plot_accuracy_vs_time(self):
        # Simulated data for accuracy vs time
        methods = ['Existing Method (CNN)', 'Rule-based Method', 'YOLO']
        accuracy = [84.7, 93.2, 98.4]
        time_taken = [118, 13, 181]

        # Create a DataFrame to store the data
        data = pd.DataFrame({'Method': methods, 'Accuracy (%)': accuracy, 'Time Taken (seconds)': time_taken})

        # Plot accuracy vs time graph
        plt.figure(figsize=(8, 4))
        plt.plot(data['Time Taken (seconds)'], data['Accuracy (%)'], marker='o')
        plt.title('Accuracy vs Time Taken')
        plt.xlabel('Time Taken (seconds)')
        plt.ylabel('Accuracy (%)')
        plt.grid(True)
        for i, (acc, time) in enumerate(zip(data['Accuracy (%)'], data['Time Taken (seconds)'])):
            plt.text(time, acc, f"{acc}%", ha='left', va='bottom', fontweight='bold')
        self.accuracy_vs_time_canvas = FigureCanvasTkAgg(plt.gcf(), master=self.master)
        self.accuracy_vs_time_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root = tk.Tk()
app = ComparisonGUI(root)
root.mainloop()
