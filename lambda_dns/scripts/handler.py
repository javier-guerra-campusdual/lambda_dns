import json
import logging
from typing import Dict, Any

from dns_updater.route53_manager import Route53Manager
from dns_updater.ec2_manager import EC2Manager

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Manejador principal de la función Lambda.
    Se activa cuando una instancia EC2 cambia de estado.
    """
    try:
        logger.info(f"Evento recibido: {json.dumps(event)}")
        
        # Extraer detalles de la instancia del evento
        instance_id = event['detail']['instance-id']
        instance_state = event['detail']['state']
        
        # Solo procesar si la instancia está en estado 'running'
        if instance_state != 'running':
            logger.info(f"Instancia {instance_id} no está en estado running. Estado actual: {instance_state}")
            return {'statusCode': 200, 'body': 'Instancia no está en estado running'}
        
        # Inicializar managers
        ec2_manager = EC2Manager()
        route53_manager = Route53Manager()
        
        # Obtener información de la instancia
        instance_info = ec2_manager.get_instance_info(instance_id)
        if not instance_info:
            return {'statusCode': 404, 'body': f'No se encontró la instancia {instance_id}'}
        
        # Obtener DNS names del tag
        dns_names = ec2_manager.get_dns_names_from_tags(instance_info)
        if not dns_names:
            logger.info(f"No se encontraron DNS names en los tags de la instancia {instance_id}")
            return {'statusCode': 200, 'body': 'No hay DNS names para actualizar'}
        
        # Obtener IP pública de la instancia
        public_ip = instance_info.get('PublicIpAddress')
        if not public_ip:
            return {'statusCode': 400, 'body': 'La instancia no tiene IP pública'}
        
        # Actualizar registros DNS
        updated_records = route53_manager.update_dns_records(dns_names, public_ip)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Registros DNS actualizados exitosamente',
                'updated_records': updated_records
            })
        }
        
    except Exception as e:
        logger.error(f"Error en la ejecución: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error interno: {str(e)}'
            })
        }