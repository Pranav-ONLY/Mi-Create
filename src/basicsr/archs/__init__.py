import importlib
from copy import deepcopy
from os import path as osp

from basicsr.utils import get_root_logger, scandir
from basicsr.utils.registry import ARCH_REGISTRY

__all__ = ['build_network']

# automatically scan and import arch modules for registry
# scan all the files under the 'archs' folder and collect files ending with
# '_arch.py'
# arch_folder = osp.dirname(osp.abspath(__file__))
# arch_filenames = [osp.splitext(osp.basename(v))[0] for v in scandir(arch_folder) if v.endswith('_arch.py')]
# # import all the arch modules
# _arch_modules = [importlib.import_module(f'basicsr.archs.{file_name}') for file_name in arch_filenames]

from . import arch_util
from . import basicvsrpp_arch
from . import basicvsr_arch
from . import dfdnet_arch
from . import dfdnet_util
from . import discriminator_arch
from . import duf_arch
from . import ecbsr_arch
from . import edsr_arch
from . import edvr_arch
from . import hifacegan_arch
from . import hifacegan_util
from . import inception
from . import rcan_arch
from . import ridnet_arch
from . import rrdbnet_arch
from . import spynet_arch
from . import srresnet_arch
from . import srvgg_arch
from . import stylegan2_arch
from . import swinir_arch
from . import tof_arch
from . import vgg_arch


def build_network(opt):
    opt = deepcopy(opt)
    network_type = opt.pop('type')
    net = ARCH_REGISTRY.get(network_type)(**opt)
    logger = get_root_logger()
    logger.info(f'Network [{net.__class__.__name__}] is created.')
    return net
