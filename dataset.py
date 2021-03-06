import torch
from torch.utils.data import Dataset
from PIL import Image
import os

class icpr_dataset(Dataset):

    def __init__(self, data_dir, phase = 'train', transform = None):
        self.data_dir = data_dir
        self.phase = phase
        self.transform = transform

        txt_dir = 'txt_' + self.phase
        img_dir = 'image_' + self.phase
        txt_dir = os.path.join(data_dir, txt_dir)
        img_dir = os.path.join(data_dir, img_dir)
        assert os.path.exists(txt_dir) == True
        assert os.path.exists(img_dir) == True

        self.img_dir = img_dir
        self.txt_dir = txt_dir
        self.txt_list = os.listdir(txt_dir)

    def __getitem__(self, idx):
        txt_name = self.txt_list[idx]
        txt_path = os.path.join(self.txt_dir, txt_name)
        assert os.path.isfile(txt_path) == True
        img_path = os.path.join(self.img_dir, txt_name[:-4] + '.jpg')
        assert os.path.isfile(img_path) == True

        with open(txt_path,'rb') as f:
            lines = f.readlines()
        num_txt = len(lines)
        truth = []
        for i in range(num_txt):
            line = lines[i].decode('utf-8').split(',')[:-1]
            truth.append([float(coord) for coord in line ])

        img = Image.open(img_path).convert('RGB')
        if self.transform:
            img = self.transform(img)

        w,h = img.size
        for box in truth:
            for i,coord in enumerate(box):
                if i%2 == 0:
                    if coord < 0:
                        box[i] = 0
                    elif coord > w-1:
                        box[i] = w-1
                else:
                    if coord < 0:
                        box[i] = 0
                    elif coord > h-1:
                        box[i] = h-1

        truth = torch.tensor(truth, dtype=float)
        data={}
        data["image"] = img
        data["truth"] = truth
        return data,img_path,txt_path




