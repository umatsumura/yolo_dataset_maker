import os
import shutil
import numpy as np
import xml.etree.ElementTree as ET

class CvatToYoloObb:
    def __init__(self):
        self.images_train = "data/dataset/images/train/"
        self.labels_train = "data/dataset/labelTxt/train/"
        self.images_valid = "data/dataset/images/valid/"
        self.labels_valid = "data/dataset/labelTxt/valid/"
        os.makedirs(self.images_train, exist_ok=True)
        os.makedirs(self.labels_train, exist_ok=True)
        os.makedirs(self.images_valid, exist_ok=True)
        os.makedirs(self.labels_valid, exist_ok=True)

    def calc_rect(self, p1, p3, ang_rad, label):
        # read p1 and p3 and rotation angle
            # p1 -- p2
            # |     |
            # p4 -- p3
        rvec = lambda t : np.array([[np.cos(t), -np.sin(t)],
                                    [np.sin(t), np.cos(t)]])
        center = (p1 + p3)/2
        p1_center = p1 - center
        p3_center = p3 - center
        p1_leveled = np.dot(rvec(-ang_rad), p1_center)
        p3_leveled = np.dot(rvec(-ang_rad), p3_center)
        p2_leveled = np.array([p3_leveled[0], p1_leveled[1]])
        p4_leveled = np.array([p1_leveled[0], p3_leveled[1]])
        #rotate p2_leveled and p4_leveled
        p2 = np.dot(rvec(ang_rad), p2_leveled) + center
        p4 = np.dot(rvec(ang_rad), p4_leveled) + center
        return [str(p1[0]),str(p1[1]), str(p2[0]),str(p2[1]), str(p3[0]),str(p3[1]), str(p4[0]),str(p4[1]), label, "0"]

    def cvat_to_obb(self,anno_path, img_path, valid_rate):
        #read annotation xml
        anno_xml = ET.parse(anno_path)
        anno_root = anno_xml.getroot()
        annos = anno_root.findall('image')
        i = 0
        for i, anno in enumerate(annos):
            box = anno.find('box')
            p1 = np.array([float(box.get('xtl')), float(box.get('ytl'))])
            p3 = np.array([float(box.get('xbr')), float(box.get('ybr'))])
            rotation = float(box.get('rotation')) if not box.get('rotation') == None else 0
            rotation = rotation if rotation < 180 else 360 - rotation
            # calculate 4 corners of rectangle
            ang_rad = np.deg2rad(rotation)
            id = anno.attrib["id"]
            label = box.attrib["label"]
            rect = self.calc_rect(p1, p3, ang_rad, label)
            label_file = label + "_" + id + ".txt"
            with open(label_file, 'w') as f:
                for data in rect:
                    f.write("%s " % data) 
            original_imgage = os.path.join(img_path, anno.attrib["name"])
            image_file = label + "_" + id + ".jpg"
            if i < int(len(annos) * (1 - valid_rate)):
                image_path = os.path.join(self.images_train, image_file)
                shutil.copy(original_imgage, image_path)
                label_path_train = shutil.move(label_file, self.labels_train)
                print(label_path_train)
            else:
                image_path = os.path.join(self.images_valid, image_file)
                shutil.copy(original_imgage, image_path)
                label_path_valid = shutil.move(label_file, self.labels_valid)
                print(label_path_valid)

if __name__ == '__main__':
    cvat2YoloObb = CvatToYoloObb()
    cvat2YoloObb.cvat_to_obb("annotations.xml", "images/", 0.15)






        



