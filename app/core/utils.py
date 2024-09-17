from fastapi import Request


async def get_client_ip(request: Request) -> str:
    # Obtener la IP del cliente
    client_ip = request.client.host

    # Si el cliente está detrás de un proxy o balanceador de carga
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        client_ip = forwarded_for.split(',')[0].strip()

    return client_ip