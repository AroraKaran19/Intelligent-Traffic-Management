from roboflow import Roboflow
from tkinter import *
import cv2
import random

def VehicleDetection():
    root = Tk()
    root.title("JamBuster | Vehicle Detection")
    root.geometry("1400x922")
    root.resizable(False, False)
    canvas = Canvas(root, width=1400, height=922)
    canvas.pack()
    img= PhotoImage(file='mod_int.png', master=root)
    canvas.create_image(0, 0, anchor=NW, image=img)
    label = Label(canvas, text="Vehicle Detection", font=("Arial", 30, "bold"))
    canvas.create_window(200, 50, window=label)

    start_button = Button(canvas, text="Start", bg="white", font=("Arial", 20, "bold"), padx=30, pady=20, command=lambda: roboflow(root, canvas))
    canvas.create_window(200, 200, window=start_button)

    root.mainloop()

def Gui():
    BG_COLOR = "#7F27FF"
    root = Tk()
    root.title("JamBuster | Vehicle Detection")
    root.geometry("600x600")
    root.resizable(False, False)
    canvas = Canvas(root, width=600, height=600, bg=BG_COLOR)
    canvas.pack()
    label = Label(canvas, text="Vehicle Detection", bg=BG_COLOR, font=("Arial", 30, "bold"))
    canvas.create_window(300, 50, window=label)

    run_button = Button(canvas, text="Run", bg="white", font=("Arial", 20, "bold"), padx=30, pady=20, command=lambda: (root.destroy(), VehicleDetection() ))
    canvas.create_window(300, 200, window=run_button)

    exit_button = Button(canvas, text="Exit", bg="white", font=("Arial", 20, "bold"), command=root.quit, padx=30, pady=20)
    canvas.create_window(300, 400, window=exit_button)

    root.mainloop()

def place_images(root, canvas):
    import os
    images = os.listdir("res")
    for i, image in enumerate(images):
        image_path = f"res/predictions_{i}.jpg"
        img = PhotoImage(file=image_path, master=root)
        canvas.create_image(600, 200 + i * 200, anchor=NW, image=img)

def predict_images():
    import os
    rf = Roboflow(api_key="tLcBukmQSSonFOkM949S")
    project = rf.workspace().project("traffic-management-1aa8k")
    model = project.version(5).model
    images = os.listdir("res")
    for i, image in enumerate(images):
        image_path = f"res/frame_{i}.jpg"
        model.predict(image_path, confidence=10, overlap=10).save(f"res/predictions_{i}.jpg")

def roboflow(root, canvas):
    video_capture = cv2.VideoCapture("traffic.mp4")
    
    # Get the total number of frames in the video
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Generate random timestamps
    random_timestamps = [random.randint(0, total_frames) for _ in range(4)]
    
    # Extract frames at random timestamps
    i = 0
    for timestamp in random_timestamps:
        # Set the frame position to the random timestamp
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, timestamp)
        
        # Read the frame
        ret, frame = video_capture.read()
        
        if ret:
            # Save the frame as an image
            output_file = f"res/frame_{i}.jpg"
            cv2.imwrite(output_file, frame)
            i += 1
    # Release the video capture object
    video_capture.release()
    predict_images()
    place_images(root, canvas)


if __name__ == "__main__":
    Gui()
