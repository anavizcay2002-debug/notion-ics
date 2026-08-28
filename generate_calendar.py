import os
import requests
from datetime import datetime, timezone

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATA_SOURCE_ID = os.environ["NOTION_DATA_SOURCE_ID"]

NOTION_VERSION = "2026-03-11"
TIMEZONE = "Europe/Madrid"


def escape_ics(text):
    """Escapa caracteres especiales del formato iCalendar."""
    if text is None:
        return ""

    return (
        str(text)
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def get_title(properties):
    """Obtiene el título desde la propiedad lecture/assignment."""
    title_property = properties.get("lecture/assignment", {})

    title_parts = title_property.get("title", [])

    return "".join(
        item.get("plain_text", "")
        for item in title_parts
    ) or "Sin título"


def get_domain(properties):
    """Obtiene el texto de la relación domain si existe."""
    domain_property = properties.get("domain", {})

    relations = domain_property.get("relation", [])

    if not relations:
        return ""

    return f"Domain: {len(relations)} relacionado(s)"


def format_date_for_ics(date_string):
    """Convierte una fecha ISO de Notion al formato ICS."""

    if "T" not in date_string:
        # Evento de día completo
        date = datetime.strptime(date_string, "%Y-%m-%d")
        return "DATE", date.strftime("%Y%m%d")

    # Evento con hora
    date_string = date_string.replace("Z", "+00:00")
    dt = datetime.fromisoformat(date_string)

    return "DATE-TIME", dt.strftime("%Y%m%dT%H%M%S")


def get_notion_events():
    url = f"https://api.notion.com/v1/data_sources/{DATA_SOURCE_ID}/query"

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

    all_results = []
    payload = {}

    while True:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        all_results.extend(data.get("results", []))

        if not data.get("has_more"):
            break

        payload["start_cursor"] = data["next_cursor"]

    return all_results


def create_ics(events):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Notion Calendar Sync//ES",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-TIMEZONE:{TIMEZONE}",
    ]

    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    for event in events:
        properties = event.get("properties", {})

        date_property = properties.get("date", {})
        date_data = date_property.get("date")

        # Si no tiene fecha, no aparece en el calendario
        if not date_data or not date_data.get("start"):
            continue

        title = get_title(properties)
        domain = get_domain(properties)

        start_type, start = format_date_for_ics(
            date_data["start"]
        )

        end_value = date_data.get("end")

        lines.append("BEGIN:VEVENT")
        lines.append(f"UID:{event['id']}@notion-calendar-sync")
        lines.append(f"DTSTAMP:{now}")
        lines.append(f"SUMMARY:{escape_ics(title)}")

        if domain:
            lines.append(f"DESCRIPTION:{escape_ics(domain)}")

        if start_type == "DATE":
            lines.append(f"DTSTART;VALUE=DATE:{start}")

            if end_value:
                _, end = format_date_for_ics(end_value)
                lines.append(f"DTEND;VALUE=DATE:{end}")

        else:
            lines.append(
                f"DTSTART;TZID={TIMEZONE}:{start}"
            )

            if end_value:
                _, end = format_date_for_ics(end_value)
                lines.append(
                    f"DTEND;TZID={TIMEZONE}:{end}"
                )

        lines.append("END:VEVENT")

    lines.append("END:VCALENDAR")

    return "\r\n".join(lines) + "\r\n"


def main():
    print("Leyendo eventos de Notion...")

    events = get_notion_events()

    print(f"Eventos encontrados: {len(events)}")

    ics_content = create_ics(events)

    with open("calendar.ics", "w", encoding="utf-8") as file:
        file.write(ics_content)

    print("calendar.ics generado correctamente.")


if __name__ == "__main__":
    main()
