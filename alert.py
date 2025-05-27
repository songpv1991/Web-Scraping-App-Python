from PyQt5.QtWidgets import QMessageBox

def trigger_alert(window, row):
    match, outcome, market, old, new, drop, time = row
    QMessageBox.information(window, "Odds Drop Alert!",
        f"Match: {match}\nOutcome: {outcome}\nDrop: {drop}", QMessageBox.Ok)
