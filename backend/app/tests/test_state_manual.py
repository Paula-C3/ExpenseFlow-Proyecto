from app.domain.entities.request import Request

def run_test():
    r = Request(1, "Compra laptop", 10)

    print("Estado inicial:", type(r.state).__name__)

    r.approve()
    print("Después de aprobar:", type(r.state).__name__)

    r.complete()
    print("Después de completar:", type(r.state).__name__)

if __name__ == "__main__":
    run_test()
