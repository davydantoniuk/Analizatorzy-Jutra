import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
from tensorflow.keras.models import load_model  # type: ignore
import modeling

model = load_model('model.keras')
model.compile(optimizer="adam", loss='mean_squared_error')


def load_data():
    data = pd.read_csv('cars.csv')
    return data


def calculate():
    selected_brand = brand_var.get()
    selected_year = year_var.get()
    odometer = max_odometer_var.get()
    condition = min_condition_var.get()
    price = max_price_var.get()

    new_observation = pd.DataFrame({
        'make': [selected_brand],
        'year': [float(selected_year)],
        'condition': [float(condition)],
        'odometer': [float(odometer)],
        'sellingprice': [float(price)]
    })

    new_observation = pd.get_dummies(new_observation, drop_first=True)
    new_observation = new_observation.reindex(
        columns=modeling.X_train.columns, fill_value=0)
    new_observation[["year", "condition", "odometer", "sellingprice"]] = modeling.scaler.transform(
        new_observation[["year", "condition", "odometer", "sellingprice"]])
    prediction = model.predict(new_observation)

    print(f"Predicted sales_count: {prediction[0]}")
    prediction_label.config(
        text=f"Predicted amount: {round(float(prediction[0][0]))}")


def update_models(event):
    selected_brand = brand_var.get()
    filtered_data = car_data[car_data['make'] == selected_brand]
    models = filtered_data['model'].unique()
    models = [str(model).strip() for model in models]
    model_combobox['values'] = models
    model_combobox.current(0)


car_data = load_data()


car_data['make'] = car_data['make'].astype(str)
car_data = car_data[car_data['make'].apply(lambda x: isinstance(x, str))]
brands = sorted(car_data['make'].unique())


root = tk.Tk()
root.title("Car Sales Prediction")
root.geometry('700x600')

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="nsew")

frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_rowconfigure(4, weight=1)


brand_var = tk.StringVar()
model_var = tk.StringVar()
year_var = tk.StringVar()
predicted_price = tk.StringVar()


max_odometer_var = tk.StringVar()
min_condition_var = tk.StringVar()
max_price_var = tk.StringVar()


ttk.Label(frame, text="Brand:").grid(
    column=0, row=0, padx=5, pady=5, sticky=tk.E)
brand_combobox = ttk.Combobox(frame, textvariable=brand_var, values=brands)
brand_combobox.set("Select Brand")
brand_combobox.grid(column=1, row=0, padx=5, pady=5)
brand_combobox.bind("<<ComboboxSelected>>", update_models)

ttk.Label(frame, text="Model:").grid(
    column=0, row=1, padx=5, pady=5, sticky=tk.E)
model_combobox = ttk.Combobox(frame, textvariable=model_var)
model_combobox.set("Select Model")
model_combobox.bind("<<ComboboxSelected>>")
model_combobox.grid(column=1, row=1, padx=5, pady=5)

ttk.Label(frame, text="Year:").grid(
    column=0, row=2, padx=5, pady=5, sticky=tk.E)
year_entry = ttk.Entry(frame, textvariable=year_var)
year_entry.grid(column=1, row=2, padx=5, pady=5)

ttk.Label(frame, text="Price:").grid(
    column=2, row=0, padx=5, pady=5, sticky=tk.W)
price_entry = ttk.Entry(frame, textvariable=max_price_var)
price_entry.grid(column=3, row=0, padx=5, pady=5)


ttk.Label(frame, text="Odometer:").grid(
    column=2, row=1, padx=5, pady=5, sticky=tk.W)
odometer_entry = ttk.Entry(frame, textvariable=max_odometer_var)
odometer_entry.grid(column=3, row=1, padx=5, pady=5)

ttk.Label(frame, text="Condition (0-50):").grid(column=2,
                                                row=2, padx=5, pady=5, sticky=tk.W)
condition_entry = ttk.Entry(frame, textvariable=min_condition_var)
condition_entry.grid(column=3, row=2, padx=5, pady=5)

calculate_button = ttk.Button(frame, text="Calculate", command=calculate)
calculate_button.grid(column=0, row=4, columnspan=4,
                      padx=5, pady=10, sticky=tk.EW)

prediction_label = ttk.Label(frame, text="Predicted amount: ")
prediction_label.grid(column=0, row=5, columnspan=4,
                      padx=5, pady=5, sticky=tk.W)


def load_image():
    image_path = 'imageApp.png'
    img = Image.open(image_path)
    img = img.resize((700, 300), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    image_label = ttk.Label(root, image=img_tk)
    image_label.image = img_tk
    image_label.grid(column=0, row=3, sticky='nsew',
                     padx=10, pady=10, columnspan=4)


load_image()
root.grid_rowconfigure(1, weight=1)
root.mainloop()
