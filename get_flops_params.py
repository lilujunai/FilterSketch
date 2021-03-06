import torch
import argparse
import utils.common as utils
from importlib import import_module
from thop import profile

parser = argparse.ArgumentParser(description='Get Model Flops and Params')

parser.add_argument(
    '--input_image_size',
    type=int,
    default=32,
    help='The input_image_size. default:32')

parser.add_argument(
    '--arch',
    type=str,
    default='resnet',
    choices=('resnet','googlenet'),
    help='The architecture to prune. default:resnet')

parser.add_argument(
    '--data_set',
    type=str,
    default='cifar10',
    help='Select dataset to Test. default:cifar10',
)

parser.add_argument(
    '--cfg',
    type=str,
    default='resnet56',
    help='Detail architecuture of model. default:resnet56'
)

parser.add_argument(
    '--sketch_rate',
    type=str,
    default=None,
    help='The proportion of each layer reserved after sketching convolution layer. default:None'
)

args = parser.parse_args()

device = torch.device("cpu")

print('==> Building model..')
sketch_rate = utils.get_sketch_rate(args.sketch_rate)
if args.arch == 'resnet':
    if args.data_set == 'imagenet':
        orimodel = import_module(f'model.{args.arch}_imagenet')\
                    .resnet(args.cfg).to(device)
        model = import_module(f'model.{args.arch}_imagenet')\
                    .resnet(args.cfg, sketch_rate=sketch_rate, start_conv=1).to(device)
    else:
        orimodel = import_module(f'model.{args.arch}').resnet(args.cfg).to(device)
        model = import_module(f'model.{args.arch}')\
                    .resnet(args.cfg, sketch_rate=sketch_rate, start_conv=1).to(device)
elif args.arch == 'googlenet':
    orimodel = import_module(f'model.{args.arch}').googlenet().to(device)
    model = import_module(f'model.{args.arch}').googlenet(sketch_rate).to(device)
else:
    raise('arch not exist!')

input = torch.randn(1, 3, args.input_image_size, args.input_image_size)

print('--------------UnPruned Model--------------')
oriflops, oriparams = profile(orimodel, inputs=(input, ))
print('Params: %.2f'%(oriparams))
print('FLOPS: %.2f'%(oriflops))

print('--------------Pruned Model--------------')
flops, params = profile(model, inputs=(input, ))
print('Params: %.2f'%(params))
print('FLOPS: %.2f'%(flops))

print('--------------Retention Ratio--------------')
print('Params Retention Ratio: %d/%d (%.2f%%)' % (params, oriparams, 100. * params / oriparams))
print('FLOPS Retention Ratio: %d/%d (%.2f%%)' % (flops, oriflops, 100. * flops / oriflops))