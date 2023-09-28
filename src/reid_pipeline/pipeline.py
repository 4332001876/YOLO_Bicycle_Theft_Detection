import sys
sys.path.append('..')

from reid_pipeline.reid_data_manager import *
import models.yolox_utils as yolox_utils

from typing import List
import torch

class Pipeline:
    def __init__(self):
        pass
    def __call__(self, *args, **kwargs):
        pass
    def spot_object_from_image(self, image) -> List[BikePersonObject]:
        args = yolox_utils.make_parser().parse_args()
        args.demo = "image"
        args.name = "yolox-m"
        args.exp_file = "/home/aistudio/Great_Project/YOLO_Bicycle_Theft_Detection/src/models/configs/yolox_exps/default/yolox_m.py"
        args.ckpt = "/home/aistudio/Great_Project/Testing_Ground/yolox/yolox_m.pth"
        args.path = "/home/aistudio/data/data237899/cam_1_2/Bike/Person_0000"
        args.conf = 0.25
        args.nms = 0.45
        args.tsize = 640
        args.save_result = True
        args.device = "gpu"
        exp = yolox_utils.get_exp(args.exp_file, args.name)
        yolox_utils.main(exp, args)
        
    def spot_object_from_video(self, video):
        pass
    def get_embedding(self, objects: List[BikePersonObject]) -> List[torch.Tensor]:
        pass
    def submit_result(self, embeddings: List[torch.Tensor]):
        pass