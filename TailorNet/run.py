import numpy as np
import torch

from visualization.vis_utils import get_specific_pose
from visualization.vis_utils import get_specific_shape

from models.tailornet_model import get_best_runner as get_tn_runner
from utils.rotation import normalize_y_rotation

from models.smpl4garment import SMPL4Garment
from dataset.canonical_pose_dataset import get_style
from utils.interpenetration import remove_interpenetration_fast

OUT_PATH = "/content/output"

def write_obj(mesh, garment=None, gender=None, filename=None):
    if garment:
        coord_filename = f"{garment}_{gender}.txt"
    else:
        coord_filename = "body_tex_coords.txt"

    with open(filename, 'w') as output:
        for r in mesh.v: 
            output.write('v %f %f %f\n' % (r[0], r[1], r[2]))
        
        with open(coord_filename) as f:
            output.write(f.read())

def generate_body(theta=get_specific_pose(0), beta=get_specific_shape('mean'), gender='female', filename='body'):
    smpl = SMPL4Garment(gender=gender)
    body,_ = smpl.run(beta=beta, theta=theta)
    return body

def generate_body_garment(theta=get_specific_pose(0), beta=get_specific_shape('mean'), size='000', gender='female', garment_class='short-pant', save_body=False):
    gamma = get_style(size, garment_class=garment_class, gender=gender)

    tn_runner = get_tn_runner(gender=gender, garment_class=garment_class)
    theta_normalized = normalize_y_rotation(theta)

    with torch.no_grad():
        pred_verts_d = tn_runner.forward(
            thetas=torch.from_numpy(theta_normalized[None, :].astype(np.float32)), #.cuda(),
            betas=torch.from_numpy(beta[None, :].astype(np.float32)), #.cuda(),
            gammas=torch.from_numpy(gamma[None, :].astype(np.float32)), #.cuda(),
        )[0].cpu().numpy()

    smpl = SMPL4Garment(gender=gender)
    body, pred_gar = smpl.run(beta=beta, theta=theta, garment_class=garment_class, garment_d=pred_verts_d, generate_body=save_body)

    return body, pred_gar

# size [top, bottom]
# garment_class [top, bottom]
def run(theta, beta, gender, size, garment, save_body):
    body, top_gar = generate_body_garment(theta=theta, beta=beta, gender=gender, garment_class=garment[0], size=size[0], save_body=True)
    _, bottom_gar = generate_body_garment(theta=theta, beta=beta, gender=gender, garment_class=garment[1], size=size[1], save_body=False)

    top_gar = remove_interpenetration_fast(top_gar, body)
    bottom_gar = remove_interpenetration_fast(bottom_gar, body)

    
    write_obj(top_gar, garment=garment[0], gender=gender, filename=f"{OUT_PATH}/{garment[0]}.obj")
    write_obj(bottom_gar, garment=garment[1], gender=gender, filename=f"{OUT_PATH}/{garment[1]}.obj")

    if save_body :
        write_obj(body, filename=f"{OUT_PATH}/body.obj")

if __name__ == '__main__':
    run(get_specific_pose(0), get_specific_shape('mean'), 'female', ['000', '000'], ['t-shirt', 'short-pant'], True)

    # body, gar = generate_body_garment(save_body=True)
    # write_obj(gar, garment="short-pant", gender="female", filename=f"{OUT_PATH}/short-pant.obj")
    # write_obj(body, filename=f"{OUT_PATH}/female.obj")
