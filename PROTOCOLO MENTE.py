import random
import json
import os
import time
from datetime import datetime

ARCHIVO_MEMORIA = "protocolos_desencriptados.json"
ARCHIVO_JUGADORES = "agentes_registrados.json"

# ========== SISTEMA ANTI-REPETICIÓN ==========

def cargar_memoria():
    if os.path.exists(ARCHIVO_MEMORIA):
        try:
            with open(ARCHIVO_MEMORIA, "r") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def guardar_memoria(memoria):
    with open(ARCHIVO_MEMORIA, "w") as f:
        json.dump(list(memoria), f)

def guardar_jugador(datos_jugador):
    jugadores = []
    if os.path.exists(ARCHIVO_JUGADORES):
        try:
            with open(ARCHIVO_JUGADORES, "r") as f:
                jugadores = json.load(f)
        except:
            jugadores = []
    jugadores.append(datos_jugador)
    with open(ARCHIVO_JUGADORES, "w") as f:
        json.dump(jugadores, f, indent=2)

# ========== 3.2 FUNCIONES DEL MODELO MATEMÁTICO ==========
# Estas 4 funciones son las que van en tu documento 3.2

def porcentaje_aciertos(aciertos):
    """P_a = (aciertos / 15) * 100, porcentaje de protocolos acertados."""
    total = 15
    return (aciertos / total) * 100

def porcentaje_fallos(aciertos):
    """P_f = 100 - P_a, porcentaje de protocolos fallados."""
    p_a = porcentaje_aciertos(aciertos)
    return 100 - p_a

def verificar_sin_repetir(clave, usados_partida, memoria_global):
    """Verifica que ejercicio ∉ lista_usados para no repetir protocolo."""
    if clave not in usados_partida and clave not in memoria_global:
        return True
    return False

def clasificar_rango(P_a):
    """Devuelve el mensaje de rango según el porcentaje."""
    if P_a >= 85:
        return "RANGO FANTASMA - Acceso total"
    if P_a >= 60:
        return "RANGO ESPECTRO - Acceso parcial"
    return "RANGO RASTREADO - Misión fallida"

# ========== GENERADOR DE PROTOCOLOS ==========

def generar_protocolo_unico(usados_partida, memoria_global):
    for _ in range(150):
        tipo = random.choice(['ecuacion', 'porcentaje', 'area', 'pitagoras', 'regla3', 'potencia'])
        
        if tipo == 'ecuacion':
            x = random.randint(2, 20)
            a = random.randint(2, 9)
            b = random.randint(1, 30)
            c = a * x + b
            pregunta = f"[PROTOCOLO ALFA] Resuelve: {a}x + {b} = {c} | ¿x?"
            clave = f"ec-{a}-{b}-{c}"
            resp = x
        elif tipo == 'porcentaje':
            p = random.choice([10,15,20,25,30,40,50,75])
            total = random.randint(5, 30) * 20
            pregunta = f"[PROTOCOLO BETA] ¿{p}% de {total}?"
            clave = f"por-{p}-{total}"
            resp = int(total * p / 100)
        elif tipo == 'area':
            base = random.randint(6, 24)
            altura = random.randint(5, 18)
            pregunta = f"[PROTOCOLO GAMMA] Área rectángulo {base} x {altura} ¿?"
            clave = f"area-{base}-{altura}"
            resp = base * altura
        elif tipo == 'pitagoras':
            triples = [(3,4,5),(5,12,13),(6,8,10),(8,15,17),(9,12,15)]
            a,b,c = random.choice(triples)
            pregunta = f"[PROTOCOLO DELTA] Catetos {a} y {b} ¿Hipotenusa?"
            clave = f"pit-{a}-{b}-{c}"
            resp = c
        elif tipo == 'regla3':
            c1 = random.randint(2, 8)
            p1 = random.randint(3, 15) * 5
            c2 = random.randint(9, 18)
            pregunta = f"[PROTOCOLO EPSILON] Si {c1} = ${p1} ¿{c2} cuánto?"
            clave = f"r3-{c1}-{p1}-{c2}"
            resp = int(p1 * c2 / c1)
        else:
            b = random.randint(3, 18)
            pregunta = f"[PROTOCOLO OMEGA] ¿{b}²?"
            clave = f"pot-{b}"
            resp = b ** 2

        # AQUI USAMOS LA FUNCIÓN DEL MODELO MATEMÁTICO
        if verificar_sin_repetir(clave, usados_partida, memoria_global):
            usados_partida.add(clave)
            return pregunta, resp, clave
    return None, None, None

# ========== REGISTRO DE JUGADOR ==========

def registrar_jugador():
    print("\n" + "="*65)
    print("  PROTOCOLO MENTE: LA ÚLTIMA ECUACIÓN")
    print("  >> REGISTRO DE AGENTE REQUERIDO <<")
    print("="*65)
    
    print("\n[ESCÁNER BIOMÉTRICO ACTIVO] Ingresa tus datos:\n")
    
    nombre = input("  1. Nombre completo: ").strip()
    while len(nombre) < 3:
        print("  [!] Nombre muy corto")
        nombre = input("  1. Nombre completo: ").strip()
    
    edad = input("  2. Edad: ").strip()
    curso = input("  3. Curso / Paralelo (ej: 2do B): ").strip()
    alias = input("  4. Alias de agente (ej: Fantasma_99): ").strip()
    if not alias:
        alias = nombre.split()[0] + f"_{random.randint(10,99)}"
    
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    datos = {
        "nombre": nombre,
        "edad": edad,
        "curso": curso,
        "alias": alias,
        "fecha_registro": fecha
    }
    
    print("\n" + "-"*65)
    print(f"  Agente registrado: {alias}")
    print("-"*65)
    
    guardar_jugador(datos)
    return datos

def calculadora_final(aciertos, total):
    # AQUI USAMOS LAS FUNCIONES DEL MODELO MATEMÁTICO
    porc_ac = porcentaje_aciertos(aciertos)
    porc_fa = porcentaje_fallos(aciertos)
    return porc_ac, porc_fa

# ========== JUEGO PRINCIPAL ==========

def main():
    memoria_global = cargar_memoria()
    usados_partida = set()
    
    datos_jugador = registrar_jugador()
    
    print("\n" + "="*65)
    print(f"  Bienvenido Agente {datos_jugador['alias'].upper()}")
    print(f"  Sincronización Neural: 92% | Bóveda: VAULT-09 BLOQUEADA")
    print(f"  Objetivo: Desencriptar 15 protocolos")
    print("="*65)
    input("\n>> Presiona ENTER para iniciar hackeo...")

    TOTAL = 15
    aciertos = 0
    fallos = 0

    for i in range(1, TOTAL + 1):
        preg, correcta, clave = generar_protocolo_unico(usados_partida, memoria_global)
        if preg is None:
            print("\n[!] Base de datos llena - Reiniciando...")
            memoria_global.clear()
            usados_partida.clear()
            preg, correcta, clave = generar_protocolo_unico(usados_partida, memoria_global)

        print(f"\n--- PROTOCOLO {i}/{TOTAL} ---")
        print(f"{preg}")
        try:
            resp = int(input(">> Código: "))
            if resp == correcta:
                print(">> [ACCESO CONCEDIDO] ✅")
                aciertos += 1
            else:
                print(f">> [DENEGADO] Era {correcta} ❌")
                fallos += 1
        except:
            print(f">> [ERROR] Era {correcta}")
            fallos += 1
        memoria_global.add(clave)

    guardar_memoria(memoria_global)
    porc_ac, porc_fa = calculadora_final(aciertos, TOTAL)
    rango = clasificar_rango(porc_ac)
    
    datos_jugador["aciertos"] = aciertos
    datos_jugador["fallos"] = fallos
    datos_jugador["porc_aciertos"] = round(porc_ac, 1)
    
    print("\n" + "="*65)
    print("  INFORME DE MISIÓN - VAULT-09")
    print("="*65)
    print(f"  Agente: {datos_jugador['alias']} ({datos_jugador['nombre']})")
    print(f"  Curso: {datos_jugador['curso']} | Edad: {datos_jugador['edad']}")
    print(f"  ---------------------------------------------")
    print(f"  Protocolos rotos: {aciertos}/{TOTAL}")
    print(f"  Precisión: {porc_ac:.1f}% | Fallos: {porc_fa:.1f}%")
    print(f"  >> {rango}")
    print("="*65)

if __name__ == "__main__":
    main()