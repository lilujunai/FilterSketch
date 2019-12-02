'''ResNet in PyTorch.

For Pre-activation ResNet, see 'preact_resnet.py'.

Reference:
[1] Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun
    Deep Residual Learning for Image Recognition. arXiv:1512.03385
'''
import torch
import torch.nn as nn
import torch.nn.functional as F


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1, sketch_rate=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, int(planes * sketch_rate), kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(int(planes * sketch_rate))
        self.conv2 = nn.Conv2d(int(planes * sketch_rate), planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

        self.downsample = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.downsample = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, in_planes, planes, stride=1, sketch_rate=1):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, int(planes * sketch_rate), kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(int(planes * sketch_rate), int(planes * sketch_rate), kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(int(planes * sketch_rate))
        self.conv3 = nn.Conv2d(int(planes * sketch_rate), self.expansion*planes, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(self.expansion*planes)

        self.downsample = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.downsample = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class ResNet(nn.Module):
    def __init__(self, block, num_blocks, num_classes=10, sketch_rate=1):
        super(ResNet, self).__init__()
        self.in_planes = 64
        self.sketch_rate = sketch_rate

        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        self.avgpool = nn.Sequential(nn.AvgPool2d(7))
        self.fc = nn.Linear(512*block.expansion, num_classes)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride, sketch_rate=self.sketch_rate))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.maxpool(out)
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.avgpool(out)
        out = out.view(out.size(0), -1)
        out = self.linear(out)
        return out

def resnet(cfg, sketch_rate=1, num_classes=1000):
    if cfg == 'resnet18':
        return ResNet(BasicBlock, [2, 2, 2, 2], sketch_rate=sketch_rate, num_classes=num_classes)
    elif cfg == 'resnet34':
        return ResNet(BasicBlock, [3, 4, 6, 3], sketch_rate=sketch_rate, num_classes=num_classes)
    elif cfg == 'resnet50':
        return ResNet(Bottleneck, [3, 4, 6, 3], sketch_rate=sketch_rate, num_classes=num_classes)
    elif cfg == 'resnet101':
        return ResNet(Bottleneck, [3, 4, 23, 3], sketch_rate=sketch_rate, num_classes=num_classes)
    elif cfg == 'resnet152':
        return ResNet(Bottleneck, [3, 8, 36, 3], sketch_rate=sketch_rate, num_classes=num_classes)

def ResNet18():
    return ResNet(BasicBlock, [2,2,2,2])

def ResNet34():
    return ResNet(BasicBlock, [3,4,6,3])

def ResNet50():
    return ResNet(Bottleneck, [3,4,6,3])

def ResNet101():
    return ResNet(Bottleneck, [3,4,23,3])

def ResNet152():
    return ResNet(Bottleneck, [3,8,36,3])


def test():
    net = ResNet101()

    # model_state_dict = net.state_dict()
    #
    # state = {
    #     'state_dict': model_state_dict
    # }
    # torch.save(state, open('./resnet101.pth', 'wb'))
    # y = net(torch.randn(1,3,32,32))
    # print(y.size())
    # print(net)
    #
    # for name, module in net.named_modules():
    #     if isinstance(module, nn.Conv2d):
    #         print(name, module.weight.size())

# test()