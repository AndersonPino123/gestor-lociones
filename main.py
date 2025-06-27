from rich.console import Console
from rich.table import Table

# Importa tus funciones ya creadas
from clientes import agregar_cliente, ver_clientes, editar_cliente, eliminar_cliente, desactivar_cliente
from compras import agregar_compra, ver_compras, editar_compra, eliminar_compra
from reportes import reporte_compras_con_clientes, compras_por_cliente, resumen_compras_cliente, resumen_general_compras

console = Console()

# Mostrar el menú con Rich
def mostrar_menu():
    table = Table(title="🧴 MENÚ GESTOR DE LOCIONES", title_style="bold magenta")

    table.add_column("Opción", style="cyan", justify="center")
    table.add_column("Acción", style="green")

    table.add_row("1", "Agregar cliente")
    table.add_row("2", "Ver clientes")
    table.add_row("3", "Editar cliente")
    table.add_row("4", "Eliminar cliente")
    table.add_row("5", "Desactivar cliente")
    table.add_row("6", "Ver compras por cliente")
    table.add_row("7", "Resumen de compras por cliente")
    table.add_row("8", "Resumen general de todos los clientes")
    table.add_row("9", "Agregar compra")
    table.add_row("10", "Ver compras")
    table.add_row("11", "Editar compra")
    table.add_row("12", "Eliminar compra")
    table.add_row("13", "Reporte completo de compras")
    table.add_row("14", "Salir")

    console.print(table)

# Lógica del menú interactivo
def menu():
    while True:
        mostrar_menu()
        opcion = input("👉 Selecciona una opción: ").strip()

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
            console.print("👋 Hasta luego.", style="bold red")
            break
        else:
            console.print("⚠️ Opción no válida. Intenta nuevamente.", style="bold yellow")

# Ejecutar el programa
if __name__ == "__main__":
    menu()