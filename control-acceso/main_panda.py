import random
import pandas as pd
from tabulate import tabulate
import itertools

roles_persona = {
    "DG": ["JVG"],
    "DR": ["HYV"],
    "DM": ["PGR"],
    "DE": ["MFE"],
    "TR": ["GTR", "LPG", "RGB", "HIV", "BJC"],
    "TC": ["RGB", "MDS", "LPG"],
    "PS": ["HJR", "PTS", "IHP"]
}

tareas_roles = {
    'T1': ['DR'],
    'T2.1': ['TR'],
    'T2.2': ['TC'],
    'T3': ['DM'],
    'T4': ['DE', 'PS']
}


def verificarSeparacionDeberes(comb):
    return comb[1] != comb[2] and comb[3] != comb[4] and comb[3] != comb[5] and comb[4] != comb[5]

def verificarBindingDeberes(comb):
    if comb[1] == "GTR":
        if comb[2] != "MDS":
            return False
    return True
            
def verificarConflictoIntereses(comb):
    if "JVG" in comb:
        if comb["T1"] != "JVG":
            return False
    return True

participacion = {persona:0 for persona in itertools.chain(*roles_persona.values())}

# Función para asignar tareas equilibrando la carga
def asignar_tareas(instances):
    resultados = []
        
    posible_t1 = [p for p in roles_persona[tareas_roles["T1"][0]]]
    posible_t2_1 = [p for p in roles_persona[tareas_roles["T2.1"][0]]]
    posible_t2_2 = [p for p in roles_persona[tareas_roles["T2.2"][0]]]
    posible_t3 = [p for p in roles_persona[tareas_roles["T3"][0]]]
    posible_t4_p1 = [p for p in roles_persona[tareas_roles["T4"][0]]]
    posible_t4_p2 = [p for p in roles_persona[tareas_roles["T4"][1]]]
    
    permutaciones = list(itertools.product(posible_t1, posible_t2_1, posible_t2_2, posible_t3, posible_t4_p1, posible_t4_p2))
    permutaciones =  [perm for perm in permutaciones if verificarBindingDeberes(perm) and verificarConflictoIntereses(perm) and verificarSeparacionDeberes(perm)]

    for i in range(instances):
        rand = random.randint(0, len(permutaciones) - 1)
        perm = permutaciones[rand]
        for persona in perm:
            participacion[persona] += 1
        resultados.append(permutaciones[rand])
    
    return resultados
diff = 10
# participacion = {persona:0 for persona in itertools.chain(*roles_persona.values())}
#     # Generar 20 instancias
# instancias_generadas = asignar_tareas(20)
# p_list = list(participacion.values())
# p_list.sort(reverse=True)
# diff = max(p_list[3:-1]) - min(p_list)
while diff > 3:
    participacion = {persona:0 for persona in itertools.chain(*roles_persona.values())}
    # Generar 20 instancias
    instancias_generadas = asignar_tareas(20)
    p_list = list(participacion.values())
    p_list.sort(reverse=True)
    diff = max(p_list[3:]) - min(p_list[:-1])

instancias_generadas = [[i[0], i[1], i[2], i[3], [i[4], i[5]]] for i in instancias_generadas]
# Convertir a DataFrame para mejor visualización
df = pd.DataFrame(instancias_generadas)
df.index = df.index + 1
# Imprimir resultados en formato tabular
print(tabulate(df, headers=list(tareas_roles.keys()), tablefmt='grid'))

# Imprimir la carga de trabajo de cada persona
print("\nLa diferencia de carga de trabajo entre las personas (sin contar los DR, DM y DE, que tienen la misma tarea asignada siempre) es de:", diff)
print("Carga de trabajo de cada persona:")
for persona, carga in participacion.items():
    print(f"{persona}: {carga} tareas")
