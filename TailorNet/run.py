import numpy as np
import torch

from visualization.vis_utils import get_specific_pose
from visualization.vis_utils import get_specific_shape

from models.tailornet_model import get_best_runner as get_tn_runner
from utils.rotation import normalize_y_rotation

from models.smpl4garment import SMPL4Garment
from dataset.canonical_pose_dataset import get_style
from utils.interpenetration import remove_interpenetration_fast


OUT_PATH = "../../output"
TXT_PATH = "../../dataset/txt/"

garment_gammas = {
        't-shirt_male' : {
            'S' : np.array([-2. , 0. , 1.5 , 0. ]),
            'M' : np.array([-1.9 , 0. , 1.5 , 0. ]),
            'L' : np.array([-0.9 , 0. , 1.5 , 0. ]),
            'XL' : np.array([0.4, 0. , 1.5 ,0. ]),
            'XXL' : np.array([0.9, 0. , 1.5 ,0. ]),
            },
        }

def write_obj(mesh, garment=None, gender=None, filename=None):
    if garment:
        coord_filename = f"{TXT_PATH}{garment}_{gender}.txt"
    else:
        coord_filename = f"{TXT_PATH}body_tex_coords.txt"

    with open(filename, 'w') as output:
        for r in mesh.v: 
            output.write('v %f %f %f\n' % (r[0], r[1], r[2]))
        
        with open(coord_filename) as f:
            output.write(f.read())

def generate_body(theta=get_specific_pose(0), beta=get_specific_shape('mean'), gender='female'):
    from smpl_lib.ch_smpl import Smpl
    from utils.smpl_paths import SmplPaths
    from psbody.mesh import Mesh
    smpl_model = SmplPaths(gender=gender).get_hres_smpl_model_data()
    smpl_base = Smpl(smpl_model)
    smpl_base.betas[:] = beta
    smpl_base.pose[:] = theta
    body_m = Mesh(v=smpl_base.r, f=smpl_base.f)
    return body_m

def generate_body_garment(theta=get_specific_pose(0), beta=get_specific_shape('mean'), size='M', gender='female', garment_class='short-pant', save_body=False):
    garment_gender = f"{garment_class}_{gender}"
    gamma = garment_gammas[garment_gender] if garment_gender in garment_gammas else get_style("000", garment_class=garment_class, gender=gender)

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

#top_garment = [garment type, garment size]
def run(theta, beta, gender, top_garment, bottom_garment, save_body):
    body_bottom_gar_combined = None
    body = None

    if bottom_garment:
        garment, size = bottom_garment[:]

        body, bottom_gar = generate_body_garment(theta=theta, beta=beta, gender=gender, garment_class=garment, size=size, save_body=True)
        top_gar = remove_interpenetration_fast(bottom_gar, body)

        body_bottom_gar_combined = bottom_gar.concatenate_mesh(body)

        write_obj(top_gar, garment=garment, gender=gender, filename=f"{OUT_PATH}/{garment}.obj")

    if top_garment:
        garment, size = top_garment[:]

        body, top_gar = generate_body_garment(theta=theta, beta=beta, gender=gender, garment_class=garment, size=size, save_body=True)
        
        if body_bottom_gar_combined:
            top_gar = remove_interpenetration_fast(top_gar, body_bottom_gar_combined)
        else:
            top_gar = remove_interpenetration_fast(top_gar, body)
        write_obj(top_gar, garment=garment, gender=gender, filename=f"{OUT_PATH}/{garment}.obj")

    if save_body :
        write_obj(body, filename=f"{OUT_PATH}/body.obj")

if __name__ == '__main__':
    # run(get_specific_pose(0), get_specific_shape('mean'), 'female', ['000', '000'], ['t-shirt', 'short-pant'], True)

    body = generate_body(gender='male')
    body.write_obj(f"{OUT_PATH}/body.obj")
    # body, gar = generate_body_garment(garment_class='pant', gender='male', save_body=True)
    # body.write_obj(f"{OUT_PATH}/pant.obj")
    # gar.write_obj(f"{OUT_PATH}/pant.obj")
    # write_obj(gar, garment="pant", gender="male", filename=f"{OUT_PATH}/pant.obj")
    # write_obj(body, filename=f"{OUT_PATH}/female.obj")
