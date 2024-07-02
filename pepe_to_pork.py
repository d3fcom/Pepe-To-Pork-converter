import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os
import uuid
import cv2
from tkinterdnd2 import DND_FILES, TkinterDnD

# Keep a reference to the modified PIL image
modified_image_pil = None
uploaded_video_path = None

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
save_button.pack(pady=10)

# Create a button to open video converter
video_button = tk.Button(root, text="Video", command=lambda: open_video_window(), bg='green', fg='white', font=("Helvetica", 14, "bold"))
video_button.pack(pady=10)

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

def open_video_window():
    global uploaded_video_path

    video_window = tk.Toplevel(root)
    video_window.title("Pepe to Pork Video Converter")
    video_window.geometry("600x400")
    video_window.config(bg='pink')

    header = tk.Label(video_window, text="Pepe to Pork Video Converter", bg='green', fg='white', font=("Helvetica", 16))
    header.pack(fill=tk.X)

    video_frame = tk.Frame(video_window, bg='#F8C8DC', bd=2, relief="groove")
    video_frame.pack(pady=20)

    placeholder_label_video = tk.Label(video_frame, text="Upload video or Drag and drop video", bg='#F8C8DC', fg='gray', font=("Helvetica", 14), width=40, height=10)
    placeholder_label_video.pack()

    video_label = tk.Label(video_frame, bg='#F8C8DC')
    video_label.pack()

    def upload_video(file_path=None):
        global uploaded_video_path
        if not file_path:
            file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
            if not file_path:
                return
        try:
            uploaded_video_path = file_path
            thumbnail_path = generate_video_thumbnail(file_path)
            display_video_thumbnail(thumbnail_path)
            convert_button.config(state=tk.NORMAL)
            save_button_video.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def generate_video_thumbnail(file_path):
        cap = cv2.VideoCapture(file_path)
        ret, frame = cap.read()
        cap.release()
        if ret:
            thumbnail_path = os.path.join("Results", f"{uuid.uuid4().hex[:8]}.png")
            thumbnail_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            thumbnail_image.save(thumbnail_path)
            return thumbnail_path
        else:
            raise RuntimeError("Failed to generate video thumbnail")

    def display_video_thumbnail(thumbnail_path):
        thumbnail_image = Image.open(thumbnail_path)
        thumbnail_image.thumbnail((400, 400))
        thumbnail_img = ImageTk.PhotoImage(thumbnail_image)
        video_label.config(image=thumbnail_img)
        video_label.image = thumbnail_img
        placeholder_label_video.pack_forget()

    def convert_and_save_video():
        try:
            output_path = convert_video(uploaded_video_path)
            show_notification(f"Video saved as {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def on_drop_video(event):
        file_path = event.data.strip('{}')
        if os.path.isfile(file_path):
            upload_video(file_path)

    def convert_video(file_path):
        cap = cv2.VideoCapture(file_path)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_dir = os.path.join("Results", "video")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, f"{uuid.uuid4().hex[:8]}.avi")

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        if not out.isOpened():
            raise RuntimeError("Failed to open video writer")

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = change_color_video(frame)
            out.write(frame)
            frame_count += 1

        cap.release()
        out.release()

        if frame_count == 0:
            raise RuntimeError("No frames were processed")
        return output_path

    def change_color_video(frame):
        # Convert the frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        data = np.array(frame)
        
        # Define the green color range (adjusted values)
        lower_green = np.array([0, 100, 0])
        upper_green = np.array([200, 255, 200])
        
        # Create a mask to identify green pixels
        mask = np.all(data >= lower_green, axis=-1) & np.all(data <= upper_green, axis=-1)
        
        # Replace green pixels with pink
        data[mask] = [255, 105, 180]
        
        # Convert back to frame
        new_frame = Image.fromarray(data)
        new_frame = np.array(new_frame)
        
        return cv2.cvtColor(new_frame, cv2.COLOR_RGB2BGR)

    video_upload_button = tk.Button(video_window, text="Upload Video", command=upload_video, bg='green', fg='white', font=("Helvetica", 14, "bold"), bd=0, highlightthickness=0, activebackground="darkgreen", activeforeground="white", width=20, height=2)
    video_upload_button.pack(pady=10)

    convert_button = tk.Button(video_window, text="Convert to Pork", command=convert_and_save_video, state=tk.DISABLED, bg='green', fg='white', font=("Helvetica", 14, "bold"), bd=0, highlightthickness=0, activebackground="darkgreen", activeforeground="white", width=20, height=2)
    convert_button.pack(pady=10)

    save_button_video = tk.Button(video_window, text="Save Video", command=convert_and_save_video, state=tk.DISABLED, bg='green', fg='white', font=("Helvetica", 14, "bold"), bd=0, highlightthickness=0, activebackground="darkgreen", activeforeground="white", width=20, height=2)
    save_button_video.pack(pady=10)

    video_frame.drop_target_register(DND_FILES)
    video_frame.dnd_bind('<<Drop>>', on_drop_video)

# Run the GUI loop
root.mainloop()
