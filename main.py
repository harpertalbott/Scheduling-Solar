# Harper Talbott

import customtkinter
import model

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")

# Placeholder credentials — replace with a proper auth system before production use.
CORRECT_USERNAME = "user"
CORRECT_PASSWORD = "pass"


class PredictionPage(customtkinter.CTkToplevel):
    """
    Secondary window that collects job parameters and displays the predicted install duration.

    Opened automatically after a successful login. Trains the regression model on
    initialization and exposes a Calculate button that calls the model with the
    user-supplied inputs.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("600x580")
        self.title("Solar Panel Installation")

        self._trained_model, self._feature_names = model.train_model_and_generate_equation()

        self._build_ui()

    def _build_ui(self):
        title_label = customtkinter.CTkLabel(
            self,
            text="Solar Panel Installation Duration Prediction Model",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=20)

        input_frame = customtkinter.CTkFrame(self)
        input_frame.pack(expand=True, padx=20, pady=20)

        # Panel quantity
        customtkinter.CTkLabel(input_frame, text="Quantity of Panels:", font=("Arial", 18), anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self._panels_entry = customtkinter.CTkEntry(input_frame, placeholder_text="Enter number of panels", font=("Arial", 18), width=200)
        self._panels_entry.grid(row=0, column=1, padx=10, pady=10)

        # Number of arrays
        customtkinter.CTkLabel(input_frame, text="Number of Arrays:", font=("Arial", 18), anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self._arrays_entry = customtkinter.CTkEntry(input_frame, placeholder_text="Enter number of arrays", font=("Arial", 18), width=200)
        self._arrays_entry.grid(row=1, column=1, padx=10, pady=10)

        # Employees
        customtkinter.CTkLabel(input_frame, text="Number of Onsite Employees:", font=("Arial", 18), anchor="w").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self._employees_entry = customtkinter.CTkEntry(input_frame, placeholder_text="Enter number of employees", font=("Arial", 18), width=200)
        self._employees_entry.grid(row=2, column=1, padx=10, pady=10)

        # Season
        customtkinter.CTkLabel(input_frame, text="Installation Season:", font=("Arial", 18), anchor="w").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self._season_dropdown = customtkinter.CTkComboBox(input_frame, values=["Spring", "Summer", "Fall", "Winter"], font=("Arial", 18), width=200)
        self._season_dropdown.grid(row=3, column=1, padx=10, pady=10)

        # Drive time
        customtkinter.CTkLabel(input_frame, text="Total Drive Time (hours):", font=("Arial", 18), anchor="w").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self._drive_entry = customtkinter.CTkEntry(input_frame, placeholder_text="Enter drive time in hours", font=("Arial", 18), width=200)
        self._drive_entry.grid(row=4, column=1, padx=10, pady=10)

        self._result_label = customtkinter.CTkLabel(self, text="", font=("Arial", 18))
        self._result_label.pack(pady=10)

        customtkinter.CTkButton(self, text="Calculate", font=("Arial", 20), command=self._calculate, width=200).pack(pady=20)
        customtkinter.CTkButton(self, text="Close", font=("Arial", 20), command=self._close, width=200).pack(pady=20)

    def _predict_duration(self, panel_qty, num_arrays, installation_season, number_of_employees):
        """Build the feature dict and return predicted labor hours from the model."""
        input_data = {name: 0 for name in self._feature_names}
        input_data['Panel QTY'] = panel_qty
        input_data['# of Arrays'] = num_arrays
        input_data['Estimated Total # of People on Site'] = number_of_employees

        for season in ['Spring', 'Summer', 'Winter']:
            season_key = f'Install Season_{season}'
            if season_key in input_data:
                input_data[season_key] = 1 if installation_season == season else 0

        return model.predict_duration(self._trained_model, self._feature_names, input_data)

    def _calculate(self):
        """Read inputs, run prediction, and display the result (or an error message)."""
        try:
            panel_qty = int(self._panels_entry.get())
            num_arrays = int(self._arrays_entry.get())
            number_of_employees = int(self._employees_entry.get())
            installation_season = self._season_dropdown.get()
            drive_time = float(self._drive_entry.get())

            prediction = self._predict_duration(panel_qty, num_arrays, installation_season, number_of_employees)
            total_time = prediction + drive_time

            self._result_label.configure(text=f"Predicted Total Duration: {total_time:.2f} hours", text_color="green")
        except ValueError:
            self._result_label.configure(text="Invalid input. Please check your values.", text_color="red")

    def _close(self):
        self.destroy()
        self.master.deiconify()


class LoginPage(customtkinter.CTk):
    """
    Root application window that handles user authentication.

    On successful login the window hides itself and opens PredictionPage.
    On close, PredictionPage calls deiconify() to restore this window.
    """

    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.title("Login")

        self._build_ui()

    def _build_ui(self):
        frame = customtkinter.CTkFrame(self)
        frame.pack(expand=True, padx=30, pady=30)

        customtkinter.CTkLabel(frame, text="Login System", font=("Arial", 32, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        customtkinter.CTkLabel(frame, text="Username:", font=("Arial", 20), anchor="w").grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self._username_entry = customtkinter.CTkEntry(frame, placeholder_text="Enter username", font=("Arial", 20), width=300)
        self._username_entry.grid(row=1, column=1, padx=15, pady=10)

        customtkinter.CTkLabel(frame, text="Password:", font=("Arial", 20), anchor="w").grid(row=2, column=0, padx=15, pady=10, sticky="w")
        self._password_entry = customtkinter.CTkEntry(frame, placeholder_text="Enter password", show="*", font=("Arial", 20), width=300)
        self._password_entry.grid(row=2, column=1, padx=15, pady=10)

        self._error_label = customtkinter.CTkLabel(frame, text="", font=("Arial", 16), text_color="red")
        self._error_label.grid(row=3, column=0, columnspan=2)

        customtkinter.CTkButton(frame, text="Login", font=("Arial", 20), command=self._login, width=200).grid(row=4, column=0, columnspan=2, pady=30)

    def _login(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            self.withdraw()
            PredictionPage(self)
        else:
            self._error_label.configure(text="Invalid username or password")


if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
