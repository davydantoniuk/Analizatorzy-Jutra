import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd

# Загрузка данных из CSV
def load_data():
    data = pd.read_csv('car_prices.csv')  # Убедитесь, что путь к файлу корректен
    return data

# Функция, которая обновляет список моделей в зависимости от выбранного бренда
def update_models(event):
    selected_brand = brand_var.get()
    filtered_data = car_data[car_data['make'] == selected_brand]
    models = filtered_data['model'].unique()
    models = [str(model).strip() for model in models]
    model_combobox['values'] = models
    model_combobox.current(0)

# Функция, которая вызывается при нажатии кнопки Calculate
def calculate():
    selected_brand = brand_var.get()
    selected_year = year_var.get()
    selected_month = month_var.get()
    odometer = max_odometer_var.get()
    condition = min_condition_var.get()
    price = max_price_var.get()

    print(f"Selected Brand: {selected_brand}, Year: {selected_year}, Month: {selected_month}")
    print(f"Odometer: {odometer}, Condition: {condition}, Price: {price}")

# Загрузка данных
car_data = load_data()

# Приведение данных в порядок
car_data['make'] = car_data['make'].astype(str)
car_data = car_data[car_data['make'].apply(lambda x: isinstance(x, str))]
brands = sorted(car_data['make'].unique())

# Основное окно
root = tk.Tk()
root.title("Car Sales Prediction")
root.geometry('700x500')  # Увеличиваем размеры окна

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Frame для всех виджетов
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="nsew")

frame.grid_columnconfigure(0, weight=1)  # Центрируем содержимое
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_rowconfigure(4, weight=1)  # Добавляем еще одну строку для месяца

# Переменные для хранения выбранных значений
brand_var = tk.StringVar()
model_var = tk.StringVar()
year_var = tk.StringVar()  # Переменная для года как текст
month_var = tk.StringVar()  # Переменная для месяца

# Переменные для новых полей
max_odometer_var = tk.StringVar()
min_condition_var = tk.StringVar()
max_price_var = tk.StringVar()

# Виджет для выбора бренда
ttk.Label(frame, text="Brand:").grid(column=0, row=0, padx=5, pady=5, sticky=tk.E)
brand_combobox = ttk.Combobox(frame, textvariable=brand_var, values=brands)
brand_combobox.set("Select Brand")
brand_combobox.bind("<<ComboboxSelected>>", update_models)
brand_combobox.grid(column=1, row=0, padx=5, pady=5)

# Виджет для выбора месяца
ttk.Label(frame, text="Month:").grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
months = list(range(1, 13))  # Список месяцев от 1 до 12
month_combobox = ttk.Combobox(frame, textvariable=month_var, values=months)
month_combobox.set("Select Month")
month_combobox.grid(column=1, row=1, padx=5, pady=5)

# Перемещаем виджет для ввода года под "Month"
ttk.Label(frame, text="Year:").grid(column=0, row=2, padx=5, pady=5, sticky=tk.E)
year_entry = ttk.Entry(frame, textvariable=year_var)  # Замена на Entry для свободного ввода
year_entry.grid(column=1, row=2, padx=5, pady=5)

# Кнопка для выполнения программы
calculate_button = ttk.Button(frame, text="Calculate", command=calculate)
calculate_button.grid(column=0, row=4, columnspan=4, padx=5, pady=10, sticky=tk.EW)

# Добавляем поля для Max Odometer, Min Condition, Max Price по правой стороне
ttk.Label(frame, text="Odometer:").grid(column=2, row=0, padx=5, pady=5, sticky=tk.W)
odometer_entry = ttk.Entry(frame, textvariable=max_odometer_var)
odometer_entry.grid(column=3, row=0, padx=5, pady=5)

ttk.Label(frame, text="Condition:").grid(column=2, row=1, padx=5, pady=5, sticky=tk.W)
condition_entry = ttk.Entry(frame, textvariable=min_condition_var)
condition_entry.grid(column=3, row=1, padx=5, pady=5)

ttk.Label(frame, text="Price:").grid(column=2, row=2, padx=5, pady=5, sticky=tk.W)
price_entry = ttk.Entry(frame, textvariable=max_price_var)
price_entry.grid(column=3, row=2, padx=5, pady=5)

# Добавление изображения
def load_image():
    # Загрузка изображения
    image_path = 'atlas.png'  # Убедитесь, что путь к изображению правильный
    img = Image.open(image_path)
    img = img.resize((700, 300), Image.Resampling.LANCZOS)  # Изменяем размер изображения
    img_tk = ImageTk.PhotoImage(img)

    # Создание виджета Label для изображения
    image_label = ttk.Label(root, image=img_tk)
    image_label.image = img_tk  # Сохраняем ссылку на изображение, чтобы оно отображалось
    image_label.grid(column=0, row=3, sticky='nsew', padx=10, pady=10, columnspan=4)

# Загрузка изображения после создания всех виджетов
load_image()

# Настройка весов для изображения
root.grid_rowconfigure(1, weight=1)

# Запуск основного цикла приложения
root.mainloop()
