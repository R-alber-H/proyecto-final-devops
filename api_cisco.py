import csv
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("DNAC_BASE_URL", "https://sandboxdnac.cisco.com")
USUARIO = os.getenv("DNAC_USER")
PASSWORD = os.getenv("DNAC_PASS")
NOMBRE_ARCHIVO = os.getenv("DNAC_OUTPUT_CSV", "inventario_red.csv")


def autenticar():
  print("\n=== AUTENTICANDO CON CISCO CATALYST CENTER ===")

  if not USUARIO or not PASSWORD:
    print("Error: Faltan DNAC_USER o DNAC_PASS en el archivo .env")
    return None

  url = f"{BASE_URL}/dna/system/api/v1/auth/token"
  try:
    response = requests.post(url, auth=(USUARIO, PASSWORD), verify=False)
    response.raise_for_status()
    print("¡Autenticación exitosa!")
    return response.json().get("Token")
  except Exception as e:
    print(f"Error de autenticación: {e}")
    return None


def obtener_inventario(token):
  url = f"{BASE_URL}/dna/intent/api/v1/network-device"
  headers = {"X-Auth-Token": token, "Content-Type": "application/json"}
  try:
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json().get("response", [])
  except Exception as e:
    print(f"Error al obtener inventario: {e}")
    return []


def exportar_csv(dispositivos):
  if not dispositivos:
    print("No hay datos para exportar")
    return

  try:
    with open(NOMBRE_ARCHIVO, mode="w", newline="", encoding="utf-8") as archivo:
      escritor = csv.writer(archivo)

      escritor.writerow([
          "Hostname",
          "IP",
          "Estado",
          "Versión",
          "Modelo",
          "SerialNumber",
          "Uptime",
      ])

      for d in dispositivos:
        escritor.writerow([
            d.get("hostname"),
            d.get("managementIpAddress"),
            d.get("reachabilityStatus"),
            d.get("softwareVersion"),
            d.get("platformId"),
            d.get("serialNumber"),
            d.get("upTime"),
        ])

    print(f"Inventario exportado correctamente a {NOMBRE_ARCHIVO}")
  except Exception as e:
    print(f"Error al exportar CSV: {e}")


def ejecutar_flujo():
  token = autenticar()
  if token:
    print("\nConsultando dispositivos de red...")
    dispositivos = obtener_inventario(token)
    print(f"Se encontraron {len(dispositivos)} dispositivos")
    exportar_csv(dispositivos)