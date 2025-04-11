@echo off
title SYSON PDV PRO - Build & Exec
setlocal
set "NOME_EXECUTAVEL=janela"
set "ICONE=imagens\favicon.ico"
set "DIRETORIO_IMAGENS=imagens"
set "PYTHON_FILE=main.py"

echo.
echo 🔄 LIMPEZA DOS ARQUIVOS ANTERIORES...
rmdir /s /q build >nul 2>&1
rmdir /s /q dist >nul 2>&1
del /q %NOME_EXECUTAVEL%.spec >nul 2>&1

echo.
echo 🛠️ COMPILANDO O SISTEMA SYSON PDV PRÓ...
pyinstaller %PYTHON_FILE% ^
 --noconsole ^
 --onefile ^
 --windowed ^
 --icon=%ICONE% ^
 --add-data "%DIRETORIO_IMAGENS%;%DIRETORIO_IMAGENS%" ^
 --name %NOME_EXECUTAVEL%

echo.
if not exist dist\%NOME_EXECUTAVEL%.exe (
    echo ❌ ERRO: A compilação falhou. Verifique os logs acima.
    pause
    exit /b 1
)

echo ✅ COMPILADO COM SUCESSO!

echo.
echo 🚀 INICIANDO O SISTEMA...
start "" "dist\%NOME_EXECUTAVEL%.exe"

echo.
echo 📂 ABRINDO PASTA DIST...
start "" "dist"

echo.
echo ✅ PRONTO!
pause
