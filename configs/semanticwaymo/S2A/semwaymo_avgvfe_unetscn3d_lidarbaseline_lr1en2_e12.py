import itertools
import logging
from typing import Sequence

from addict.addict import Dict


num_class=23
ignore_class=0



# training and testing settings
# voxelization setup as same as det
# z range should be [-4, 2]
# point_cloud_range=[-75.2, -75.2, -4, 75.2, 75.2, 2]
# we find that z_range of [-2, 4] can achive better results for waymo datatset
point_cloud_range=[-75.2, -75.2, -2, 75.2, 75.2, 4] 
voxel_size=[0.1, 0.1, 0.15]



# model settings
model = dict(
    type="SegNet",
    pretrained=None,
    reader=dict(
        type="ImprovedMeanVoxelFeatureExtractor",
        num_input_features=5, 
    ),
    backbone=dict(
        type="UNetSCN3D", 
        num_input_features=5+8, # for SemanticNuScene
        ds_factor=8, 
        us_factor=8,
        point_cloud_range=point_cloud_range, 
        voxel_size=voxel_size, 
        model_cfg=dict(
            SCALING_RATIO=2, # channel scaling
        ),
    ),
    point_head=dict(
        type="PointSegBatchlossHead",
        class_agnostic=False, 
        num_class=num_class,
        model_cfg=dict(
            CONV_IN_DIM=32,  
            CONV_CLS_FC=[64],
            CONV_ALIGN_DIM=64,
            OUT_CLS_FC=[64, 64],
            IGNORED_LABEL=0,
        )
    )
)

train_cfg = dict()
test_cfg = dict()



# dataset settings
dataset_type = "SemanticWaymoDataset"
data_root = "data/SemanticWaymo"
nsweeps = 1

train_preprocessor = dict(
    mode="train",
    shuffle_points=True,
    npoints=400000, 
    global_rot_noise=[-0.78539816, 0.78539816],
    global_scale_noise=[0.95, 1.05], 
    global_translate_std=0.5,
)
val_preprocessor = dict(
    mode="val",
    shuffle_points=False,
)
test_preprocessor = dict(
    mode="val",
    shuffle_points=False,
)




voxel_generator = dict(
    range=point_cloud_range,
    voxel_size=voxel_size,
    max_points_in_voxel=5,
    max_voxel_num=[300000, 300000], 
)

train_pipeline = [
    dict(type="LoadPointCloudFromFile", dataset=dataset_type),
    dict(type="LoadPointCloudAnnotations", with_bbox=False),
    dict(type="SegPreprocess", cfg=train_preprocessor),
    dict(type="SegVoxelization", cfg=voxel_generator),
    dict(type="SegAssignLabel", cfg=dict(voxel_label_enc="compact_value")),
    dict(type="Reformat"),
]
val_pipeline = [
    dict(type="LoadPointCloudFromFile", dataset=dataset_type),
    dict(type="SegPreprocess", cfg=val_preprocessor),
    dict(type="SegVoxelization", cfg=voxel_generator),
    dict(type="Reformat"),
]
test_pipeline = [ ] 


train_anno = "data/SemanticWaymo/infos_train_01sweeps_segdet_filter_zero_gt.pkl"
val_anno = "data/SemanticWaymo/infos_val_01sweeps_segdet_filter_zero_gt.pkl"
test_anno = None



data = dict(
    samples_per_gpu=4, 
    workers_per_gpu=8, 
    train=dict(
        type=dataset_type,
        root_path=data_root,
        info_path=train_anno,
        ann_file=train_anno,
        nsweeps=nsweeps,
        load_interval=1, 
        pipeline=train_pipeline,
    ),
    val=dict(
        type=dataset_type,
        root_path=data_root,
        info_path=val_anno,
        test_mode=True,
        ann_file=val_anno,
        nsweeps=nsweeps,
        load_interval=1,
        pipeline=val_pipeline,
    ),
    test=dict(
        type=dataset_type,
        root_path=data_root,
        info_path=test_anno,
        test_mode=True,
        ann_file=test_anno,
        nsweeps=nsweeps,
        pipeline=test_pipeline,
    ),
)



optimizer_config = dict(grad_clip=dict(max_norm=35, norm_type=2))
# optimizer
optimizer = dict(
    type="adam", amsgrad=0.0, wd=0.01, fixed_wd=True, moving_average=False,
)
lr_config = dict(
    type="one_cycle", lr_max=0.01, moms=[0.95, 0.85], div_factor=10.0, pct_start=0.4,
)

checkpoint_config = dict(interval=1)
# yapf:disable
log_config = dict(
    interval=5, 
    hooks=[
        dict(type="TextLoggerHook"),
        # dict(type='TensorboardLoggerHook')
    ],
)
# yapf:enable
# runtime settings
total_epochs = 12

device_ids = range(8)

dist_params = dict(backend="nccl", init_method="env://")
log_level = "INFO"
work_dir = './work_dirs/{}/'.format(__file__[__file__.rfind('/') + 1:-3])
load_from = None
resume_from = None 
workflow = [('train', 1)]

sync_bn_type = "torch"