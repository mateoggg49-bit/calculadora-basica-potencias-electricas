# ============================================================
#   CALCULADORA DE POTENCIAS EN DC Y AC MONOFÁSICO - PROYECTO
# ============================================================

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#0 Notación de ingeniería
def to_engineering(value):
    if value == 0:
        return "0"
    exponent = int(math.floor(math.log10(abs(value)) / 3) * 3)
    scaled = value / (10 ** exponent)
    return f"{scaled:.4g}e{exponent}"
#1 Bienvenida al usuario
def welcome():
    print("\n==============================================================")
    print("        BIENVENIDO A LA CALCULADORA DE POTENCIAS")
    print("==============================================================")
    print("Este programa permite determinar potencias eléctricas en:")
    print("- Corriente Directa (DC)")
    print("- Corriente Alterna Monofásica (AC)")
    print("\nFUNCIONALIDADES:")
    print("• Cálculo de potencia en fuentes y cargas")
    print("• Manejo de unidades científicas (1e-3, 1e3, etc.)")
    print("• Diagramas: potencia vs tiempo (DC) y triángulo + potencia instantánea (AC)")
    print("• Análisis automático de resultados")
    print("• Exportación de resultados en CSV")
    print("\n==============================================================\n")
#2 Modulo de selección dc/ac
def select_mode():
    opcion = input("Seleccione el tipo de análisis [dc/ac]: ").strip().lower()
    while opcion not in ["dc", "ac"]:
        opcion = input("Entrada inválida. Escriba dc o ac: ").strip().lower()
    return opcion
#3 Selección carga/fuente
def select_element_type():
    opcion = input("¿Analizará una carga o una fuente? [carga/fuente]: ").strip().lower()
    while opcion not in ["carga", "fuente"]:
        opcion = input("Entrada inválida. Escriba carga o fuente: ").strip().lower()
    return opcion
#4 Ingreso de los datos en dc
def input_parameters_dc(element):

    print("\n--- INGRESO DE PARÁMETROS (DC) ---")
    print("Puede ingresar valores en notación científica (ej: 1e-3 = 1 mA).")

    if element == "fuente":
        V = float(input("Ingrese el voltaje (V): "))
        I = float(input("Ingrese la corriente (A): "))
        return {"V": V, "I": I, "R": None, "element": "fuente"}

    elif element == "carga":
        V = input("Voltaje (V), o Enter si no lo tiene: ")
        I = input("Corriente (A), o Enter si no la tiene: ")
        R = input("Resistencia (Ω), o Enter si no la tiene: ")

        V = float(V) if V else None
        I = float(I) if I else None
        R = float(R) if R else None

        datos = {"V": V, "I": I, "R": R, "element": "carga"}

        # Validación: al menos 2 parámetros
        if sum(x is not None for x in [V, I, R]) < 2:
            raise ValueError("Debe ingresar al menos dos parámetros entre V, I y R.")

        return datos
#5 Ingreso prametros ac monofásico
def input_parameters_ac(element):

    print("\n--- INGRESO DE PARÁMETROS (AC MONOFÁSICO) ---")
    print("Ingrese V e I como fasores en forma polar (magnitud y ángulo en grados).")

    if element == "fuente":
        Vmag = float(input("Magnitud del voltaje RMS (V): "))
        Vang = float(input("Ángulo del voltaje (°): "))
        Imag = float(input("Magnitud de la corriente RMS (A): "))
        Iang = float(input("Ángulo de la corriente (°): "))

        return {
            "Vmag": Vmag, "Vang": Vang,
            "Imag": Imag, "Iang": Iang,
            "element": "fuente"
        }

    elif element == "carga":
        print("\nDebe ingresar al menos dos parámetros entre voltaje, corriente e impedancia.")
        
        Vmag = input("Magnitud del voltaje RMS (V), o Enter: ")
        Vang = input("Ángulo del voltaje (°), o Enter: ")
        Imag = input("Magnitud de la corriente RMS (A), o Enter: ")
        Iang = input("Ángulo de la corriente (°), o Enter: ")
        
        Zmag = input("Magnitud de la impedancia (Ω), o Enter: ")
        Zang = input("Ángulo de la impedancia (°), o Enter: ")

        Vmag = float(Vmag) if Vmag else None
        Vang = float(Vang) if Vang else None
        Imag = float(Imag) if Imag else None
        Iang = float(Iang) if Iang else None
        Zmag = float(Zmag) if Zmag else None
        Zang = float(Zang) if Zang else None

        if sum(x is not None for x in [Vmag, Imag, Zmag]) < 2:
            raise ValueError("Debe ingresar al menos dos parámetros entre V, I y Z.")

        if Vmag is not None and Zmag is not None and Imag is None:
            Imag = Vmag / Zmag
            Iang = Vang - Zang

        if Imag is not None and Zmag is not None and Vmag is None:
            Vmag = Imag * Zmag
            Vang = Iang + Zang

        if Vmag is not None and Imag is not None and Zmag is None:
            Zmag = Vmag / Imag
            Zang = Vang - Iang

        return {
            "Vmag": Vmag, "Vang": Vang,
            "Imag": Imag, "Iang": Iang,
            "Zmag": Zmag, "Zang": Zang,
            "element": "carga"
        }

#6 Potencia DC
def calculate_dc(params):

    V = params["V"]
    I = params["I"]
    R = params["R"]

    if V is not None and I is not None:
        P = V * I
        formula = "P = V × I"

    elif V is not None and R is not None:
        P = (V ** 2) / R
        formula = "P = V² / R"

    elif I is not None and R is not None:
        P = (I ** 2) * R
        formula = "P = I² × R"

    else:
        raise ValueError("Faltan parámetros para el cálculo en DC.")

    return {
        "modo": "DC",
        "P (W)": to_engineering(P),
        "formula": formula
    }

#7 Potencia AC monofásica
def calculate_ac(params):

    Vmag = params["Vmag"]
    Vang = params["Vang"]
    Imag = params["Imag"]
    Iang = params["Iang"]

    V = Vmag * (math.cos(math.radians(Vang)) + 1j * math.sin(math.radians(Vang)))
    I = Imag * (math.cos(math.radians(Iang)) + 1j * math.sin(math.radians(Iang)))

    S = V * np.conjugate(I)
    P = S.real
    Q = S.imag
    S_va = abs(S)
    phi_deg = Vang - Iang
    FP = math.cos(math.radians(phi_deg))

    return {
        "modo": "AC",
        "P (W)": to_engineering(P),
        "Q (VAR)": to_engineering(Q),
        "S (VA)": to_engineering(S_va),
        "factor_potencia": FP,
        "phi_deg": phi_deg
    }
#8 Gráficos de análisis
# Potencia vs tiempo en DC (constante)
def plot_dc_power(P):
    P = float(P.split("e")[0]) * 10 ** int(P.split("e")[1])

    t = np.linspace(0, 1, 1000)
    p = np.full_like(t, P)

    plt.figure(figsize=(6,4))
    plt.plot(t, p)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Potencia (W)")
    plt.title("Potencia vs Tiempo (DC)")
    plt.grid(True)
    plt.show()


# Triángulo de potencias AC
def plot_ac_triangle(P, Q, S):
    P = float(P.split("e")[0]) * 10 ** int(P.split("e")[1])
    Q = float(Q.split("e")[0]) * 10 ** int(Q.split("e")[1])
    S = float(S.split("e")[0]) * 10 ** int(S.split("e")[1])

    plt.figure(figsize=(5,4))
    plt.plot([0, P], [0, 0], 'r-', label="P")
    plt.plot([0, 0], [0, Q], 'b-', label="Q")
    plt.plot([P, 0], [0, Q], 'g--', label="S")
    plt.title("Triángulo de Potencias (AC)")
    plt.xlabel("W")
    plt.ylabel("VAR")
    plt.grid(True)
    plt.legend()
    plt.axis("equal")
    plt.show()


# Potencia instantánea AC
def plot_ac_instant_power(V, I, phi_deg):
    t = np.linspace(0, 0.04, 2000)
    w = 2 * math.pi * 60
    phi = math.radians(phi_deg)

    v = np.sqrt(2)*V*np.sin(w*t)
    i = np.sqrt(2)*I*np.sin(w*t - phi)
    p = v*i

    plt.figure(figsize=(6,4))
    plt.plot(t, p)
    plt.title("Potencia Instantánea (AC)")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("p(t) (W)")
    plt.grid(True)
    plt.show()
#9 Análisis de resultados obtenidos
def analyze_results(res):

    print("\n----- ANÁLISIS AUTOMÁTICO -----")

    if res["modo"] == "DC":
        print("• La potencia es constante en el tiempo.")
        print("• Se trata de un sistema en corriente continua.\n")

    else:
        Q = float(res["Q (VAR)"].split("e")[0]) * 10 ** int(res["Q (VAR)"].split("e")[1])

        if Q > 0:
            print("• La carga es inductiva.")
        elif Q < 0:
            print("• La carga es capacitiva.")
        else:
            print("• La carga es puramente resistiva.")

        if abs(res["factor_potencia"]) < 0.8:
            print("• El factor de potencia es bajo, se recomienda corrección.")
        else:
            print("• El factor de potencia es adecuado.")

        print("• S, P y Q fueron determinados a partir de S = V·I*.\n")

#10 Exportación a CSV
def export_csv(res):
    df = pd.DataFrame([res])
    filename = "resultados_potencia.csv"
    df.to_csv(filename, index=False)
    print(f"\nArchivo CSV generado: {filename}")

    # Opción de descarga (solo funciona en Google Colab)
    try:
        from google.colab import files
        files.download(filename)
        print("Descarga iniciada...")
    except:
        print("Descarga automática no disponible fuera de Google Colab.")
#11 Función principal
def main():
    welcome()

    modo = select_mode()
    elemento = select_element_type()

    if modo == "dc":
        params = input_parameters_dc(elemento)
        resultados = calculate_dc(params)
        print("\nRESULTADOS:\n", resultados)
        plot_dc_power(resultados["P (W)"])

    elif modo == "ac":
        params = input_parameters_ac(elemento)
        resultados = calculate_ac(params)
        print("\nRESULTADOS:\n", resultados)

        plot_ac_triangle(resultados["P (W)"], resultados["Q (VAR)"], resultados["S (VA)"])

        V = params["Vmag"]
        I = params["Imag"]
        phi_deg = resultados["phi_deg"]
        plot_ac_instant_power(V, I, phi_deg)

    analyze_results(resultados)
    export_csv(resultados)


# Ejecutar
main()
