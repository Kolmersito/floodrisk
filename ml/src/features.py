"""Reglas temporales compartidas; construir variables después de auditar las fuentes."""
from datetime import date


def validate_cutoff(target_year: int, data_cutoff: str) -> None:
    if date.fromisoformat(data_cutoff) >= date(target_year, 1, 1):
        raise ValueError("El corte debe ser anterior al inicio del año objetivo")


def validate_availability(data_cutoff: str, available_at: str) -> None:
    if date.fromisoformat(available_at) > date.fromisoformat(data_cutoff):
        raise ValueError("El registro todavía no estaba disponible en la fecha de corte")
