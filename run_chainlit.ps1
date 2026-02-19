# RotterMaatje Chainlit UI Launcher
# Run this script to start the chatbot interface

Write-Host "Starting RotterMaatje Chainlit UI..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

uv run python -m chainlit run src/web/app.py -w
