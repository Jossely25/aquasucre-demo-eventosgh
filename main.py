from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

#BUS DE EVENTOS
#_________________________________________
def publicar_evento(nombre_evento, data):
    print(f"\n Evento publicado:{nombre_evento}")

    if nombre_evento == "factura_vencida":
        notificar_cliente(data)
        registrar_evento(data)
        log_evento(data)

#REACCIONES DE LOS CONSUMIDORES
#__________________________________________
def notificar_cliente(data):
    print(f"Notificando Cliente {data['cliente_id']} - factura vencida ({data['dias_mora']} días)")

def registrar_evento(data):
    print(f"REgistrando en la BD del Sistema: cliente {data['cliente_id']} con mora")

def log_evento(data):
    print(f" LOG: Evento procesado correctamente")

#RUTA BASE
#___________________________________________
@app.route("/")
def home():
    return "API AquaSucre funcionando...."

#ENDPOINT PRINCIPAL
#___________________________________________
@app.route("/facturas", methods=["POST"])
def crear_factura():
    data = request.get_json()

    cliente_id = data.get("cliente_id")
    valor = data.get("valor")
    fecha_vencimiento = data.get("fecha_vencimiento")

    #validación básica
    if not cliente_id or not valor or not fecha_vencimiento:
        return jsonify({"error": "Datos incompletos"}), 400
    
    try:
        fecha_venc = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido. Utiliza YYYY-mm-DD"}), 400

    hoy = datetime.now()

    print(f"\n Factura recibida para cliente {cliente_id}")

    #LOGICA DE NEGOCIO

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
            "mensaje": "Factura vencida detectada",
            "evento": "factura_vencida",
            "dias_mora": dias_mora
        })
    
    else:
        return jsonify({
            "mensaje": "Factura registrada sin mora"
        })

# EJECUCIÓN PARA RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
