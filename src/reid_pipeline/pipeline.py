from .reid_data_manager import *

from typing import List
import torch

class Pipeline:
    def __init__(self):
        pass
    def __call__(self, *args, **kwargs):
        pass
    def spot_object_from_image(self, image) -> List[BikePersonObject]:
        pass
    def spot_object_from_video(self, video):
        pass
    def get_embedding(self, objects: List[BikePersonObject]) -> List[torch.Tensor]:
        pass
    def submit_result(self, embeddings: List[torch.Tensor]):
        pass