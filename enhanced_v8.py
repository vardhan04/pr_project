#Basic imports.
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from getpass import getpass
import roboflow
import yaml
import subprocess
from roboflow import Roboflow



# Install packages, in cmd.
# pip install ultralytics==8.1.24
# pip install flask==3.0.2
# pip install tensorflow


# If you've already run the v8.py training yolo model, the dataset is downloaded, if not the below lines of code will download it.
folder_name = "ExDark-12"
# Get the current directory of the Python file
current_directory = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the folder
folder_path = os.path.join(current_directory, folder_name)

# Check if the folder exists, if not it downloads the dataset.
if not os.path.exists(folder_path):
    # Set Roboflow API key, also this is my private key, I am just hard coding it to make implementation easy.
    ROBOFLOW_API_KEY = 'CabVUHoCeNaNe2M7fApx'

    # Initialize Roboflow, basically logging in without implcitly doing it.
    rf = Roboflow(api_key=ROBOFLOW_API_KEY)

    # Downloading the dataset, providing the versions, project dataset name.
    project = rf.workspace("project-h68de").project("exdark-kd37x")
    version = project.version(12)
    dataset = version.download("yolov8")


# # Only if you face a datset path error, please un-comment below, I have debugged the error and below is the resolution code.
# # Define the hard-coded username, give your actual username
# username = "YOUR_ACTUAL_USERNAME"

# # Define the path to the settings.yaml file
# settings_file_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Ultralytics\\settings.yaml"

# # Loading the YAML file
# with open(settings_file_path, 'r') as file:
#     lines = file.readlines()

# with open(settings_file_path, 'w') as file:
#     for line in lines:
#         if line.startswith('datasets_dir:'):
#             file.write(f'datasets_dir: C:\\Users\\{username}\\Downloads\\v8YOLO_code\n')
#         else:
#             file.write(line)








## Running "custom_enhancement.py" -> What it does it takes the images from each of the (train,test,valid) folders
## and it enhances the low-light images using custom CLAHE techniques and creates 3 new enhanced folders to train, test, validate.




process = subprocess.Popen(["python", "custom_enhancement.py"])
print("Enhancement of dataset has started...")
# Wait for the the script to finish
process.wait()
# Continuing nwith the execution of the first Python script after the script has finished
print("Enhancement script execution completed. Continuing with training.")



# Modifying the default data.yaml file according to our hierarchy.
# Loading the YAML file.
with open('ExDark-12/data.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Modify the paths, as per our directory structure.
data['test'] = 'enhanced_test/images'
data['train'] = 'enhanced_train/images'
data['val'] = 'enhanced_valid/images'

# Save the changes back to the YAML file.
with open('ExDark-12/data.yaml', 'w') as file:
    yaml.safe_dump(data, file, default_flow_style=False)




# Training YOLOv8 model, I put 25 epochs, as it consumes a lot of time. Also scaled images to a dimension supported by dataset images. Having a T4 GPU on colab, we can have freedom to increase the epochs to 50 or more, maybe.
os.system('yolo task=detect mode=train model=yolov8s.yaml data=ExDark-12/data.yaml epochs=25 imgsz=512 batch=16 workers=8')

# Validating, based on our custom trained v8 model.
os.system('yolo task=detect mode=val model=runs/detect/train/weights/best.pt data=ExDark-12/data.yaml')

# Predict mode using v8 model, for all the test images.
os.system('yolo task=detect mode=predict model=runs/detect/train/weights/best.pt conf=0.25 source=ExDark-12/enhanced_test/images')



# Displaying result images.
Image.open('runs/detect/train/confusion_matrix.png').show()
Image.open('runs/detect/train/results.png').show()
Image.open('runs/detect/train/val_batch1_pred.jpg').show()

# Loading results data from v8 train.
data_path = 'runs/detect/train/results.csv'
data = pd.read_csv(data_path)


# Strip whitespace from column names
data.columns = data.columns.str.strip()


# Setting up the plot to display.
plt.figure(figsize=(12, 8))

# Plotting box losses
plt.subplot(3, 1, 1)  # 3 rows, 1 column, first subplot
plt.plot(data['epoch'], data['train/box_loss'], label='Train Box Loss', marker='o')
plt.plot(data['epoch'], data['val/box_loss'], label='Validation Box Loss', marker='o')
plt.title('Box Loss Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Plotting class losses
plt.subplot(3, 1, 2)  # 3 rows, 1 column, second subplot
plt.plot(data['epoch'], data['train/cls_loss'], label='Train Class Loss', marker='o')
plt.plot(data['epoch'], data['val/cls_loss'], label='Validation Class Loss', marker='o')
plt.title('Class Loss Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Plotting DFL losses
plt.subplot(3, 1, 3)  # 3 rows, 1 column, third subplot
plt.plot(data['epoch'], data['train/dfl_loss'], label='Train DFL Loss', marker='o')
plt.plot(data['epoch'], data['val/dfl_loss'], label='Validation DFL Loss', marker='o')
plt.title('DFL Loss Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()

# Path to the directory containing YOLO training logs
logdir = os.path.join('runs', 'detect')

# Ensure the log directory exists
if not os.path.exists(logdir):
    raise FileNotFoundError(f"Log directory '{logdir}' does not exist")

# Start TensorBoard
print(f"Starting TensorBoard with logdir: {logdir}")
subprocess.run(['tensorboard', '--logdir', logdir])