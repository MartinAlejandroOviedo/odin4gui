# parser.py

def parse_odin_output(line: str) -> dict:
    """
    Analisa uma linha de saída do odin4 e tenta extrair o status e progresso.
    """
    line = line.strip()
    
    if not line:
        return {"type": "log", "message": ""}
        
    # Exemplo: Sending packet 10/320...
    if "Sending packet" in line and "/" in line:
        try:
            parts = line.split(" ")
            progress_part = parts[-1] # "10/320..."
            current, total = map(int, progress_part.strip('...').split('/'))
            percentage = int((current / total) * 100)
            return {
                "type": "progress",
                "current": current,
                "total": total,
                "percentage": percentage,
                "message": line
            }
        except Exception:
            pass # Falha na extração do progresso, trata como log normal

    # Status final e comandos chave
    if line.upper() == "PASS":
        return {"type": "status", "level": "success", "message": line}
    if "FAIL" in line.upper() or "ERROR" in line.upper():
        return {"type": "status", "level": "error", "message": line}
    if "Rebooting" in line:
        return {"type": "event", "message": line}

    # Default: Apenas uma mensagem de log
    return {"type": "log", "message": line}

def format_log(parsed_data: dict) -> str:
    """
    Formata o log para exibição na QTextEdit (pode adicionar HTML para cor)
    """
    msg = parsed_data['message']
    
    if parsed_data['type'] == 'progress':
        return f"[PROCESSO {parsed_data['percentage']}%] {msg}"
    if parsed_data['type'] == 'status' and parsed_data['level'] == 'success':
        return f"\n*** SUCESSO ***: {msg}\n"
    if parsed_data['type'] == 'status' and parsed_data['level'] == 'error':
        return f"\n!!! ERRO CRÍTICO !!!: {msg}\n"
        
    return f" > {msg}"
    