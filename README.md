# Describe

Pruning neural network model via filter sketch.

# Pre-train Models

Additionally, we provide several  pre-trained models used in our experiments.

## CIFAR-10

| [ResNet56](https://drive.google.com/open?id=1pt-LgK3kI_4ViXIQWuOP0qmmQa3p2qW5) | [ResNet110](https://drive.google.com/open?id=1Uqg8_J-q2hcsmYTAlRtknCSrkXDqYDMD) |[GoogLeNet](https://drive.google.com/open?id=1YNno621EuTQTVY2cElf8YEue9J4W5BEd) | 

## ImageNet

| [ResNet50](https://download.pytorch.org/models/resnet50-19c8e357.pth) |

# Result Models

we provide all models after sketching in our experiments.

|           | DataSet  |              Sketch Rate              | Flops  | Params | Top-1 Accuracy | Top-5 Accuracy |                           Download                           |
| :-------: | :------: | :-----------------------------------: | :----: | :----: | :------------: | :------------: | :----------------------------------------------------------: |
| ResNet56  | CIFAR-10 |               [0.6]*27                | 73.36M | 0.50M  |     93.19      |       -        | [Link](https://drive.google.com/open?id=1E1I1Cg5Ki6aIzvjKixDSrjuEeV6rnrRF) |
| ResNet110 | CIFAR-10 | [0.9]\*3+[0.4]\*24+[0.3]\*24+[0.9]\*3 | 92.84M | 0.69M  |     93.44      |       -        | [Link](https://drive.google.com/open?id=1h0vh6pprBXDz8FYQK43gQT6PirmGtkVa) |
| GoogLeNet | CIFAR-10 |               [0.25]*9                | 0.59B  | 2.61M  |     94.88      |       -        | [Link](https://drive.google.com/open?id=10uS8hDD4n85fiSGUxBtKljcpRPHeHWX0) |
| ResNet50  | ImageNet |               [0.2]*16                | 0.93B  | 7.18M  |     69.43      |     89.23      | [Link](https://drive.google.com/open?id=1Xo82p37IVKelp4K79tn8TaBdU4bvqhPj) |
| ResNet50  | ImageNet |               [0.4]*16                | 1.51B  | 10.40M |     73.04      |     91.18      | [Link](https://drive.google.com/open?id=1Q-aUjEUh5Q-3Syc5i1n0ZBq85QDUpUtQ) |
| ResNet50  | ImageNet |               [0.6]*16                | 2.23B  | 14.53M |     74.68      |     92.17      | [Link](https://drive.google.com/open?id=1Kk2PRsFAsK_uhs8siWnfvURJlz4zc_j2) |
| ResNet50  | ImageNet |               [0.7]*16                | 2.64B  | 16.95M |     75.22      |     92.50      | [Link](https://drive.google.com/open?id=13Fc-eNP4z3HSQuikcRmHLSvpVJrjXYVu) |

# Running Code

In this code, you can run our models on CIFAR-10 and ImageNet dataset. The code has been tested by Pytorch1.3 and CUDA10.0 on Ubuntu16.04.



## Filter Sketch

You can run the following code to sketch model in cifar10 dataset:

```shell
python sketch_cifar.py 
--data_set cifar10 
--data_path ../data/cifar10/
--sketch_model ./experiment/pretrain/resne56.pt 
--job_dir ./experiment/resnet56/sketch/
--arch resnet 
--cfg resnet56 
--lr 0.01
--lr_decay_step 50 100
--num_epochs 150 
--gpus 0
--sketch_rate [0.6]*27
--weight_norm_method l2
```

You can run the following code to sketch model in imagenet dataset:

```shell
python sketch_imagenet.py 
--data_set imagenet 
--data_path ../data/imagenet/
--sketch_model ./experiment/pretrain/resne50.pth 
--job_dir ./experiment/resnet50/sketch/
--arch resnet 
--cfg resnet50 
--lr 0.1
--lr_decay_step 30 60
--num_epochs 90 
--gpus 0
--sketch_rate [0.6]*16
--weight_norm_method l2
```

## Get FLOPS

You can use the following command to install the thop python package when you need to calculate the flops of the model:

```shell
pip install thop
```

```shell
python get_flop.py 
--data_set cifar10 
--input_image_size 32 
--arch resnet 
--cfg resnet56
--sketch_rate [0.6]*27
```

## Remarks

The number of pruning rates required for different networks is as follows:

|           | CIFAR-10 | ImageNet |
| :-------: | :------: | :------: |
| ResNet56  |    27    |    -     |
| ResNet110 |    54    |    -     |
| GoogLeNet |    9     |    -     |
| ResNet50  |    -     |    16    |

## Other Arguments

```shell
optional arguments:
  -h, --help            show this help message and exit
  --gpus GPUS [GPUS ...]
                        Select gpu_id to use. default:[0]
  --data_set DATA_SET   Select dataset to train. default:cifar10
  --data_path DATA_PATH
                        The dictionary where the input is stored.
                        default:/home/lishaojie/data/cifar10/
  --job_dir JOB_DIR     The directory where the summaries will be stored.
                        default:./experiments
  --arch ARCH           Architecture of model. default:resnet
  --cfg CFG             Detail architecuture of model. default:resnet56
  --num_epochs NUM_EPOCHS
                        The num of epochs to train. default:150
  --train_batch_size TRAIN_BATCH_SIZE
                        Batch size for training. default:128
  --eval_batch_size EVAL_BATCH_SIZE
                        Batch size for validation. default:100
  --momentum MOMENTUM   Momentum for MomentumOptimizer. default:0.9
  --lr LR               Learning rate for train. default:1e-2
  --lr_decay_step LR_DECAY_STEP [LR_DECAY_STEP ...]
                        the iterval of learn rate. default:50, 100
  --weight_decay WEIGHT_DECAY
                        The weight decay of loss. default:5e-4
  --start_conv START_CONV
                        The index of Conv to start sketch, index starts from
                        0. default:1
  --sketch_rate SKETCH_RATE
                        The proportion of each layer reserved after sketching
                        convolution layer sketch. default:None
  --sketch_model SKETCH_MODEL
                        Path to the model wait for sketch. default:None
  --weight_norm_method WEIGHT_NORM_METHOD
                        Select the weight norm method. default:None
                        Optional:l2
```

## Tips

Any problem, free to contact lmbxmu@stu.xmu.edu.cn(mailto:lmbxmu@stu.xmu.edu.cn) or shaojieli@stu.xmu.edu.cn(mailto:shaojieli@stu.xmu.edu.cn)).
