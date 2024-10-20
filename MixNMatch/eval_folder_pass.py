from config import cfg
import os
import time
from PIL import Image
import torch.backends.cudnn as cudnn
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.utils as vutils
from tensorboardX import SummaryWriter
from model_eval import G_NET, Encoder, FeatureExtractor
import torchvision.transforms as transforms
import random
import torch.nn.functional as F
from utils import *
import pdb
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from random import sample
import argparse
from pathlib import Path
import itertools

device = torch.device("cuda:" + cfg.GPU_ID)
gpus = [int(ix) for ix in cfg.GPU_ID.split(',')]




parser = argparse.ArgumentParser()
parser.add_argument("--z",  help="path to z(pose) source image" )  
parser.add_argument("--b",  help="path to b(background) source image" ) 
parser.add_argument("--p",  help="path to p(shape) source image" )
parser.add_argument("--c",  help="path to c(texture) source image" )
parser.add_argument("--out",  help="path to output image" )
parser.add_argument("--mode",  help="either code or feature" )
parser.add_argument("--models",  help="dir to pretrained models" )
args = parser.parse_args()



Z = args.z
B = args.b
P = args.p
C = args.c
OUT = args.out
MODE = args.mode
MODELS = args.models



def load_network(names):
    "load pretrained generator and encoder"


    # prepare G net     
    netG = G_NET().to(device)  
    netG = torch.nn.DataParallel(netG, device_ids=gpus)
    state_dict = torch.load( names[0]  )
    netG.load_state_dict(state_dict)

    # prepare encoder
    encoder = Encoder().to(device)
    encoder = torch.nn.DataParallel(encoder, device_ids=gpus)
    state_dict = torch.load( names[1] )
    encoder.load_state_dict(state_dict)

    extractor = FeatureExtractor(3,16)    
    extractor = torch.nn.DataParallel(extractor , device_ids=gpus)
    extractor.load_state_dict(torch.load(  names[2] ))
    extractor.to(device)
    
    return netG.eval(), encoder.eval(), extractor.eval()




def get_images(fire, size=[128,128]):
    transform = transforms.Compose([ transforms.Resize( (size[0],size[1]) ) ])
    normalize = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))])    
    img = Image.open(   fire   ).convert('RGB') 
    img = transform(img)
    img = normalize(img)   
    return img.unsqueeze(0)




def save_img(img, file, target_size=(1600,2400)):  
    img = img.cpu() 
    
    img = F.interpolate(img, size=target_size, mode='nearest')
    
    vutils.save_image( img, file, scale_each=True, normalize=True )
    real_img_set = vutils.make_grid(img).numpy()
    real_img_set = np.transpose(real_img_set, (1, 2, 0))
    real_img_set = real_img_set * 255
    real_img_set = real_img_set.astype(np.uint8)



def eval_code(folder_z, folder_b, folder_p, folder_c, output_folder):

    names = [ os.path.join(MODELS,'G.pth'), os.path.join(MODELS,'E.pth'), os.path.join(MODELS,'EX.pth')  ] 
    netG, encoder, _ = load_network(names)
    

    # Iterate through images in the folders
    for z_file, b_file, p_file, c_file in zip(Path(folder_z).glob("*"), Path(folder_b).glob("*"), Path(folder_p).glob("*"), Path(folder_c).glob("*")):
        real_img_z = get_images(str(z_file))
        real_img_b = get_images(str(b_file))
        real_img_p = get_images(str(p_file))
        real_img_c = get_images(str(c_file))

        with torch.no_grad():
            fake_z2, _, _, _ = encoder(real_img_z.to(device), 'softmax')
            fake_z1, fake_b, _, _ = encoder(real_img_b.to(device), 'softmax')
            _, _, fake_p, _ = encoder(real_img_p.to(device), 'softmax')
            _, _, _, fake_c = encoder(real_img_c.to(device), 'softmax')

            fake_imgs, _, _, _ = netG(fake_z1, fake_z2, fake_c, fake_p, fake_b, 'code')
            img = fake_imgs[2]
            
        # Save the generated image
        output_path = Path(output_folder) / f"{z_file.stem}_output.jpg"
        save_img(img, str(output_path), target_size=(1600, 2400))





def eval_feature(folder_b, folder_p, folder_c, output_folder):
    names = [os.path.join(MODELS, 'G.pth'), os.path.join(MODELS, 'E.pth'), os.path.join(MODELS, 'EX.pth')]
    netG, encoder, extractor = load_network(names)

    # Iterate through images in the folders
    for b_file, p_file, c_file in zip(Path(folder_b).glob("*"), Path(folder_p).glob("*"), Path(folder_c).glob("*")):
        real_img_b = get_images(str(b_file))
        real_img_p = get_images(str(p_file))
        real_img_c = get_images(str(c_file))

        with torch.no_grad():
            shape_feature = extractor(real_img_p.to(device))
            fake_z1, fake_b, _, _ = encoder(real_img_b.to(device), 'softmax')
            _, _, _, fake_c = encoder(real_img_c.to(device), 'softmax')

            fake_imgs, _, _, _ = netG(fake_z1, None, fake_c, shape_feature, fake_b, 'feature')
            img = fake_imgs[2]

        # Save the generated image
        output_path = Path(output_folder) / f"{b_file.stem}_output.jpg"
        save_img(img, str(output_path), target_size=(1600, 2400))




if __name__ == "__main__":

    if MODE == 'code':
        eval_code(folder_z=args.z, folder_b=args.b, folder_p=args.p, folder_c=args.c, output_folder=args.out)
    elif MODE == 'feature':
        eval_feature(folder_b=args.b, folder_p=args.p, folder_c=args.c, output_folder=args.out)
    else:
        raise ValueError()