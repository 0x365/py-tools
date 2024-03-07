import numpy as np
import math
from scipy.optimize import minimize

def get_cov(m1, m2):
    no = m1.shape[0]*m1.shape[1]
    m1_avg = np.sum(m1)/no
    m2_avg = np.sum(m2)/no
    return np.sum((m1-m1_avg)*(m2-m2_avg))/(no-1)

# Get single covaraince
def single_cov(mask_1, mask_2):
    mask_1[mask_1 == None] = 0
    mask_1[mask_1 < 0] = 0
    mask_2[mask_2 == None] = 0
    mask_2[mask_2 < 0] = 0
    cov = get_cov(mask_1, mask_2)/(np.std(mask_1)*np.std(mask_2))
    return (cov)


def all_cov(scaler, mask, mask_neg):
    scaler = np.append(scaler, 1-sum(scaler))
    mask_i_li = []
    for i in range(len(mask)):
        if len(mask_neg) == len(mask[i]):
            mask_i_temp = (mask[i] - mask_neg) * scaler[i]
        else:
            mask_i_temp = mask[i] * scaler[i]
        mask_i_temp[mask_i_temp == None] = 0
        mask_i_temp[mask_i_temp < 0] = 0
        mask_i_li.append(mask_i_temp)
        try:
            mask_comb += mask_i_temp
        except:
            mask_comb = mask_i_temp

    p_cor = 0
    for mask_i in mask_i_li:
        p_cor += get_cov(mask_comb, mask_i)/(np.std(mask_comb)*np.std(mask_i))
    p_cor = p_cor/len(mask_i_li)
    print("P Cor: "+str(round(p_cor, 10))+" | Scalers: "+str(scaler))
    return (1/p_cor)


def corr_top(m1, m2):
    m1_avg = np.average(m1)
    m2_avg = np.average(m2)
    return np.sum((m1-m1_avg)*(m2-m2_avg))

def corr_bottom(m1, m2):
    m1_avg = np.average(m1)
    m2_avg = np.average(m2)
    m1_com = np.sum(np.square(m1-m1_avg))
    m2_com = np.sum(np.square(m2-m2_avg))
    return math.sqrt(m1_com*m2_com)


def all_corr(scaler, mask, mask_neg=[]):
    scaler = np.append(scaler, 1-sum(scaler))
    mask_i_li = []
    for i in range(len(mask)):
        if len(mask_neg) == len(mask[i]):
            mask_i_temp = (mask[i] - mask_neg) * scaler[i]
        else:
            mask_i_temp = mask[i] * scaler[i]
        mask_i_temp[mask_i_temp == None] = 0
        mask_i_temp[mask_i_temp < 0] = 0
        mask_i_li.append(mask_i_temp)
        try:
            mask_comb += mask_i_temp
        except:
            mask_comb = mask_i_temp

    p_cor = 0
    for mask_i in mask_i_li:
        if corr_bottom(mask_i, mask_comb) == 0:
            continue
        else:
            p_cor += math.pow(corr_top(mask_i, mask_comb)/corr_bottom(mask_i, mask_comb), 2)
    p_cor = math.sqrt(p_cor)
    print("P Cor: "+str(round(p_cor, 10))+" | Scalers: "+str(scaler))
    
    return (1/p_cor)


def get_rms(m1, m2):
    no = len(m1)
    take = np.square(m2-m1)
    return math.sqrt(np.sum(take)/no)

def all_rms(scaler, mask, mask_neg=[]):

    scaler = np.append(scaler, 1-sum(scaler))

    mask_i_li = []
    for i in range(len(mask)):
        if len(mask_neg) == len(mask[i]):
            mask_i_temp = (mask[i] - mask_neg) * scaler[i]
        else:
            mask_i_temp = mask[i] * scaler[i]
        mask_i_temp[mask_i_temp == None] = 0
        mask_i_temp[mask_i_temp < 0] = 0
        mask_i_li.append(mask_i_temp)
        try:
            mask_comb = mask_comb + mask_i_temp
        except:
            mask_comb = mask_i_temp

    masks_flat = []
    for mask in mask_i_li:
        masks_flat.append(mask.flatten())

    masker = []
    corr_out = []
    for i in range(len(masks_flat)):
        c_mask = masks_flat[i]
        c_mask_review = []
        temp = []
        corr_out_temp = []
        mask_x = []
        for ii in range(len(c_mask)):
            if c_mask[ii] != 0:
                temp.append(ii)
                mask_x.append(c_mask[ii])

        for ii in range(len(masks_flat)):
            mask_y = []
            for iii in range(len(temp)):
                mask_y.append(masks_flat[ii][temp[iii]])


            corr_out_temp.append(get_rms(np.array(mask_x), np.array(mask_y)))
        corr_out.append(corr_out_temp)
    #rms = np.sum(np.array(corr_out))
    rms = np.average(np.array(corr_out))
    print("RMS: "+str(round(rms, 10))+" | Scalers: "+str(scaler))
    
    return (rms)


def run_minimize(mask, mask_neg=[], precision=1e-4):
    start_points = []
    for i in range(len(mask)-1):
        start_points.append(round(1/len(mask),2))
        mask[i][mask[i] >= 255] = 255
    res = minimize(all_rms, start_points, args=(mask, mask_neg), method='nelder-mead',
                options={'xatol': precision, 'disp': True})
    opt_out = res['final_simplex'][0][0]
    scaler = []
    final_val = 0
    for outs in opt_out:
        scaler.append(outs)
        final_val += outs
    scaler.append(1 - final_val)
    with open("src/data-small/scaler_store.txt", "w") as f:
        f.write(str(scaler))
    return scaler