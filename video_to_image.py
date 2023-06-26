import os
import cv2

#convert mp4 movie into jpg image
class VideotoImage:
    def __init__(self, image_width, image_height):
        self.image_width = image_width
        self.image_height = image_height
    
    def save_frames(self, video_path, dir_path, basename):
        videos = os.listdir(video_path)
        print(videos)
        digit = 0
        for video in videos:
            cap = cv2.VideoCapture(video_path + video)
            print(video_path+video)
            print(cap.isOpened())
            if not cap.isOpened():
                return
            os.makedirs(dir_path, exist_ok=True)
            base_path = os.path.join(dir_path, basename)
            n = 0
            while True:
                ret, frame = cap.read()
                if ret:
                    if n%5 == 0:
                        cv2.imwrite('{}_{}.{}'.format(base_path, str(digit), 'jpg'), frame)
                        n+=1
                        digit += 1
                    else:
                        n+=1
                else:
                    break

videoToImage = VideotoImage(640, 480)

videoToImage.save_frames('data/hako/', 'data/temp/result', 'hako')