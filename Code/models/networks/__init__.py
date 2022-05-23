from .tecogan_nets import FRNet, SpatioTemporalDiscriminator, SpatialDiscriminator
from .rbpgan_nets import RBPN_RBPGAN

def define_generator(opt):
    net_G_opt = opt['model']['generator']

    if net_G_opt['name'].lower() == 'frnet':  # frame-recurrent generator
        net_G = FRNet(
            in_nc=net_G_opt['in_nc'],
            out_nc=net_G_opt['out_nc'],
            nf=net_G_opt['nf'],
            nb=net_G_opt['nb'],
            degradation=opt['dataset']['degradation']['type'],
            scale=opt['scale'])

    elif net_G_opt['name'].lower() == 'rbpn':  # frame-recurrent generator
        # TODO: Zabat nFrames for testing
        if 'nFrames' in net_G_opt:
            nFrames = net_G_opt['nFrames']
        else:
            nFrames = opt['train']['tempo_extent']
            # Adjust for pingpong criterion
            if opt['train'].get('pingpong_crit') is not None:
                nFrames = 2 * nFrames - 1

        net_G = RBPN_RBPGAN(
            num_channels=net_G_opt['num_channels'],
            base_filter=net_G_opt['base_filter'],
            feat=net_G_opt['feat'],
            num_stages=net_G_opt['num_stages'],
            n_resblock=net_G_opt['n_resblock'],
            nFrames=nFrames,
            degradation=opt['dataset']['degradation']['type'],
            scale_factor=opt['scale'])

    else:
        raise ValueError(f'Unrecognized generator: {net_G_opt["name"]}')

    return net_G

def define_discriminator(opt):
    net_D_opt = opt['model']['discriminator']

    if opt['dataset']['degradation']['type'] == 'BD':
        spatial_size = opt['dataset']['train']['crop_size']
    else:  # BI
        spatial_size = opt['dataset']['train']['gt_crop_size']

    if net_D_opt['name'].lower() == 'stnet':  # spatio-temporal discriminator
        net_D = SpatioTemporalDiscriminator(
            in_nc=net_D_opt['in_nc'],
            spatial_size=spatial_size,
            tempo_range=net_D_opt['tempo_range'],
            degradation=opt['dataset']['degradation']['type'],
            scale=opt['scale'])

    elif net_D_opt['name'].lower() == 'snet':  # spatial discriminator
        net_D = SpatialDiscriminator(
            in_nc=net_D_opt['in_nc'],
            spatial_size=spatial_size,
            use_cond=net_D_opt['use_cond'])

    else:
        raise ValueError(f'Unrecognized discriminator: {net_D_opt["name"]}')

    return net_D
