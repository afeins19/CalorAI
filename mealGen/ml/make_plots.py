# generates plots and saves them as base64 files

import matplotlib.pyplot as plt
import os
import base64

# creates and saves a plot 
def make_and_save_plot(x, y, title, model_name, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=model_name)
    plt.title(title)
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.legend()
    plt.grid(True)
    
    # static/plots_images
    static_path = os.path.join('static', 'plot_images', filename)
    plt.savefig(static_path)
    plt.close()
    return static_path

# save as base64 
def to_base64(filename):
    file_path = f"static/plot_images/{filename}"
    with open(file_path, "rb") as img: 
        encoded_img = base64.b64encode(img.read()).decode('utf-8')
    return encoded_img
