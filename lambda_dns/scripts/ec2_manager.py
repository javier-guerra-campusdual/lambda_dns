import boto3
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger()

class EC2Manager:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
    
    def get_instance_info(self, instance_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene la información detallada de una instancia EC2.
        """
        try:
            response = self.ec2.describe_instances(
                InstanceIds=[instance_id]
            )
            
            if response['Reservations'] and response['Reservations'][0]['Instances']:
                return response['Reservations'][0]['Instances'][0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo información de la instancia: {str(e)}")
            raise
    
    def get_dns_names_from_tags(self, instance_info: Dict[str, Any]) -> List[str]:
        """
        Extrae los nombres DNS del tag 'DNS_NAMES' de la instancia.
        """
        dns_names = []
        
        if 'Tags' in instance_info:
            for tag in instance_info['Tags']:
                if tag['Key'] == 'DNS_NAMES':
                    dns_names = [name.strip() for name in tag['Value'].split(',')]
                    break
        
        return dns_names