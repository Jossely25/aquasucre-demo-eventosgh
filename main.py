from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

#Bus de eventos
#________________________________________________
def publicar_evento(nombre_evento, data):
    # Aquí puedes implementar la lógica para publicar el evento en un bus de eventos real
    print(f"\n Evento publicado: {nombre_evento} ")

    if nombre_evento == "factura_vencida":
        notificar_cliente(data)
        registrar_evento(data)
        log_evento(data)

#Reaccione de los consumidores
def notificar_cliente(data):
    print(f"Notificando al cliente sobre la factura vencida: {data['cliente_id']} - factura vencida ({data['dias_mora']} dias)")

def registrar_evento(data):
    print(f"Registrando en la base de datos del sistema: {data['cliente_id']} - con mora")

def log_evento(data):
    print(f"Log: Evento procesado correctamente ")

#Ruta base 
#________________________________________________
@app.route('/')
def home():
    return "Api AquaSucre funcionando correctamente"

#Endpoint principal 
#________________________________________________
@app.route('/facturas', methods=['POST'])
def crear_factura():
    data = request.get_json()
    cliente_id = data.get('cliente_id')
    valor = data.get('valor')
    fecha_vencimiento = data.get('fecha_vencimiento')

    #Validacion basica
    if not cliente_id or not valor or not fecha_vencimiento:
        return jsonify({"error": "Faltan datos requeridos"}), 400
    
    try:
        fecha_venc = datetime.strptime(fecha_vencimiento, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400
    
    hoy = datetime.now()
    print(f"\n Creando factura para cliente {cliente_id} con valor {valor} y fecha de vencimiento {fecha_vencimiento.date()}")

    #logica de negocio
    if hoy > fecha_venc:
        dias_mora = (hoy - fecha_venc).days
        evento = {
            "cliente_id": cliente_id,
            "valor": valor,
            "dias_mora": dias_mora,
            "timestamp": datetime.now().isoformat()
        }
        publicar_evento("factura_vencida", evento)
        return jsonify({
            "message": "Factura vencida detectada", 
            "evento": "factura_vencida"
            "dias_mora": dias_mora
            })
    else:
        return jsonify({"message": "Factura creada exitosamente, no vencida"})
    
#ejecucion para render 
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

