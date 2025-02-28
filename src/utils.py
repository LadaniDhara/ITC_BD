def format_tube_status(data):
    """Formats the Tube status data for display."""
    if not data:
        return "No data available."

    status_message = "\nLondon Underground Status:\n"
    for line in data:
        name = line["name"]
        status = line["lineStatuses"][0]["statusSeverityDescription"]
        reason = line["lineStatuses"][0].get("reason")  # Defaults to None
        
        status_message += f"🚇 {name}: {status}\n"
        if reason:
            status_message += f"   🔹 {reason}\n"

    return status_message
