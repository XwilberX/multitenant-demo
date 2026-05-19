from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    name: str

    @abstractmethod
    def process(self, amount: float) -> dict:
        ...


class StripeProcessor(PaymentProcessor):
    name = "stripe"

    def process(self, amount: float) -> dict:
        return {
            "provider": "Stripe",
            "amount": amount,
            "status": "ok",
            "tx_id": f"ch_demo_{int(amount * 100)}",
        }


class MercadoPagoProcessor(PaymentProcessor):
    name = "mercadopago"

    def process(self, amount: float) -> dict:
        return {
            "provider": "MercadoPago",
            "amount": amount,
            "status": "ok",
            "tx_id": f"mp-demo-{int(amount * 100)}",
        }


_REGISTRY: dict[str, type[PaymentProcessor]] = {
    "stripe": StripeProcessor,
    "mercadopago": MercadoPagoProcessor,
}


def get_processor(name: str) -> PaymentProcessor:
    if name not in _REGISTRY:
        raise ValueError(f"Unknown payment provider: {name}")
    return _REGISTRY[name]()
