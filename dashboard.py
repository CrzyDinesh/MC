import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os


class WSNDashboard:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Mobile Sampling WSN - Dashboard"
        )

        self.root.geometry(
            "1000x650"
        )

        self.root.configure(
            bg="#f2f4f7"
        )

        # ====================================================
        # TITLE
        # ====================================================

        title = tk.Label(
            root,
            text="Mobile Sampling of Sensor Field Data",
            font=("Arial", 24, "bold"),
            bg="#f2f4f7"
        )

        title.pack(
            pady=(20, 5)
        )

        subtitle = tk.Label(
            root,
            text="Band-Based Directional Broadcast",
            font=("Arial", 14),
            bg="#f2f4f7"
        )

        subtitle.pack(
            pady=(0, 20)
        )

        # ====================================================
        # INFORMATION FRAME
        # ====================================================

        info_frame = tk.Frame(
            root,
            bg="#f2f4f7"
        )

        info_frame.pack(
            pady=10
        )

        self.create_card(
            info_frame,
            "Sensor Nodes",
            "80",
            0
        )

        self.create_card(
            info_frame,
            "Sampling Points",
            "25",
            1
        )

        self.energy_card = self.create_card(
            info_frame,
            "Energy Reduction",
            "--",
            2
        )

        self.delivery_card = self.create_card(
            info_frame,
            "Delivery Ratio",
            "--",
            3
        )

        # ====================================================
        # RESULTS FRAME
        # ====================================================

        result_frame = tk.LabelFrame(
            root,
            text="Simulation Results",
            font=("Arial", 13, "bold"),
            bg="#ffffff",
            padx=20,
            pady=20
        )

        result_frame.pack(
            padx=30,
            pady=20,
            fill="x"
        )

        self.normal_energy = tk.StringVar(
            value="--"
        )

        self.directional_energy = tk.StringVar(
            value="--"
        )

        self.normal_transmissions = tk.StringVar(
            value="--"
        )

        self.directional_transmissions = tk.StringVar(
            value="--"
        )

        self.normal_delivery = tk.StringVar(
            value="--"
        )

        self.directional_delivery = tk.StringVar(
            value="--"
        )

        self.create_result_row(
            result_frame,
            "Normal Broadcast Energy",
            self.normal_energy,
            0
        )

        self.create_result_row(
            result_frame,
            "Directional Broadcast Energy",
            self.directional_energy,
            1
        )

        self.create_result_row(
            result_frame,
            "Normal Transmissions",
            self.normal_transmissions,
            2
        )

        self.create_result_row(
            result_frame,
            "Directional Transmissions",
            self.directional_transmissions,
            3
        )

        self.create_result_row(
            result_frame,
            "Normal Delivery Ratio",
            self.normal_delivery,
            4
        )

        self.create_result_row(
            result_frame,
            "Directional Delivery Ratio",
            self.directional_delivery,
            5
        )

        # ====================================================
        # BUTTONS
        # ====================================================

        button_frame = tk.Frame(
            root,
            bg="#f2f4f7"
        )

        button_frame.pack(
            pady=20
        )

        run_button = tk.Button(
            button_frame,
            text="▶  RUN SIMULATION",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=12,
            command=self.run_simulation
        )

        run_button.pack(
            side="left",
            padx=10
        )

        graph_button = tk.Button(
            button_frame,
            text="📊 VIEW GRAPHS",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=12,
            command=self.open_graphs
        )

        graph_button.pack(
            side="left",
            padx=10
        )

        # ====================================================
        # STATUS
        # ====================================================

        self.status = tk.StringVar(
            value="Ready to run simulation"
        )

        status_label = tk.Label(
            root,
            textvariable=self.status,
            font=("Arial", 11),
            bg="#f2f4f7"
        )

        status_label.pack(
            pady=10
        )

    # ========================================================
    # CREATE CARD
    # ========================================================

    def create_card(
        self,
        parent,
        title,
        value,
        column
    ):

        frame = tk.Frame(
            parent,
            bg="white",
            width=200,
            height=100,
            relief="ridge",
            borderwidth=1
        )

        frame.grid(
            row=0,
            column=column,
            padx=10
        )

        frame.pack_propagate(
            False
        )

        tk.Label(
            frame,
            text=title,
            font=("Arial", 11),
            bg="white"
        ).pack(
            pady=(15, 5)
        )

        value_label = tk.Label(
            frame,
            text=value,
            font=("Arial", 20, "bold"),
            bg="white"
        )

        value_label.pack()

        return value_label

    # ========================================================
    # RESULT ROW
    # ========================================================

    def create_result_row(
        self,
        parent,
        title,
        variable,
        row
    ):

        tk.Label(
            parent,
            text=title,
            font=("Arial", 11),
            bg="white",
            anchor="w",
            width=30
        ).grid(
            row=row,
            column=0,
            pady=5
        )

        tk.Label(
            parent,
            textvariable=variable,
            font=("Arial", 11, "bold"),
            bg="white",
            anchor="w"
        ).grid(
            row=row,
            column=1,
            pady=5
        )

    # ========================================================
    # RUN SIMULATION
    # ========================================================

    def run_simulation(self):

        self.status.set(
            "Running simulation..."
        )

        self.root.update()

        try:

            result = subprocess.run(
                [
                    sys.executable,
                    "main.py"
                ],
                capture_output=True,
                text=True
            )

            output = result.stdout

            if result.returncode != 0:

                messagebox.showerror(
                    "Error",
                    result.stderr
                )

                return

            self.parse_results(
                output
            )

            self.status.set(
                "Simulation completed successfully"
            )

            messagebox.showinfo(
                "Simulation Complete",
                "Simulation completed successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ========================================================
    # PARSE OUTPUT
    # ========================================================

    def parse_results(
        self,
        output
    ):

        lines = output.splitlines()

        for line in lines:

            if "Normal energy consumed" in line:

                value = line.split(":")[-1].strip()

                self.normal_energy.set(
                    value
                )

            elif "Directional energy used" in line:

                value = line.split(":")[-1].strip()

                self.directional_energy.set(
                    value
                )

            elif "Energy reduction" in line:

                value = line.split(":")[-1].strip()

                self.energy_card.config(
                    text=value
                )

            elif "Normal transmissions" in line:

                value = line.split(":")[-1].strip()

                self.normal_transmissions.set(
                    value
                )

            elif "Directional transmissions" in line:

                value = line.split(":")[-1].strip()

                self.directional_transmissions.set(
                    value
                )

            elif "Normal delivery ratio" in line:

                value = line.split(":")[-1].strip()

                self.normal_delivery.set(
                    value
                )

            elif "Directional delivery" in line:

                value = line.split(":")[-1].strip()

                self.directional_delivery.set(
                    value
                )

                self.delivery_card.config(
                    text=value
                )

    # ========================================================
    # OPEN GRAPHS
    # ========================================================

    def open_graphs(self):

        graph_files = [
            "network_simulation.png",
            "energy_comparison.png",
            "transmissions_comparison.png",
            "delivery_comparison.png",
            "energy_over_time.png"
        ]

        existing = [
            f for f in graph_files
            if os.path.exists(f)
        ]

        if not existing:

            messagebox.showwarning(
                "No Results",
                "Run the simulation first."
            )

            return

        for file in existing:

            os.startfile(
                os.path.abspath(file)
            )


# ============================================================
# START DASHBOARD
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = WSNDashboard(
        root
    )

    root.mainloop()