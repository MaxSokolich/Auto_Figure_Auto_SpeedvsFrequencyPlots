import pandas as pd
import matplotlib.pyplot as plt
import os
import cv2




cam = cv2.VideoCapture("/Users/bizzarohd/Desktop/PhD/Papers/Janus Mazebots and Cellbots Navigating Obstacles/mazedata/raw data/maze_openloop_cellbot.mp4")
savedfolder = "/Users/bizzarohd/Desktop/PhD/Papers/Janus Mazebots and Cellbots Navigating Obstacles/mazedata/figures"



width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

total_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
print(total_frames)

save_interval = total_frames
num_figs = 5
interval = int(total_frames / num_figs)

final_time = 86
interval_display_time = final_time / num_figs

myframes = []
start_time = 0 
for f in range(total_frames):

    _ , frame = cam.read()

    

    cv2.rectangle(frame, (0, 0), (600, 200), (0, 0, 0), -1)  # Add black rectangle
    cv2.rectangle(frame, (1650, 0), (width, 395), (0, 0, 0), -1)  # Add black rectangle
    
    cv2.putText(frame, f'Time: {int(start_time)} s', (1700, 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 4)
    
    scale_bar_length = 150  # Length of the scale bar in pixels
    scale_bar_label = '100um'  # Label for the scale bar
    cv2.putText(frame, scale_bar_label, (frame.shape[1] - 750, 270), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 4)
    cv2.line(frame, (frame.shape[1] - 100, 270), (frame.shape[1] - 100 - scale_bar_length, 270), (255, 255, 255), 20)

    alpha = 0.9  # Contrast control (1.0-3.0)
    beta = 0    # Brightness control (0-100)
    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    
    

    
    if f % interval == 0:
        print(f"save {f}")
        
        cv2.putText(frame, f'Time: {int(start_time)} s', (1700, 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 4)
        myframes.append(frame)
        start_time += interval_display_time
    cv2.imshow("img", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
myframes.append(frame)
cam.release()
cv2.destroyAllWindows()

print(len(myframes))


fig, axes = plt.subplots(2, 3, figsize=(12, 8))
for i in range(2):
    for j in range(3):
        axes[i, j].imshow(cv2.cvtColor(myframes[i * 3 + j], cv2.COLOR_BGR2RGB))
        axes[i, j].axis('off')
        axes[i, j].set_aspect('auto')

plt.subplots_adjust(wspace=0.05, hspace=0.05)
plt.show()