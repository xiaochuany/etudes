from fasthtml.common import *

app, rt = fast_app()

@rt("/")
def get():
    return Titled("mortgate calculator", 
        Grid(
            Input(type="number", placeholder="Loan Amount", id="P"),
            Input(type="number", placeholder="Interest rate (per cent)", id="r"),
            Input(type="number", placeholder="Loan Term (months)", id="n"),
            Button("Calculate", target_id="result", hx_put="/calculate", hx_include="#P,#r,#n"),),
        Div(id="result")
    )

@rt("/calculate")
def put(P:float,r:float,n:int):
    r= r/ 100 / 12
    m = P*r*(1+r)**n / ((1+r)**n - 1)
    return Details(
        Summary(H3(f"monthly payment {m:.2f}")), 
        Ul(Li(f"interest payment {P*r:.2f}"), Li(f"principle payment {m-P*r:.2f}")),
        open=True)

serve()
