# noinspection PyUnresolvedReferences
from .base import *

ALLOWED_CIDR_NETS = ['172.30.0.0/16']

KUBE_POD_IP = os.getenv('THIS_POD_IP', '')
if KUBE_POD_IP:
  ALLOWED_CIDR_NETS.append(KUBE_POD_IP)

MIDDLEWARE = [
    'allow_cidr.middleware.AllowCIDRMiddleware',
] +  MIDDLEWARE
