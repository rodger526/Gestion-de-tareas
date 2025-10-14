def agregar_tareas():
    tarea=input('ingrese el nombre de su tarea: ')
    tareas.append(tarea)
    print('tarea registrada con exito')

def ver_tarea():
    if not tareas:
        print('no existen tareas disponibles')
    else:
        print('tus tareas son: ')
        for i, tarea in enumerate (tareas):
            print(f'{i}. {tarea}')

def editar_tarea():
    if not tareas:
        print('no existen tareas registradas')
    else:
        print('lista de tareas: ')
        for i, tarea in enumerate(tareas):
            print(f'{i}. {tarea}')
        try:
            editar=int(input('ingrese el numero de la tarea que desea editar: '))
            if 0 <= editar < len (tareas):
                nueva = input ('ingrese la nueva tarea: ')
                tareas[editar]=nueva
                print('tarea actualizada')
            else:
                print('numero invalido')
        except ValueError:
            print('numero invalido')

def eliminar_tarea():
    if not tareas:
        print('No hay tareas para eliminar.')
    else:
        print('Lista de tareas:')
        for i, tarea in enumerate(tareas):
            print(f'{i}. {tarea}')
        try:
            eliminar = int(input('Ingrese el número de la tarea que desea eliminar: '))
            if 0 <= eliminar < len(tareas):
                tareas.pop(eliminar)
                print('Tarea eliminada.')
            else:
                print('Número inválido.')
        except ValueError:
            print('Entrada inválida.')

def salir():
    print('gracias por preferirnos')
    exit()

tareas=[]

while True:
    try:
        print('sistema de gestion de tareas')
        print('por favor ingrese solo numeros')
        print('1.ingresar\n2.visualizar\n3.editar\n4.eliminar\n5.salir')
        opcion=int(input('ingrese una opcion: '))
        if opcion==1:
            agregar_tareas()
        elif opcion==2:
            ver_tarea()
        elif opcion==3:
            editar_tarea()
        elif opcion==4:
            eliminar_tarea()
        elif opcion==5:
            salir()
        else:
            print('ingrese un numero del los recomendados')
    except ValueError:
        print('valor desconocido ingresado')