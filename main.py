from clientes import agregar_cliente, ver_clientes, editar_cliente, eliminar_cliente, desactivar_cliente
from compras import agregar_compra, ver_compras, editar_compra, eliminar_compra
from reportes import reporte_compras_con_clientes, compras_por_cliente, resumen_compras_cliente, resumen_general_compras

def menu():
    while True:
        print("\n--- MENÚ GESTOR DE LOCIONES ---")
        print("1. Agregar cliente")
        print("2. Ver clientes")
        print("3. Editar cliente")
        print("4. Eliminar cliente")
        print("5. Desactivar cliente")
        print("6. Ver compras por cliente")
        print("7. Ver resumen de compras por cliente")
        print("8. Ver resumen general de todos los clientes")
        print("9. Agregar compra")
        print("10. Ver compras")
        print("11. Editar compra")
        print("12. Eliminar compra")
        print("13. Reporte compras por cliente")
        print("14. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_cliente()
        elif opcion == "2":
            ver_clientes()
        elif opcion == "3":
            editar_cliente()
        elif opcion == "4":
            eliminar_cliente()
        elif opcion == "5":
            desactivar_cliente()
        elif opcion == "6":
            compras_por_cliente()
        elif opcion == "7":
            resumen_compras_cliente()    
        elif opcion == "8":
            resumen_general_compras()
        elif opcion == "9":
            agregar_compra()
        elif opcion == "10":
            ver_compras()
        elif opcion == "11":
            editar_compra()
        elif opcion == "12":
            eliminar_compra()
        elif opcion == "13":
            reporte_compras_con_clientes()
        elif opcion == "14":
            print("👋 Hasta luego.")
            break
        else:
            print("⚠️ Opción no válida.")

menu()