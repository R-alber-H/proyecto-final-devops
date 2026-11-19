import urllib3
from api_cisco import autenticar, exportar_csv, obtener_inventario

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
  print("\n========================================")
  print("  AUTOMATIZACIÓN CISCO CATALYST CENTER  ")
  print("========================================")

  token = autenticar()

  if not token:
    print("No se pudo obtener el token. Proceso detenido.")
    return

  print("\nConsultando dispositivos de red...")
  dispositivos = obtener_inventario(token)
  print(f"Se encontraron {len(dispositivos)} dispositivos")

  for d in dispositivos:
    print(f"=== Dispositivo: {d.get('hostname')} ===")
    print(f"    IP de Gestión:   {d.get('managementIpAddress')}")
    print(f"    Estado:          {d.get('reachabilityStatus')}")
    print(f"    Versión OS:      {d.get('softwareVersion')}")
    print(f"    Modelo:          {d.get('platformId')}")
    print(f"    Número de Serie: {d.get('serialNumber')}")
    print(f"    Tiempo activo:   {d.get('upTime')}")

  print("\nExportando inventario a CSV...")
  exportar_csv(dispositivos)
  print("Proceso finalizado.")


if __name__ == "__main__":
  main()