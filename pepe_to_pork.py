import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os
import uuid
from tkinterdnd2 import DND_FILES, TkinterDnD

# Keep a reference to the modified PIL image
modified_image_pil = None

def change_color(image):
    # Convert the image to RGBA
    image = image.convert("RGBA")
    
    # Convert image to numpy array
    data = np.array(image)
    
    # Define the green color range (adjusted values)
    lower_green = np.array([0, 100, 0, 255])
    upper_green = np.array([200, 255, 200, 255])
    
    # Create a mask to identify green pixels
    mask = np.all(data >= lower_green, axis=-1) & np.all(data <= upper_green, axis=-1)
    
    # Replace green pixels with pink
    data[mask] = [255, 105, 180, 255]
    
    # Convert back to PIL image
    new_image = Image.fromarray(data, 'RGBA')
    
    return new_image

def upload_image(file_path=None):
    global modified_image_pil
    if not file_path:
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
    try:
        original_image = Image.open(file_path)
        modified_image_pil = change_color(original_image)
        
        # Display the modified image in the GUI
        display_image(modified_image_pil)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def display_image(image):
    # Resize image for display
    image.thumbnail((400, 400))
    img = ImageTk.PhotoImage(image)
    
    # Update the image label
    image_label.config(image=img)
    image_label.image = img
    placeholder_label.pack_forget()
    close_button.place(relx=1.0, x=-10, y=10, anchor="ne")
    
    # Show the save button
    save_button.pack(pady=20)

def save_image():
    global modified_image_pil
    if not os.path.exists("Results"):
        os.makedirs("Results")
    existing_files = os.listdir("Results")
    numbers = sorted(int(f.split('.')[0]) for f in existing_files if f.split('.')[0].isdigit())
    next_number = numbers[-1] + 1 if numbers else 1
    save_filename = f"{next_number}.png"
    save_path = os.path.join("Results", save_filename)
    modified_image_pil.save(save_path)
    show_notification(f"Image saved as {save_filename} in the Results folder.")

def on_drop(event):
    file_path = event.data.strip('{}')
    if os.path.isfile(file_path):
        upload_image(file_path)

def reset_image_slot():
    image_label.config(image='')
    image_label.image = None
    close_button.place_forget()
    placeholder_label.pack()

def copy_eth_address():
    root.clipboard_clear()
    root.clipboard_append("0x30A657Dd1311c270571F4ccF559dF588FECc9c2a")
    show_notification("Copied")

def show_notification(message):
    notification = tk.Toplevel(root)
    notification.title("Notification")
    notification.geometry("300x100")
    notification.config(bg='lightgreen')
    notification_label = tk.Label(notification, text=message, bg='lightgreen', font=("Helvetica", 12))
    notification_label.pack(pady=10)
    
    close_notification_button = tk.Button(notification, text="Close", command=notification.destroy, bg='green', fg='white')
    close_notification_button.pack(pady=10)
    
    root.after(5000, notification.destroy)  # Auto close after 5 seconds

# Create the main window with TkinterDnD
root = TkinterDnD.Tk()
root.title("Pepe to Pork Meme Converter")
root.geometry("600x600")  # Set predefined window size
root.config(bg='pink')  # Set background color to pink

# Set the window icon
icon_image = ImageTk.PhotoImage(file="programAssets/porklogo.png")
root.iconphoto(False, icon_image)

# Add a header
header = tk.Label(root, text="Pepe to Pork Meme Converter", bg='green', fg='white', font=("Helvetica", 16))
header.pack(fill=tk.X)

# Add a logo
logo_image = Image.open("programAssets/porklogo.png")
logo_image.thumbnail((100, 100))
logo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo, bg='pink')
logo_label.image = logo
logo_label.pack(side="left", anchor="s", padx=10, pady=10)

# Create a placeholder for the image with border-radius and shading
image_frame = tk.Frame(root, bg='#F8C8DC', bd=2, relief="groove")
image_frame.pack(pady=20)

placeholder_label = tk.Label(image_frame, text="Upload photo or Drag and drop photo", bg='#F8C8DC', fg='gray', font=("Helvetica", 14), width=40, height=10)
placeholder_label.pack()

# Create an image label for displaying the processed image
image_label = tk.Label(image_frame, bg='#F8C8DC')
image_label.pack()

# Add a close button ("X") to reset the image slot
close_button = tk.Button(image_frame, text="X", command=reset_image_slot, bg='red', fg='white', relief="flat")
close_button.place_forget()

# Create and style the upload button
upload_button = tk.Button(root, text="Upload Image", command=upload_image, bg='green', fg='white', font=("Helvetica", 14, "bold"), bd=0, highlightthickness=0, activebackground="darkgreen", activeforeground="white", width=20, height=2)
upload_button.pack(pady=10)

# Create a save button
save_button = tk.Button(root, text="Save Image", command=save_image, bg='green', fg='white', font=("Helvetica", 14, "bold"))

# Ensure the save button is packed below the upload button
save_button.pack(pady=10)

# Add mention and ETH address at the bottom
footer_frame = tk.Frame(root, bg='pink')
footer_frame.pack(side="bottom", pady=10)

mention_label = tk.Label(footer_frame, text="X: @yahooWeis", bg='pink', fg='black', font=("Helvetica", 10))
mention_label.pack(side="left")

eth_address_label = tk.Label(footer_frame, text="ETH (Tips): 0x30A6...c9c2a", bg='pink', fg='blue', font=("Helvetica", 10, "underline"), cursor="hand2")
eth_address_label.pack(side="left", padx=10)
eth_address_label.bind("<Button-1>", lambda e: copy_eth_address())

# Enable drag-and-drop functionality on the image frame
image_frame.drop_target_register(DND_FILES)
image_frame.dnd_bind('<<Drop>>', on_drop)

# Run the GUI loop
root.mainloop()
