import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os


# ============================================================
# CONFIGURATION
# ============================================================

APP_TITLE = "Mobile Sampling WSN"


# ============================================================
# MAIN APPLICATION
# ============================================================

class MobileSamplingApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            APP_TITLE
        )

        self.root.geometry(
            "1100x700"
        )

        self.root.configure(
            bg="#f4f6f8"
        )

        self.create_header()

        self.create_main_content()

        self.create_footer()


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#1f2937",
            height=100
        )

        header.pack(
            fill="x"
        )

        title = tk.Label(
            header,
            text="Mobile Sampling of Sensor Field Data",
            font=("Arial", 25, "bold"),
            fg="white",
            bg="#1f2937"
        )

        title.pack(
            pady=(18, 3)
        )

        subtitle = tk.Label(
            header,
            text="Band-Based Directional Broadcast",
            font=("Arial", 13),
            fg="#d1d5db",
            bg="#1f2937"
        )

        subtitle.pack()


    # ========================================================
    # MAIN CONTENT
    # ========================================================

    def create_main_content(self):

        container = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )

        container.pack(
            expand=True,
            fill="both",
            padx=35,
            pady=30
        )

        # ----------------------------------------------------
        # PROJECT DESCRIPTION
        # ----------------------------------------------------

        description = tk.Frame(
            container,
            bg="white",
            bd=1,
            relief="solid"
        )

        description.pack(
            fill="x",
            pady=(0, 25)
        )

        tk.Label(
            description,
            text="Project Overview",
            font=("Arial", 17, "bold"),
            bg="white"
        ).pack(
            anchor="w",
            padx=25,
            pady=(18, 8)
        )

        overview = (
            "This system simulates energy-efficient mobile sampling "
            "in a wireless sensor network. Sensor nodes collect data "
            "and a mobile sink moves through predefined sampling points. "
            "Band-Based Directional Broadcast restricts communication "
            "toward the mobile sink to reduce unnecessary transmissions."
        )

        tk.Label(
            description,
            text=overview,
            font=("Arial", 11),
            bg="white",
            justify="left",
            wraplength=1000
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )


        # ----------------------------------------------------
        # BUTTON AREA
        # ----------------------------------------------------

        button_frame = tk.Frame(
            container,
            bg="#f4f6f8"
        )

        button_frame.pack(
            pady=15
        )

        self.create_button(
            button_frame,
            "▶  RUN SIMULATION",
            self.run_simulation,
            0
        )

        self.create_button(
            button_frame,
            "🚗  LIVE ANIMATION",
            self.run_animation,
            1
        )

        self.create_button(
            button_frame,
            "📊  VIEW RESULTS",
            self.view_results,
            2
        )

        self.create_button(
            button_frame,
            "📈  VIEW GRAPHS",
            self.view_graphs,
            3
        )


        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        self.result_frame = tk.Frame(
            container,
            bg="white",
            bd=1,
            relief="solid"
        )

        self.result_frame.pack(
            fill="both",
            expand=True,
            pady=20
        )

        tk.Label(
            self.result_frame,
            text="Simulation Status",
            font=("Arial", 17, "bold"),
            bg="white"
        ).pack(
            pady=(25, 15)
        )

        self.status_label = tk.Label(
            self.result_frame,
            text="Ready to start simulation",
            font=("Arial", 13),
            bg="white"
        )

        self.status_label.pack(
            pady=10
        )


    # ========================================================
    # BUTTON
    # ========================================================

    def create_button(
        self,
        parent,
        text,
        command,
        column
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 12, "bold"),
            padx=25,
            pady=15,
            width=18
        )

        button.grid(
            row=0,
            column=column,
            padx=8
        )


    # ========================================================
    # FOOTER
    # ========================================================

    def create_footer(self):

        footer = tk.Label(
            self.root,
            text="Energy-Efficient Wireless Sensor Network Simulation",
            font=("Arial", 10),
            bg="#f4f6f8",
            fg="#6b7280"
        )

        footer.pack(
            pady=10
        )


    def run_simulation(self):

        self.status_label.config(
            text="Running sensor network simulation..."
        )

        self.root.update()

        try:

            result = subprocess.run(
                [sys.executable, "main.py"],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:

                self.status_label.config(
                    text="Simulation failed"
                )

                messagebox.showerror(
                    "Simulation Error",
                    result.stderr
                )

                return

            self.status_label.config(
                text="Simulation completed successfully"
            )

            messagebox.showinfo(
                "Success",
                "Simulation completed successfully.\n\n"
                "Results and graphs have been generated."
            )

        except Exception as error:

            self.status_label.config(
                text="Simulation failed"
            )

            messagebox.showerror(
                "Error",
                str(error)
            )


    # ========================================================
    # ANIMATION
    # ========================================================

    def run_animation(self):

        self.status_label.config(
            text="Starting live sensor-field animation..."
        )

        self.root.update()

        try:

            subprocess.Popen(
                [
                    sys.executable,
                    "animated_simulation.py"
                ]
            )

        except Exception as error:

            messagebox.showerror(
                "Animation Error",
                str(error)
            )


    # ========================================================
    # RESULTS
    # ========================================================

    def view_results(self):

        result_window = tk.Toplevel(
            self.root
        )

        result_window.title(
            "Simulation Results"
        )

        result_window.geometry(
            "650x500"
        )

        result_window.configure(
            bg="white"
        )

        tk.Label(
            result_window,
            text="Simulation Results",
            font=("Arial", 20, "bold"),
            bg="white"
        ).pack(
            pady=20
        )

        results = [
            ("Sensor Nodes", "80"),
            ("Sampling Points", "25"),
            ("Normal Broadcast Energy", "755.20"),
            ("Directional Broadcast Energy", "560.20"),
            ("Energy Reduction", "25.82%"),
            ("Normal Transmissions", "6960"),
            ("Directional Transmissions", "5335"),
            ("Normal Delivery Ratio", "100%"),
            ("Directional Delivery Ratio", "100%")
        ]

        for name, value in results:

            frame = tk.Frame(
                result_window,
                bg="white"
            )

            frame.pack(
                fill="x",
                padx=60,
                pady=6
            )

            tk.Label(
                frame,
                text=name,
                font=("Arial", 11),
                bg="white",
                anchor="w"
            ).pack(
                side="left"
            )

            tk.Label(
                frame,
                text=value,
                font=("Arial", 11, "bold"),
                bg="white"
            ).pack(
                side="right"
            )


    # ========================================================
    # GRAPHS
    # ========================================================

    def view_graphs(self):

        graph_files = [

            "network_simulation.png",

            "energy_comparison.png",

            "transmissions_comparison.png",

            "delivery_comparison.png",

            "energy_over_time.png"

        ]

        existing_files = []

        for file in graph_files:

            if os.path.exists(file):

                existing_files.append(file)

        if not existing_files:

            messagebox.showwarning(
                "No Graphs",
                "Please run the simulation first."
            )

            return

        for file in existing_files:

            try:

                os.startfile(
                    os.path.abspath(file)
                )

            except Exception as error:

                print(error)


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    application = MobileSamplingApp(
        root
    )

    root.mainloop()