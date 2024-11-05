from django.shortcuts import render, get_object_or_404
from llenar_quiniela.models import Prediccion
from tabla_general.models import Equipos, Jornadas, Cartas, Puntos_extra, Colores, Cartas_aux, jugadores_gol, Puntos_cartas, tiempo

import sqlite3
# Create your views here.

Jugadores = ['Leo', 'Manuel', 'Luis Angel', 'Juan Luis', 'Omar', 'Hector', 'Horacio', 'Fernando', 'Bryan', 'Jorge', 'Josue', 'Rafa', 'Erick', 'Miguel', 'Alfonso', 'Saem']
def sec_resultados(nj):
    jornada = f'pJ{nj}'
    
    # Obtener el valor de la jornada desde el modelo Prediccion
    resultado = Prediccion.objects.filter(nombre='Resultados').values_list(jornada, flat=True)
    resultado = str(resultado[0])
    #print(resultado)
    return resultado
def marcador_a_secuencia(secuencia):
    elementos = secuencia.split(', ')

    letras_resultado = []

    for elemento in elementos:
        if '-' in elemento:
            numero1, numero2 = map(int, elemento.split('-'))

            if numero1 > numero2:
                letras_resultado.append('L')
            elif numero1 < numero2:
                letras_resultado.append('V')
            else:
                letras_resultado.append('E')
        else:
            letras_resultado.append(elemento)

    return ', '.join(letras_resultado)
def get_card(nj, nombre):
    jornada = f'j{nj}'
    
    # Realizar la consulta utilizando los modelos de Django
    resultados = Cartas.objects.filter(nombre=nombre).values_list(jornada, flat=True)
    resultados = str(resultados[0])
    return resultados
def get_predict(nj, nombre):
    jornada = f'pJ{nj}'
    # Realizar la consulta utilizando los modelos de Django
    resultados = Prediccion.objects.filter(nombre=nombre).values_list(jornada, flat=True)
    resultados = str(resultados[0])
    return resultados
def get_jugadores_gol(nj):
    jornada = f'j{nj}'
    
    # Obtener el objeto de jugadores_gol
    jugadores_gol_obj = jugadores_gol.objects.first()
    
    if jugadores_gol_obj:
        # Obtener el valor del campo correspondiente (j1, j2, etc.)
        return getattr(jugadores_gol_obj, jornada)
    
    return None
def get_tiempo(nj):
    jornada = f'j{nj}'
    
    # Obtener el objeto de jugadores_gol
    tiempo_obj = tiempo.objects.first()
    
    if tiempo_obj:
        # Obtener el valor del campo correspondiente (j1, j2, etc.)
        return getattr(tiempo_obj, jornada)
    
    return None
def get_card_aux(nj, nombre):
    jornada = f'j{nj}'
    # Realizar la consulta utilizando los modelos de Django
    resultados = Cartas_aux.objects.filter(nombre=nombre).values_list(jornada, flat=True)
    resultados = str(resultados[0])
    return resultados
def get_points(prediccion_n, prediccion_s, carta, pred_j, carta_aux, jug_gol, tiempos):
    sec_colores = ['lightsalmon', 'lightsalmon', 'lightsalmon', 'lightsalmon', 'lightsalmon', 'lightsalmon', 'lightsalmon', 'lightsalmon', 'lightsalmon', 'lightsalmon', 'lightsalmon']
    correctos = [item.strip() for item in prediccion_s.split(',')]
    pred = [item.strip() for item in pred_j.split(',')]
    p_extra = 0
    #print(prediccion_s)
    #print(pred_j)
    # Suma de puntos para Opcion doble y Opcion triple
    if carta == 'OD' or carta == 'OT' or carta == 'IQ' or carta == 'NC':
        contador = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, pred)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'

            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
        #print(contador)
    elif carta == 'DQ':
        q1 = [elemento[0] for elemento in pred]
        q2 = [elemento[1] for elemento in pred]
        arr_col1 = []
        arr_col2 = []
        contador_q1 = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, q1)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador_q1 += 1
                    arr_col1.append(idx)
            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador_q1 += 1
                    arr_col1.append(idx)
        contador_q2 = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, q2)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador_q2 += 1
                    arr_col2.append(idx)
            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador_q2 += 1
                    arr_col2.append(idx)
        if contador_q1 > contador_q2:
            contador = contador_q1
            for i in arr_col1:
                sec_colores[i] = 'lightgreen'
            q = q1
        elif contador_q2 > contador_q1:
            contador = contador_q2
            for i in arr_col2:
                sec_colores[i] = 'lightgreen'
            q = q2
        else:
            contador = contador_q1
            for i in arr_col1:
                sec_colores[i] = 'lightgreen'
            q = q1

        #print('Doble Quiniela: ', contador, q)
    elif carta == 'J':
        contador = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, pred)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
        p_extra, sec_colores = extra_points(carta, carta_aux, jug_gol, correctos, pred, prediccion_n, pred_j, sec_colores, tiempos)
        contador += p_extra
        #print('Jugador: ', contador)
    elif carta == 'T':
        contador = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, pred)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
        p_extra, sec_colores = extra_points(carta, carta_aux, jug_gol, correctos, pred, prediccion_n, pred_j, sec_colores, tiempos)
        contador += p_extra
    elif carta == 'M':
        pred_M = [letra.upper() for letra in pred]
        contador = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, pred_M)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
        p_extra, sec_colores = extra_points(carta, carta_aux, jug_gol, correctos, pred, prediccion_n, pred_j, sec_colores, tiempos)
        contador += p_extra
        #print('Multiplicador: ', contador)
    elif carta == 'MA':
        q_s = marcador_a_secuencia(pred_j)
        q_s = [item.strip() for item in q_s.split(',')]
        contador = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, q_s)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
        p_extra, sec_colores = extra_points(carta, carta_aux, jug_gol, correctos, pred, prediccion_n, pred_j, sec_colores, tiempos)
        contador += p_extra
        #print('Marcador: ', contador)
    else:
        contador = 0
        #print('No aplica')
    #print(correctos, pred)
    cadena_resultante = ', '.join(sec_colores)
    return contador, p_extra, cadena_resultante
def extra_points(carta, carta_aux, jug_gol, correctos, pred, pred_n, pred_j_n, colo, tiempos):
    puntos = 0
    if carta == 'J':
        if carta_aux in jug_gol:
            puntos = 2
            print(carta_aux)
            print('Puntos por jugador que mete gol: ', puntos)
    elif carta == 'T':
        if carta_aux in tiempos:
            carta_aux = carta_aux.split(":")
            ti = int(carta_aux[0].split("-")[1]) - int(carta_aux[0].split("-")[0])
            if ti == 45:
                puntos = 1
            elif ti == 30:
                puntos = 2  
            elif ti == 15:
                puntos = 3
            elif ti == 5:
                puntos = 5 
            else:
                puntos = 0         
        #print('Puntos por jugador que mete gol: ', puntos)
    elif carta == 'M':
        if correctos[int(carta_aux)] == pred[int(carta_aux)]:
            puntos = 2
            colo[int(carta_aux)] = 'goldenrod'
        #print('Puntos por el Multiplicador: ', puntos)
    elif carta == 'MA':
        s1 = [item.strip() for item in pred_n.split(',')]
        s2 = [item.strip() for item in pred_j_n.split(',')]
        c = []
        for i in range(len(s1)):
            if s1[i] == s2[i]:
                puntos += 1
                if puntos > 3:
                    puntos = 3
                c.append(i)
        for i in c:
            colo[i] = 'aquamarine'
        #print('Puntos por el Marcador: ', puntos)
    else:
        #print('No hay puntos extra')
        puntos = 0
    return puntos, colo

def get_pts_car(carta, nj):
    jornada = f'j{nj}'
    if carta == 'NC':
        pts = 9
    elif carta == 'OD':
        pts = 8
    elif carta == 'T':
        pts = 7
    elif carta == 'J':
        pts = 6
    elif carta == 'DQ':
        pts = 5
    elif carta == 'M':
        pts = 4
    elif carta == 'OT':
        pts = 3
    elif carta == 'MA':
        pts = 2
    else:
        pts = 1
    return pts

def actualizar_puntos_cartas(nombre, pts, nj):
    if nombre != 'Resultados':
        jornada = f'j{nj}'

        # Actualizar los puntos en la tabla Jornadas
        jornada_obj = Puntos_cartas.objects.get(nombre=nombre)
        setattr(jornada_obj, jornada, pts)
        jornada_obj.save()
        #print('SI')
def actualizar_puntos(nombre, nj, puntos, puntos_extra):
    if nombre != 'Resultados':
        jornada = f'j{nj}'

        # Actualizar los puntos en la tabla Jornadas
        jornada_obj = Jornadas.objects.get(nombre=nombre)
        setattr(jornada_obj, jornada, puntos)
        jornada_obj.save()
        #print('SI')
        # Actualizar los puntos extras en la tabla PuntosExtra
        puntos_extra_obj = Puntos_extra.objects.get(nombre=nombre)
        setattr(puntos_extra_obj, jornada, puntos_extra)
        puntos_extra_obj.save()
        #print('NO')
def actualizar_suma_puntos(nombre):
    if nombre != 'Resultados':
        # Obtener el objeto de jornadas
        jornadas_obj = Jornadas.objects.filter(nombre=nombre).first()

        if jornadas_obj:
            # Sumar los valores de las jornadas
            suma = sum([getattr(jornadas_obj, f'j{i}') for i in range(1, 18)])

            # Actualizar el campo suma_j en el objeto de jornadas
            jornadas_obj.suma_j = suma
            jornadas_obj.save()
def actualizar_suma_puntos_cartas(nombre):
    if nombre != 'Resultados':
        # Obtener el objeto de jornadas
        jornadas_obj = Puntos_cartas.objects.filter(nombre=nombre).first()
        jornadas_obj2 = Jornadas.objects.filter(nombre=nombre).first()

        if jornadas_obj:
            # Sumar los valores de las jornadas
            suma = sum([getattr(jornadas_obj, f'j{i}') for i in range(1, 18)])

            # Actualizar el campo suma_j en el objeto de jornadas
            jornadas_obj2.suma_j_c = suma
            jornadas_obj2.save()
def actualizar_colores(nombre, sec_colores, nj):
    if nombre != 'Resultados':
        # Obtener el objeto de colores
        colores_obj = Colores.objects.filter(nombre=nombre).first()

        if colores_obj:
            # Asignar el valor de sec_colores al campo correspondiente (j1, j2, etc.)
            setattr(colores_obj, f'j{nj}', sec_colores)
            colores_obj.save()
def actualizar_DQ_MA(nj, carta, nombre):
    registros = Prediccion.objects.filter(nombre=nombre)
    nombre_campo = f'pJ{nj}'
    #print('Jugadores Disponibles')
    if carta == 'DQ':
        for r in registros:
            conteo_X = getattr(r, nombre_campo).split(', ').count('X')
            if conteo_X == 11:
                objeto = get_object_or_404(Prediccion, nombre=r.nombre)
                setattr(objeto, nombre_campo, 'XX, XX, XX, XX, XX, XX, XX, XX, XX, XX, XX')
                objeto.save()
    elif carta == 'MA':
        for r in registros:
            conteo_X = getattr(r, nombre_campo).split(', ').count('X')
            if conteo_X == 11:
                objeto = get_object_or_404(Prediccion, nombre=r.nombre)
                setattr(objeto, nombre_campo, '0-0, 0-0, 0-0, 0-0, 0-0, 0-0, 0-0, 0-0, 0-0, 0-0, 0-0')
                objeto.save()
                
    """
    nombres = []
    if carta == 'DQ':
        print(nj, carta)
        for r in registros:
            if r.nombre != 'Resultados':
                #conteo_X = getattr(r, nombre_campo).split(', ').count('X')
                conteo_X = getattr(r, nombre_campo).split(', ').count('XX')
                print(conteo_X)
                if conteo_X == 11:

                    objeto = get_object_or_404(Prediccion, nombre=r.nombre)
                    print("SI")
                    setattr(objeto, nombre_campo, 'X, X, X, X, X, X, X, X, X, X, X')
                    objeto.save()
    """
    
def jornadas(request):

    if request.method == 'POST':
        jor = request.POST.get('opciones')
        jor = int(jor)
        #print(type(jor))
    else:
        jor = 1

    ############# ACTUALIZAR QUINIELAS #################
    Resultados = sec_resultados(jor)
    Resultados_s = marcador_a_secuencia(Resultados)
    Jugadores_con_gol = get_jugadores_gol(jor)
    Jugadores_con_gol = Jugadores_con_gol.split(', ')
    tiempos = get_tiempo(jor)
    tiempos = tiempos.split(', ')
    #print(Resultados)
    #print(Resultados_s)
    #print(Jugadores_con_gol)
    for n in range(len(Jugadores)):
        #print('XXXX', jor, Jugadores[n])
        carta = get_card(jor, Jugadores[n])
        actualizar_DQ_MA(jor, carta, Jugadores[n])
        carta_auxiliar = get_card_aux(jor, Jugadores[n])
        prediccion = get_predict(jor, Jugadores[n])
        pts_cartas = get_pts_car(carta, jor)
        actualizar_puntos_cartas(Jugadores[n], pts_cartas, jor)
        actualizar_suma_puntos_cartas(Jugadores[n])
        #print(Jugadores[n], carta, carta_auxiliar, prediccion)
        #print(Jugadores[n], carta, carta_auxiliar, prediccion)
        puntos, puntos_extra, sec_colores = get_points(Resultados, Resultados_s, carta, prediccion, carta_auxiliar, Jugadores_con_gol, tiempos)
        #print(puntos, puntos_extra, sec_colores)
        actualizar_puntos(Jugadores[n], jor, puntos, puntos_extra)
        actualizar_suma_puntos(Jugadores[n])
        actualizar_colores(Jugadores[n], sec_colores, jor)
        #print(puntos, puntos_extra)
        #print("*"*50)
    ####################################################


    # Obtener todos los registros de TuModelo
    registros = Prediccion.objects.all()
    registros2 = Equipos.objects.all()
    reg_puntos = Jornadas.objects.all()
    reg_car = Cartas.objects.all()
    reg_car_aux = Cartas_aux.objects.all()
    reg_extra = Puntos_extra.objects.all()
    reg_c = Colores.objects.all()

    # Función de orden personalizado
    def orden_personalizado(registro):
        if registro.nombre == 'Resultados':
            return (0, )
        return (1, registro.nombre)

    # Ordenar los registros usando la función personalizada
    registros = sorted(registros, key=orden_personalizado)
    reg_pts = []
    for i in registros:
        for j in reg_puntos:
            if i.nombre == j.nombre:
                reg_pts.append(j)
    reg_cartas = []
    for i in registros:
        for j in reg_car:
            if i.nombre == j.nombre:
                reg_cartas.append(j)
    reg_cartas_aux = []
    for i in registros:
        for j in reg_car_aux:
            if i.nombre == j.nombre:
                reg_cartas_aux.append(j)
    reg_ep = []
    for i in registros:
        for j in reg_extra:
            if i.nombre == j.nombre:
                reg_ep.append(j)
    reg_colores = []
    for i in registros:
        for j in reg_c:
            if i.nombre == j.nombre:
                reg_colores.append(j)
    #print(registros)
    #print(reg_pts)
    # Construye el nombre de la variable
    nombre_campo = f'pJ{jor}'
    nombre_campo2 = f'j{jor}'

    nom_lis_exp = []
    lis_exp = []

    for reg in reg_ep:
        if getattr(reg, nombre_campo2) != 0:
            lis_exp.append({
                'nombre': reg.nombre,
                'puntos_extra': getattr(reg, nombre_campo2),
            })
    # Procesar los campos pJ1 de cada registro
    datos_procesados = []
    sec_pred = []
    for registro in registros2:
        secuencia = [item.strip() for item in getattr(registro, nombre_campo2).split(',')]
        datos_procesados.append({
            'nombre': registro.eq,
        })
    for registro in registros:
        # Dividir la secuencia por comas y eliminar espacios en blanco
        secuencia = [item.strip() for item in getattr(registro, nombre_campo).split(',')]
        datos_procesados.append({
            'nombre': registro.nombre,
        })
    
        #print(type(secuencia))
    
    for i in range(len(secuencia)):
        l = []
        c = []
        for registro in registros2:
            secuencia = [item.strip() for item in getattr(registro, nombre_campo2).split(',')]
            l.append([secuencia[i], 'lightgreen'])
            #print(i)
        c.append('white')
        c.append('white')
        for registro in range(len(registros)):
            #print(len(registros), len(reg_colores), registro)
            # Dividir la secuencia por comas y eliminar espacios en blanco
            secuencia1 = [item.strip() for item in getattr(registros[registro], nombre_campo).split(',')]
            if registro == 0:
                val = 'thistle'
            elif len(reg_colores) >= registro:
                secuencia2 = [item.strip() for item in getattr(reg_colores[registro - 1], nombre_campo2).split(',')]
                val = secuencia2[i]
            else:
                val = 'white'
            l.append([secuencia1[i], val])
        for registro in reg_colores:
            secuencia = [item.strip() for item in getattr(registro, nombre_campo2).split(',')]
            c.append([secuencia[i], 'lightgoldenrodyellow'])
        sec_pred.append({
            'pred' : l,
            'color': c,
        })
    l = []
    c = []
    l.append(['', 'lightgoldenrodyellow'])
    l.append(['TOTAL', 'lightgoldenrodyellow'])
    c.append('white')
    c.append('white')
    for i in reg_pts:
        l.append([getattr(i, nombre_campo2), 'lightgoldenrodyellow'])
    for i in range(len(reg_pts)):
        c.append('white')
    sec_pred.append({
            'pred' : l,
            'color': c,
        })
    l = []
    c = []
    l.append(['', 'lightgoldenrodyellow'])
    l.append(['CARTAS', 'lightgoldenrodyellow'])
    c.append('white')
    c.append('white')
    for i in reg_cartas:
        l.append([getattr(i, nombre_campo2), 'lightgoldenrodyellow'])
    for i in range(len(reg_cartas)):
        c.append('white')
    sec_pred.append({
            'pred' : l,
            'color': c,
        })
    l = []
    c = []
    l.append(['Gol de jugador o Multiplicador', 'lightgoldenrodyellow'])
    l.append(['AUX', 'lightgoldenrodyellow'])
    c.append('white')
    c.append('white')
    for i in reg_cartas_aux:
        l.append([getattr(i, nombre_campo2), 'lightgoldenrodyellow'])
    for i in range(len(reg_cartas)):
        c.append('white')
    sec_pred.append({
            'pred' : l,
            'color': c,
        })
    #print(datos_procesados)
    return render(request, 'jornadas/jornadas.html', {'datos_procesados': datos_procesados, 'sec_pred': sec_pred, 'puntos_extra':lis_exp, 'page':'jornadas', 'jornada_actual': jor})