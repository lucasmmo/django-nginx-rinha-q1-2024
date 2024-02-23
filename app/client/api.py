from typing import Any
from ninja import NinjaAPI, Swagger, Schema
from .models import Clients, Transactions
from datetime import datetime
from django.utils.timezone import timezone

api = NinjaAPI(docs=Swagger())

class Erro(Schema):
    message: str

class TransacaoIn(Schema):
    valor: int
    tipo: str
    descricao: str

class TransacaoOut(Schema):
    saldo: int
    limite: int

@api.post('/{client_id}/transacoes', response={ 200: TransacaoOut, (404, 422): Erro })
async def transaction(request, client_id:int, txIn: TransacaoIn):
    try:

        client = await Clients.objects.aget(pk=client_id)

        if txIn.valor < 0:
            return 422, {
                "message": "invalid valor",
            }

        if len(txIn.descricao) > 10:
            return 422, {
                "message": "len invalid descricao"
            }

        match txIn.tipo:
            case "d":
                new_balance = client.actual_balance - txIn.valor
            case "c":
                new_balance = client.actual_balance + txIn.valor
            case _:
                return 422, {
                    "message": "invalid tipo"
                }

        if (new_balance + client.limits) < 0:
            return 422, {
                "message": "limite exceeded"
            }

        client.actual_balance = new_balance
        await client.asave()

        tx = Transactions(
            value=txIn.valor,
            transaction_type=txIn.tipo,
            description=txIn.descricao,
            completed_at=datetime.now(tz=timezone.utc),
            client=client
        )
        await tx.asave()

        return 200, {
            "saldo": client.actual_balance,
            "limite": client.limits
        }

    except Clients.DoesNotExist: 

        return 404, {
            "message": "client does not exists"
        }

class ExtratoOut(Schema):
    saldo: Any
    ultimas_transacoes: Any

@api.get("/{client_id}/extrato", response={200: ExtratoOut, (422, 404): Erro})
async def extract(request, client_id: int):
    try:

        client = await Clients.objects.aget(pk=client_id)

        last_transactions = []

        async for tx in Transactions.objects.order_by("completed_at").filter(client__pk=client_id)[:10]:
            last_transactions.append({
                "valor": tx.value,
                "tipo": tx.transaction_type,
                "descricao": tx.description,
                "realizada_em": tx.completed_at
            })
            
        return {
            "saldo": {
                "total": client.actual_balance,
                "data_extrato": datetime.now(),
                "limite": client.limits
            },
            "ultimas_transacoes": last_transactions
        }

    

    except Clients.DoesNotExist:

        return 404, {
            "message": "client does not exists"
        }
