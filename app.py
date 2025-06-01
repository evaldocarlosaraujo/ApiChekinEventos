from flask import Flask, request, jsonify
from firebase_config import initialize_firebase
from firebase_admin import db
import uuid
from datetime import datetime

app = Flask(__name__)

# Inicializa Firebase
initialize_firebase()

@app.route('/')
def home():
    return "API de Controle de Eventos - Online!"

# Criar um evento
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    event_id = str(uuid.uuid4())
    event_data = {
        "name": data.get("name"),
        "location": data.get("location"),
        "date": data.get("date"),
        "price": data.get("price")
    }

    db.reference('events').child(event_id).set(event_data)
    return jsonify({"id": event_id, "message": "Evento criado com sucesso"}), 201

# Listar todos os eventos
@app.route('/events', methods=['GET'])
def get_events():
    events_ref = db.reference('events')
    events = events_ref.get()
    if not events:
        return jsonify([]), 200
    return jsonify(events), 200

# Obter evento específico
@app.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):
    event_ref = db.reference('events').child(event_id)
    event = event_ref.get()
    if not event:
        return jsonify({"error": "Evento não encontrado"}), 404
    return jsonify(event), 200

# Atualizar evento
@app.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados JSON são obrigatórios"}), 400

    event_ref = db.reference('events').child(event_id)
    if not event_ref.get():
        return jsonify({"error": "Evento não encontrado"}), 404

    event_ref.update(data)
    return jsonify({"message": "Evento atualizado com sucesso"}), 200

# Deletar evento
@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    event_ref = db.reference('events').child(event_id)
    if not event_ref.get():
        return jsonify({"error": "Evento não encontrado"}), 404

    event_ref.delete()
    return jsonify({"message": "Evento deletado com sucesso"}), 200

# Check-in de cliente no evento
@app.route('/checkin', methods=['POST'])
def checkin():
    data = request.get_json()

    event_id = data.get('event_id')
    cliente_id = data.get('cliente_id')
    cliente_name = data.get('name')

    if not event_id or not cliente_id or not cliente_name:
        return jsonify({'error': 'event_id, cliente_id e name são obrigatórios'}), 400

    # Verifica se o evento existe
    event_ref = db.reference('events').child(event_id)
    if not event_ref.get():
        return jsonify({'error': 'Evento não encontrado'}), 404

    # Referência para o check-in
    ref = db.reference(f'/checkins/{event_id}/{cliente_id}')
    
    # Verifica se já existe check-in
    if ref.get():
        return jsonify({'error': 'Cliente já realizou check-in neste evento'}), 400

    # Dados do check-in
    from datetime import datetime
    checkin_data = {
        'name': cliente_name,
        'timestamp': datetime.utcnow().isoformat()
    }

    # Salva o check-in no Firebase
    ref.set(checkin_data)

    return jsonify({'message': f'Check-in realizado para o cliente {cliente_name} no evento {event_id}'}), 200

# Listar todos os check-ins de um evento
@app.route('/checkins/<event_id>', methods=['GET'])
def list_checkins(event_id):
    checkins_ref = db.reference(f'/checkins/{event_id}')
    checkins = checkins_ref.get()
    
    if not checkins:
        return jsonify({'message': 'Nenhum check-in encontrado para este evento'}), 200

    return jsonify(checkins), 200

# Consultar check-in específico de um cliente
@app.route('/checkins/<event_id>/<cliente_id>', methods=['GET'])
def get_checkin(event_id, cliente_id):
    checkin_ref = db.reference(f'/checkins/{event_id}/{cliente_id}')
    checkin = checkin_ref.get()

    if not checkin:
        return jsonify({'message': 'Check-in não encontrado para este cliente no evento'}), 404

    return jsonify(checkin), 200

# Cancelar check-in de cliente
@app.route('/checkins/<event_id>/<cliente_id>', methods=['DELETE'])
def delete_checkin(event_id, cliente_id):
    ref = db.reference(f'/checkins/{event_id}/{cliente_id}')
    if not ref.get():
        return jsonify({'error': 'Check-in não encontrado'}), 404

    ref.delete()
    return jsonify({'message': f'Check-in do cliente {cliente_id} removido do evento {event_id}'}), 200

# Atualizar check-in de cliente
@app.route('/checkins/<event_id>/<cliente_id>', methods=['PUT'])
def update_checkin(event_id, cliente_id):
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Campo "name" obrigatório para atualização'}), 400

    ref = db.reference(f'/checkins/{event_id}/{cliente_id}')
    checkin = ref.get()
    if not checkin:
        return jsonify({'error': 'Check-in não encontrado'}), 404

    from datetime import datetime
    updated_data = {
        'name': data.get('name'),
        'timestamp': datetime.utcnow().isoformat()
    }

    ref.update(updated_data)
    return jsonify({'message': f'Check-in do cliente {cliente_id} atualizado no evento {event_id}'}), 200

if __name__ == '__main__':
    app.run(debug=True)
