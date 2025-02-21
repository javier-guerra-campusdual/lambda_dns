import boto3
import logging
from typing import List, Dict, Any

logger = logging.getLogger()

class Route53Manager:
    def __init__(self):
        self.route53 = boto3.client('route53')
        self.hosted_zone_id = self._get_hosted_zone_id()
        self.domain_suffix = '.campusdual.mkcampus.com'
    
    def _get_hosted_zone_id(self) -> str:
        """
        Obtiene el ID de la zona hospedada de Route 53.
        En este caso, está hardcodeado pero podría obtenerse dinámicamente.
        """
        # TODO: Obtener dinámicamente o desde variable de entorno
        return 'YOUR_HOSTED_ZONE_ID'
    
    def update_dns_records(self, dns_names: List[str], ip_address: str) -> List[Dict[str, Any]]:
        """
        Actualiza los registros DNS para los nombres proporcionados.
        """
        changes = []
        try:
            for dns_name in dns_names:
                fqdn = f"{dns_name.strip()}{self.domain_suffix}"
                change = {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': fqdn,
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [
                            {'Value': ip_address}
                        ]
                    }
                }
                changes.append(change)
            
            if changes:
                response = self.route53.change_resource_record_sets(
                    HostedZoneId=self.hosted_zone_id,
                    ChangeBatch={
                        'Comment': 'Actualización automática de DNS',
                        'Changes': changes
                    }
                )
                logger.info(f"Cambios en Route 53 iniciados: {response}")
                return changes
            
        except Exception as e:
            logger.error(f"Error actualizando registros DNS: {str(e)}")
            raise
        
        return []