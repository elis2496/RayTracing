import argparse 
from utils import make_3Dimage

parser = argparse.ArgumentParser(
    description='Main')
parser.add_argument('--text_file', type=str, default='./data.txt',
                    help='txt file with parameters and coordinats')
parser.add_argument('--img_filename', default='./result.png', type=str,
                    help='Name of processed image')
parser.add_argument('--img_width', default=200, type=int,
                    help='Width of image')
parser.add_argument('--img_height', default=200, type=int,
                    help='Height of image')

def main(args):
    make_3Dimage(args.text_file,
                 args.img_width,
                 args.img_width,
                 args.img_filename)
    
if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
