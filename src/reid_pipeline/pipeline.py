import sys
sys.path.append('..')

from reid_pipeline.reid_data_manager import *
import models.yolox_utils as yolox_utils
from models.configs.PersonalConfigTemplate import PersonalConfig

from fastreid.config import get_cfg
from fastreid.engine import DefaultTrainer, default_argument_parser, default_setup, launch
from fastreid.utils.checkpoint import Checkpointer

from models import BikePerson

from typing import List
import torch

class Pipeline:
    def __init__(self):
        self.yolox_predictor, self.yolo_args = self.build_yolox_model()
        self.reid_model, self.reid_args, self.reid_cfg = self.build_reid_model()

    def __call__(self, image, cam_id): #run the pipeline
        objs = self.spot_object_from_image(image)
        objs = self.get_embedding(objs)
        self.submit_result(objs)
        self.add_extra_info(objs, cam_id)
        return objs

    def build_yolox_model(self):
        # get_yolox_predictor
        yolox_args = yolox_utils.make_parser()
        yolox_args.parse_known_args()
        yolox_args.demo = "image"
        yolox_args.name = "yolox-m"
        yolox_args.exp_file = PersonalConfig().yolox_exp_file
        yolox_args.ckpt = PersonalConfig().yolox_ckpt
        yolox_args.path = PersonalConfig().yolox_path
        yolox_args.conf = 0.25
        yolox_args.nms = 0.45
        yolox_args.tsize = 640
        yolox_args.save_result = True

        yolox_args.experiment_name = None
        yolox_args.camid = 0
        yolox_args.fp16 = False
        yolox_args.legacy = False
        yolox_args.fuse = False 
        yolox_args.trt = False

        if torch.cuda.is_available():
            yolox_args.device = "gpu"
        else:
            yolox_args.device = "cpu"
        exp = yolox_utils.get_exp(yolox_args.exp_file, yolox_args.name)
        return yolox_utils.build_model(exp, yolox_args),yolox_args

    def build_reid_model(self):
        # get_reid_model
        args = default_argument_parser()
        args.parse_known_args()

        args.config_file = "models/configs/bagtricks_R50-ibn market1501.yml"
        args.num_gpus = 0
        args.eval_only = True

        args.num_machines = 1
        args.machine_rank = 0
        port = 2 ** 15 + 2 ** 14 + hash(os.getuid() if sys.platform != "win32" else 1) % 2 ** 14
        args.dist_url = "tcp://127.0.0.1:{}".format(port)
        args.opts = None

        print("Command Line Args:", args)

        cfg = self.reid_setup(args)
        cfg.defrost()
        cfg.MODEL.BACKBONE.PRETRAIN = False
        model = DefaultTrainer.build_model(cfg)
        Checkpointer(model).load(cfg.MODEL.WEIGHTS)  # load trained model
        model.training = False
        
        return model, args, cfg

    def reid_setup(self, args):
        """
        Create configs and perform basic setups.
        """
        cfg = get_cfg()
        cfg.merge_from_file(args.config_file)
        if args.opts is not None:
            cfg.merge_from_list(args.opts)
        cfg.freeze()
        default_setup(cfg, args)
        return cfg


    def spot_object_from_image(self, image) -> List[DetectedObject]:
        return yolox_utils.get_objects_from_image(self.yolox_predictor, image)
        
    def spot_object_from_video(self, video):
        obj_groups = []
        for image in video:
            objects = self.spot_object_from_image(image)
            obj_groups.append(objects)
        return obj_groups
    
    def get_embedding(self, objects: List[DetectedObject]):
        for obj in objects:
            inputs = torch.from_numpy(obj.img).unsqueeze(0).permute(0,3,1,2).float()
            inputs = torch.concat([inputs,inputs], dim=0) #fix batchsize=1 bug
            if self.reid_cfg.MODEL.DEVICE == "cuda":
                inputs = inputs.cuda()
            outputs = self.reid_model(inputs)
            embeddings = outputs["features"]
            obj.embedding = embeddings[0]
            print(obj.embedding)
        return objects

    def submit_result(self, objects: List[DetectedObject]):
        pass

    def add_extra_info(self, objects: List[DetectedObject], cam_id):
        for obj in objects:
            obj.cam_id = cam_id
