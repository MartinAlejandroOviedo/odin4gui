from pathlib import Path

ERROR_PREFIX = "ERROR"

NO_DEVICE_TEXT = "Ningún dispositivo encontrado o error."
DETECTING_DEVICES_TEXT = "Buscando..."

UI_TEXT = {
    "window_title": "Odin4 Linux GUI - Herramienta de flasheo",
    "firmware_group": "Archivos de firmware (.tar / .tar.md5)",
    "options_group": "Opciones",
    "device_group": "Dispositivo",
    "refresh_devices": "Actualizar lista",
    "start_flash": "INICIAR FLASH",
    "stop_flash": "DETENER",
    "logs_group": "Registros / Salida de Odin4",
    "status_ready": "Estado: Listo.",
    "status_scanning": "Estado: Escaneando dispositivos...",
    "status_detected": "Estado: {count} dispositivo(s) detectado(s).",
    "status_detection_error": "Estado: Error en la detección. Asegúrese de que odin4 esté configurado (reglas udev).",
    "status_starting": "Estado: Iniciando flash...",
    "status_canceling": "Estado: Cancelando...",
    "status_cancelled": "Estado: Flash cancelado.",
    "status_success": "Estado: ¡FLASH COMPLETADO CON ÉXITO! ✅",
    "status_fail": "Estado: ¡FALLO EN EL FLASH! ❌ ({status})",
    "warn_missing_firmware_title": "Atención",
    "warn_missing_firmware_body": "Seleccione al menos un archivo de firmware (AP/BL/CP/CSC).",
    "warn_invalid_firmware_title": "Atención",
    "warn_invalid_firmware_body": "Archivo inválido o inexistente: {path}",
    "info_success_title": "Éxito",
    "info_success_body": "El proceso de flash se completó.",
    "info_cancelled_title": "Cancelado",
    "info_cancelled_body": "El proceso de flash fue cancelado.",
    "error_fail_title": "Fallo",
    "error_fail_body": "Ocurrió un error durante el proceso de flash. Revise los registros.",
    "select_file_title": "Seleccionar archivo {part_key}",
    "select_file_filter": "Archivos de firmware (*.tar *.tar.md5);;Todos los archivos (*)",
}

ALLOWED_FIRMWARE_EXTENSIONS = {".tar", ".md5", ".tar.md5"}

def is_valid_firmware_path(path: str) -> bool:
    p = Path(path)
    if not p.exists():
        return False
    name = p.name.lower()
    if name.endswith(".tar.md5"):
        return True
    return p.suffix.lower() in ALLOWED_FIRMWARE_EXTENSIONS
