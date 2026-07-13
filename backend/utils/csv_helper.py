import csv
import io


CSV_HEADERS = ["User ID", "Trek Name", "Location", "Booking Status", "Dates"]


def booking_history_csv(bookings):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(CSV_HEADERS)
    for booking in bookings:
        trek = booking.trek
        dates = f"{trek.start_date.isoformat()} to {trek.end_date.isoformat()}" if trek else ""
        writer.writerow([
            booking.user_id,
            trek.name if trek else "Deleted trek",
            trek.location if trek else "",
            booking.booking_status.value,
            dates,
        ])
    return output.getvalue()
