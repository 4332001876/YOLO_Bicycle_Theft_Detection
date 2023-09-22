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
        exp = yolox_utils.get_exp(args.exp_file, args.name)
        
    def spot_object_from_video(self, video):
        pass
    def get_embedding(self, objects: List[BikePersonObject]) -> List[torch.Tensor]:
        pass
    def submit_result(self, embeddings: List[torch.Tensor]):
        pass