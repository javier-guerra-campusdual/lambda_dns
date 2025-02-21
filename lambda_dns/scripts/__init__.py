"""
DNS Updater Lambda Package
Proporciona funcionalidad para actualizar registros DNS en Route53 basado en tags de EC2.
"""

from dns_updater.handler import lambda_handler
from dns_updater.route53_manager import Route53Manager
from dns_updater.ec2_manager import EC2Manager

__version__ = '1.0.0'
__author__ = 'Campus Dual'

__all__ = ['lambda_handler', 'Route53Manager', 'EC2Manager']