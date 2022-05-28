import numpy as np
import torch

from visualization.vis_utils import get_specific_pose
from visualization.vis_utils import get_specific_shape

from models.tailornet_model import get_best_runner as get_tn_runner
from utils.rotation import normalize_y_rotation

from models.smpl4garment import SMPL4Garment
# from dataset.canonical_pose_dataset import get_style, get_shape
from dataset.canonical_pose_dataset import get_style
from utils.interpenetration import remove_interpenetration_fast

# Set output path where inference results will be stored
OUT_PATH = "/content/output"
def generate_garment(theta=get_specific_pose(0), beta=get_specific_shape('mean'), gender='male', garment_class='short-pant', filename='out'):
    gamma = get_style('000',garment_class=garment_class,gender=gender)
    tn_runner = get_tn_runner(gender=gender, garment_class=garment_class)
    theta_normalized = normalize_y_rotation(theta)
    with torch.no_grad():
        pred_verts_d = tn_runner.forward(
            thetas=torch.from_numpy(theta_normalized[None, :].astype(np.float32)),#.cuda(),
            betas=torch.from_numpy(beta[None, :].astype(np.float32)),#.cuda(),
            gammas=torch.from_numpy(gamma[None, :].astype(np.float32)),#.cuda(),
        )[0].cpu().numpy()

    smpl = SMPL4Garment(gender=gender)
    body, pred_gar = smpl.run(beta=beta, theta=theta, garment_class=garment_class, garment_d=pred_verts_d)
    pred_gar = remove_interpenetration_fast(pred_gar, body)

    pred_gar.write_ply("./src/models/ply/"+filename+".ply")
    pred_gar.write_obj("./src/models/obj/"+filename+".obj")

generate_garment()
