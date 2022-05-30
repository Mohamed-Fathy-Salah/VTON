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

def write_obj(filename, mesh, garment=None, gender=None):
    with open(f"{OUT_PATH}/{filename}.obj", 'w') as output:
        for r in mesh.v: 
            output.write('v %f %f %f\n' % (r[0], r[1], r[2]))
        
        if garment:
            coord_filename = f"{garment}_{gender}"
            vt = np.load(f"{coord_filename}_vt.npy")
            ft = np.load(f"{coord_filename}_ft.npy")
            for i in vt:
              s = f"{i[0]} {i[1]} {i[2]}"
              output.write(s)
            
            for i in ft:
              s = f"{i[0]} {i[1]} {i[2]} {i[3]}"
              output.write(s)

def generate_body(theta=get_specific_pose(0), beta=get_specific_shape('mean'), gender='male', filename='body'):
    smpl = SMPL4Garment(gender=gender)
    body,_ = smpl.run(beta=beta, theta=theta)
    write_obj(filename, body)

def generate_body_garment(theta=get_specific_pose(0), beta=get_specific_shape('mean'), gender='male', garment_class='short-pant', filename='garment', save_body=False, body_filename='body'):
    gamma = get_style('000',garment_class=garment_class,gender=gender)
    tn_runner = get_tn_runner(gender=gender, garment_class=garment_class)
    theta_normalized = normalize_y_rotation(theta)
    with torch.no_grad():
        pred_verts_d = tn_runner.forward(
            thetas=torch.from_numpy(theta_normalized[None, :].astype(np.float32)).cuda(),
            betas=torch.from_numpy(beta[None, :].astype(np.float32)).cuda(),
            gammas=torch.from_numpy(gamma[None, :].astype(np.float32)).cuda(),
        )[0].cpu().numpy()

    smpl = SMPL4Garment(gender=gender)
    body, pred_gar = smpl.run(beta=beta, theta=theta, garment_class=garment_class, garment_d=pred_verts_d)
    pred_gar = remove_interpenetration_fast(pred_gar, body)

    write_obj(filename, pred_gar, garment_class, gender)
    if save_body :
        write_obj(body_filename, body)

if __name__ == '__main__':
    generate_body_garment()
