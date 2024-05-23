import random
import pandas as pd
from tabulate import tabulate

# Definición de las personas y roles
personas_roles = {
    'JVG': ['DG'],
    'HYV': ['DR', 'TR'],
    'PGR': ['DM'],
    'MFE': ['DE'],
    'GTR': ['TR'],
    'LPG': ['TR', 'TC'],
    'RGB': ['TR', 'TC'],
    'BJC': ['TR'],
    'MDS': ['TC'],
    'HJR': ['PS'],
    'PTS': ['PS'],
    'IHP': ['PS']
}

# Definición de las tareas y roles asignados
tareas_roles = {
    'T1': ['DR'],
    'T2.1': ['TR'],
    'T2.2': ['TC'],
    'T3': ['DM'],
    'T4': ['DE', 'PS']
}

# Políticas de control de acceso
policies = {
    'R1': ('T2.1', 'T2.2'),
    'R2': ('T3', 'T4'),
    'R3': ('GTR', 'MDS'),
    'R4': 'JVG'
}

# Inicializar contadores de participación
participacion = {persona: 0 for persona in personas_roles.keys()}

# Función para asignar tareas equilibrando la carga
def asignar_tareas(instancias, tareas_roles, personas_roles, policies):
    resultados = []

    for _ in range(instancias):
        instancia = {}
        
        # Asignar T1
        if policies['R4'] == 'JVG':
            instancia['T1'] = 'JVG'
            participacion['JVG'] += 1
        else:
            posible_t1 = [p for p, roles in personas_roles.items() if any(r in roles for r in tareas_roles['T1'])]
            t1_person = min(posible_t1, key=lambda p: participacion[p])
            instancia['T1'] = t1_person
            participacion[t1_person] += 1
        
        # Asignar T2.1 y T2.2 con separación de deberes
        posible_t2_1 = [p for p, roles in personas_roles.items() if 'TR' in roles]
        t2_1_person = random.choice([p for p in posible_t2_1 if participacion[p] == min(participacion[p] for p in posible_t2_1)])
        instancia['T2.1'] = t2_1_person
        participacion[t2_1_person] += 1
        
        posible_t2_2 = [p for p, roles in personas_roles.items() if 'TC' in roles and p != t2_1_person]
        t2_2_person = random.choice([p for p in posible_t2_2 if participacion[p] == min(participacion[p] for p in posible_t2_2)])
        instancia['T2.2'] = t2_2_person
        participacion[t2_2_person] += 1

        # Binding de deberes
        if t2_1_person == 'GTR':
            instancia['T2.2'] = 'MDS'
            participacion['MDS'] += 1

        # Asignar T3 y T4 con separación de deberes
        posible_t3 = [p for p, roles in personas_roles.items() if 'DM' in roles]
        t3_person = random.choice([p for p in posible_t3 if participacion[p] == min(participacion[p] for p in posible_t3)])
        instancia['T3'] = t3_person
        participacion[t3_person] += 1

        posible_t4 = [p for p, roles in personas_roles.items() if any(r in roles for r in tareas_roles['T4']) and p != t3_person]
        t4_person_1 = random.choice([p for p in posible_t4 if participacion[p] == min(participacion[p] for p in posible_t4)])
        participacion[t4_person_1] += 1
        
        posible_t4_2 = [p for p in posible_t4 if p != t4_person_1]
        t4_person_2 = random.choice([p for p in posible_t4_2 if participacion[p] == min(participacion[p] for p in posible_t4_2)])
        participacion[t4_person_2] += 1
        
        instancia['T4'] = (t4_person_1, t4_person_2)

        resultados.append(instancia)
    
    return resultados

diff = 10
while diff > 4:
    participacion = {persona: 0 for persona in personas_roles.keys()}
    # Generar 20 instancias
    instancias_generadas = asignar_tareas(20, tareas_roles, personas_roles, policies)
    p_list = list(participacion.values())
    p_list.sort(reverse=True)
    diff = max(p_list[2:]) - min(p_list)

# Convertir a DataFrame para mejor visualización
df = pd.DataFrame(instancias_generadas)

# Imprimir resultados en formato tabular
print(tabulate(df, headers='keys', tablefmt='grid'))

# Imprimir la carga de trabajo de cada persona
print("\nLa diferencia de carga de trabajo entre las personas (sin contar los DR y DM, que tienen la misma tarea asignada siempre) es de:", diff)
print("Carga de trabajo de cada persona:")
for persona, carga in participacion.items():
    print(f"{persona}: {carga} tareas")
