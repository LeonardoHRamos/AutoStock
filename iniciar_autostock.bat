@echo off
REM ============================================================
REM  AutoStock - iniciar servidor para acesso da equipe na rede
REM  Basta dar duplo-clique neste arquivo.
REM  Mantenha esta janela ABERTA enquanto a equipe estiver usando.
REM  Para encerrar: feche a janela ou pressione Ctrl+C.
REM ============================================================

cd /d "%~dp0"

echo.
echo Iniciando o AutoStock...
echo.
echo Enderecos de acesso desta maquina na rede:
ipconfig | findstr /i "IPv4"
echo.
echo A equipe deve acessar no navegador:  http://SEU_IP:8000/
echo (troque SEU_IP por um dos enderecos IPv4 mostrados acima)
echo.

call ".venv\Scripts\activate.bat"
python manage.py runserver 0.0.0.0:8000

echo.
echo Servidor encerrado.
pause
