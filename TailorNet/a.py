import os
import numpy as np
import global_var 

def get_style(style_idx, gender, garment_class):
    gammas = np.load(os.path.join(
        global_var.DATA_DIR,
        '{}_{}/style/gamma_{}.npy'.format(garment_class, gender, style_idx)
    )).astype(np.float32)
    return gammas

garment_gammas = {
        't-shirt_male' : {
            'S' : np.array([-2. , 0. , 1.5 , 0. ]),
            'M' : np.array([-1.9 , 0. , 1.5 , 0. ]),
            'L' : np.array([-0.9 , 0. , 1.5 , 0. ]),
            'XL' : np.array([0.4, 0. , 1.5 ,0. ]),
            'XXL' : np.array([0.9, 0. , 1.5 ,0. ]),
            },
        }

print(get_style('000', 'male', 'pant').shape)
garment_gender = "t-shirt_male"
gamma = garment_gammas[garment_gender]['S'] if garment_gender in garment_gammas else get_style("000", garment_class='pant', gender='male')
print(gamma)
