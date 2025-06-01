# API de Controle de Eventos

API RESTful em Python com Flask para gerenciamento de eventos, utilizando Firebase Realtime Database.

## Funcionalidades

- Criar evento
POST: /events
Ex:
{
  "name": "Apresentação Evaldo",
  "location": "Auditorio da PUC Contagem",
  "date": "2025-06-15",
  "price": 0.00
}
- Listar eventos
GET: /events - Listar todos eventos

- Obter evento específico
GET: /events/<event_id> - Obter evento específico
Ex: 
http://127.0.0.1:5000/events/c3fe1d55-1819-40e4-bc69-b53db456bfe5

- Atualizar evento
PUT: /events/<event_id> - Atualizar um evento
Ex: 
http://127.0.0.1:5000/events/c3fe1d55-1819-40e4-bc69-b53db456bfe5

- Deletar evento
DELETE: /events/<event_id> - Deletar um evento
Ex: 
http://127.0.0.1:5000/events/c3fe1d55-1819-40e4-bc69-b53db456bfe5

- Realizar Chekin
POST: [/checkin](http://127.0.0.1:5000/checkin)
EX:
{
    "event_id": "c3fe1d55-1819-40e4-bc69-b53db456bfe5",
    "cliente_id": "cliente456",
    "name": "João"
}

- Repetir check-in
Receberá erro de duplicidade: Cliente já realizou check-in neste evento

- Obter checkin específico
GET: /checkins/<event_id>
EX:
http://127.0.0.1:5000/checkins/c3fe1d55-1819-40e4-bc69-b53db456bfe5


- Atualizar checkin
PUT: http://127.0.0.1:5000/checkins/c3fe1d55-1819-40e4-bc69-b53db456bfe5/cliente456
EX:
{
  "name": "João Pedro"
}

- Excluir Chekin
DELETE: http://127.0.0.1:5000/checkins/c3fe1d55-1819-40e4-bc69-b53db456bfe5/cliente456
EX:
{
  "message": "Check-in do cliente cliente123 removido do evento ID_DO_EVENTO"
}
CASO NÃO EXISTA:
{
  "error": "Check-in não encontrado"
}

## Tecnologias

- Python 3.10+
- Flask
- Firebase Admin SDK
- Swagger para documentação

## Como rodar

1. Clone o repositório.
2. Instale as dependências:

```bash
pip install -r requirements.txt
