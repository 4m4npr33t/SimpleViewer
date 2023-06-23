import torch

from Common.StructuredGridClass import *
import numpy as np
import nibabel as nib
from copy import deepcopy


def LoadNifti(filename, device='cpu', dtype=torch.float32):
    nifti_img = nib.load(filename)
    dataArray = np.asanyarray(nifti_img.dataobj)

    if dataArray.dtype == 'uint16':
        dataArray = dataArray.astype('int32')
    tensor = torch.as_tensor(dataArray).unsqueeze(0)

    qform = nifti_img.get_qform()

    image_origin = qform[0:3, 3].copy()
    image_origin[0] *= -1

    image_spacing = np.diagonal(qform)[0:3].copy()
    image_spacing[0] *= -1

    image_size = np.asarray(dataArray.shape)

    out = StructuredGrid(
        size=image_size,
        spacing=image_spacing,
        origin=image_origin,
        device=device,
        dtype=dtype,
        tensor=tensor,
        channels=1
    )

    return out


def SaveNifti(grid, filename, header_filename):
    nifti_img = nib.load(header_filename)
    header = nifti_img.header
    im_aff = nifti_img.affine

    new_nifti = nib.Nifti1Image(grid.data.cpu().numpy().squeeze(), im_aff, header)

    nib.save(new_nifti, filename)

    return


def correctHeaders(filename):
    nifti_img = nib.load(filename)
    dataArray = np.asanyarray(nifti_img.dataobj)

    if dataArray.dtype == 'uint16':
        dataArray = dataArray.astype('int32')
    tensor = torch.as_tensor(dataArray).unsqueeze(0)

    qform = nifti_img.get_qform()

    image_origin = qform[0:3, 3].copy()
    image_origin[0] *= -1

    image_spacing = np.diagonal(qform)[0:3].copy()
    image_spacing[0] *= -1

    s = np.asarray(dataArray.shape)

    a = image_origin
    b = a + (image_spacing * (s - 1))
    s1 = np.min(np.vstack([a, b]), axis=0)

    affine = deepcopy(nifti_img.affine)
    affine[:3, 3] = s1
    affine[:3, :3] = np.abs(affine[:3, :3])
    affine[0, 0] *= -1
    affine[0, 1] *= -1
    affine[1, 0] *= -1
    affine[0, 3] *= -1

    hdr = nib.Nifti1Header()
    hdr.set_qform(affine, 0)
    hdr.set_xyzt_units(2)
    hdr.set_sform(affine)
    hdr.set_slope_inter(np.nan, np.nan)


    base_path = '/'.join(filename.split('/')[:-1]) + '/'
    new_nifti = nib.Nifti1Image(dataArray[::-1, ::-1, :][::-1, :, :], affine, hdr)
    nib.save(new_nifti, base_path+filename.split('/')[-1].split('.')[0]+'_corrected.nii.gz')

    return


def SaveNifti_fromGrid(grid, filename):

    origin = grid.origin
    spacing = grid.spacing

    origin[0] *= -1
    spacing[0] *= -1

    affine = torch.eye(4)
    affine[0:3, 3] = origin
    affine.diagonal()[:3].copy_(spacing)
    new_nifti = nib.Nifti1Image(grid.data.cpu().numpy().squeeze(), affine.cpu().numpy())

    nib.save(new_nifti, filename)

    return


def SaveNifti_withAffine(grid, affine, filename):
    # affine[0, 0] *= -1
    # affine[0, 3] *= -1
    # affine[0] *= -1
    new_nifti = nib.Nifti1Image(grid.data.cpu().numpy().squeeze(), affine.cpu().numpy())
    new_nifti.set_qform(affine.cpu().numpy(), 1)
    new_nifti.set_sform(affine.cpu().numpy(), 1)

    nib.save(new_nifti, filename)

    return