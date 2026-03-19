#!/usr/bin/env bash
# =============================================================================
# git_commit_con_status_<rama>_<YYYYMMDDHHmmss>.sh
#
# Script genérico y reutilizable para la rama 2-feature_eda_jj.
# En cada ejecución:
#   1. Lee git status y captura los cambios reales
#   2. Genera commit_message_<rama>_<timestamp>.txt con esos cambios
#   3. git add . (incluye el propio fichero de commit)
#   4. Muestra el stage y pide confirmación
#   5. git commit -F <fichero> + git push
#
# Uso: bash git_commit_con_status_2-feature_eda_jj.sh
# Ejecutar desde la raíz del proyecto: ~/Proyectos/p7_g1_multiclase/
# =============================================================================

set -e
set -u

RAMA="2-feature_eda_jj"

# ─── Timestamp en el momento de ejecución ─────────────────────────────────────
TIMESTAMP=$(date +%Y%m%d%H%M%S)
FICHERO_COMMIT="commit_message_${RAMA}_${TIMESTAMP}.txt"

echo ""
echo "========================================================"
echo "  git_commit_con_status_${RAMA}.sh"
echo "  Timestamp : $TIMESTAMP"
echo "  Fichero   : $FICHERO_COMMIT"
echo "========================================================"
echo ""

# ─── 0. Verificaciones previas ────────────────────────────────────────────────
echo "[0/6] Verificando entorno..."

if [ ! -f "pyproject.toml" ]; then
    echo "ERROR: Ejecuta desde la raíz del proyecto (donde está pyproject.toml)."
    exit 1
fi

RAMA_ACTUAL=$(git branch --show-current)
if [ "$RAMA_ACTUAL" != "$RAMA" ]; then
    echo "ERROR: Rama actual '$RAMA_ACTUAL' — se esperaba '$RAMA'."
    echo "       Ejecuta: git checkout $RAMA"
    exit 1
fi

echo "  ✓ Rama correcta: $RAMA"

# ─── 1. Capturar git status completo ──────────────────────────────────────────
echo ""
echo "[1/6] Leyendo git status..."

# Capturar la salida completa de git status para mostrarla en el commit
GIT_STATUS_COMPLETO=$(git status)

# Extraer ficheros por categoría usando git status --short
# Formato --short: XY filename
#   M  = modified (staged o unstaged)
#   D  = deleted
#   ?? = untracked
#   A  = added (staged)
#   R  = renamed

MODIFICADOS=""
ELIMINADOS=""
NUEVOS=""
RENOMBRADOS=""

while IFS= read -r linea; do
    # Los dos primeros caracteres son el estado XY, el resto el nombre
    estado="${linea:0:2}"
    fichero="${linea:3}"

    case "$estado" in
        " M"|"M "|"MM")
            MODIFICADOS="${MODIFICADOS}  · ${fichero}\n" ;;
        " D"|"D ")
            ELIMINADOS="${ELIMINADOS}  · ${fichero}\n" ;;
        "??")
            NUEVOS="${NUEVOS}  · ${fichero}\n" ;;
        " R"|"R ")
            RENOMBRADOS="${RENOMBRADOS}  · ${fichero}\n" ;;
        "AM"|"AD")
            MODIFICADOS="${MODIFICADOS}  · ${fichero} (staged+modified)\n" ;;
    esac
done < <(git status --short)

# Verificar que hay algo que commitear
TOTAL_CAMBIOS=$(git status --short | grep -v "^$" | wc -l)
if [ "$TOTAL_CAMBIOS" -eq 0 ]; then
    echo "  Sin cambios pendientes. Nada que commitear."
    exit 0
fi

echo "  ✓ Cambios detectados: $TOTAL_CAMBIOS ficheros"

# Mostrar resumen en consola
[ -n "$MODIFICADOS" ]  && echo -e "  Modificados:\n${MODIFICADOS}"
[ -n "$ELIMINADOS" ]   && echo -e "  Eliminados:\n${ELIMINADOS}"
[ -n "$NUEVOS" ]       && echo -e "  Nuevos (untracked):\n${NUEVOS}"
[ -n "$RENOMBRADOS" ]  && echo -e "  Renombrados:\n${RENOMBRADOS}"

# ─── 2. Generar fichero de commit con los cambios reales ──────────────────────
echo ""
echo "[2/6] Generando fichero de commit: $FICHERO_COMMIT"

# Cabecera del commit (línea de asunto — máx 72 chars recomendado por git)
ASUNTO="chore(jj): cambios menores rama ${RAMA} · ${TIMESTAMP}"

{
    echo "$ASUNTO"
    echo ""
    echo "RAMA   : $RAMA"
    echo "FECHA  : $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "CAMBIOS DETECTADOS POR git status"
    echo "=================================="
    echo ""

    if [ -n "$MODIFICADOS" ]; then
        echo "MODIFICADOS:"
        echo -e "$MODIFICADOS"
    fi

    if [ -n "$ELIMINADOS" ]; then
        echo "ELIMINADOS:"
        echo -e "$ELIMINADOS"
    fi

    if [ -n "$NUEVOS" ]; then
        echo "NUEVOS (untracked — se añaden con git add .):"
        echo -e "$NUEVOS"
    fi

    if [ -n "$RENOMBRADOS" ]; then
        echo "RENOMBRADOS:"
        echo -e "$RENOMBRADOS"
    fi

    echo ""
    echo "DESCRIPCIÓN DE CADA CAMBIO"
    echo "=========================="
    echo ""

    # ── Ficheros conocidos del proyecto — descripción automática ──────────────
    # El script reconoce los ficheros del proyecto y añade contexto.
    # Para ficheros no reconocidos deja una línea con '(pendiente de describir)'.

    TODOS_LOS_FICHEROS=$(git status --short | awk '{print $NF}')

    while IFS= read -r f; do
        case "$f" in
            notebooks/Preprocesamiento_p7_g1_multiclase_JJ.ipynb)
                echo "  $f"
                echo "    → Notebook de preprocesamiento actualizado"
                echo "      (código, outputs de ejecución o celdas markdown)"
                ;;
            notebooks/modelado_p7_g1_multiclase_JJ.ipynb)
                echo "  $f"
                echo "    → Notebook de modelado actualizado"
                ;;
            notebooks/EDA_Obesity_p7_g1_multiclase_JJ.ipynb)
                echo "  $f"
                echo "    → Notebook EDA actualizado"
                ;;
            docs/.obsidian/workspace.json)
                echo "  $f"
                echo "    → Estado del workspace de Obsidian (ventanas abiertas, cursor)"
                echo "      Cambio automático generado por Obsidian al abrir la carpeta docs/"
                ;;
            docs/p7_g1_multiclase.docx)
                echo "  $f"
                echo "    → Documento Word del proyecto actualizado"
                ;;
            "docs/p7_g1_multiclase - ipynb.docx")
                echo "  $f"
                echo "    → Documento Word con notebooks exportados, actualizado"
                ;;
            pyproject.toml)
                echo "  $f"
                echo "    → Configuración del proyecto / dependencias actualizada"
                ;;
            uv.lock)
                echo "  $f"
                echo "    → Lockfile uv actualizado (versiones exactas de dependencias)"
                ;;
            .gitignore)
                echo "  $f"
                echo "    → Reglas de exclusión git actualizadas"
                ;;
            files.zip|"files.*.zip"|*.zip)
                echo "  $f"
                echo "    → Fichero ZIP (exportación / backup de ficheros del proyecto)"
                ;;
            commit_message_*.txt)
                echo "  $f"
                echo "    → Fichero de commit anterior (registro de versión)"
                ;;
            commit_cambios_*.sh|git_commit_*.sh|push_rama_*.sh)
                echo "  $f"
                echo "    → Script de automatización git del proyecto"
                ;;
            data/processed/*.csv)
                echo "  $f"
                echo "    → Dataset procesado actualizado"
                ;;
            models/*.pkl)
                echo "  $f"
                echo "    → Modelo/artefacto sklearn actualizado"
                ;;
            reports/*.png|reports/*.csv)
                echo "  $f"
                echo "    → Informe / gráfico de resultados actualizado"
                ;;
            *)
                echo "  $f"
                echo "    → (pendiente de describir)"
                ;;
        esac
        echo ""
    done <<< "$TODOS_LOS_FICHEROS"

    echo ""
    echo "SALIDA COMPLETA DE git status"
    echo "=============================="
    echo "$GIT_STATUS_COMPLETO"

    echo ""
    echo "CONVENCIÓN DE NOMBRADO"
    echo "======================"
    echo "commit_message_<rama>_<YYYYMMDDHHmmss>.txt"
    echo "  <rama>           : rama git activa en el momento del commit"
    echo "  <YYYYMMDDHHmmss> : timestamp de ejecución del script"

} > "$FICHERO_COMMIT"

echo "  ✓ Fichero de commit generado"

# ─── 3. git add . ─────────────────────────────────────────────────────────────
echo ""
echo "[3/6] Añadiendo todos los cambios al stage (git add .)..."

git add .

echo ""
echo "  Ficheros en stage:"
git status --short

# ─── 4. Confirmación ──────────────────────────────────────────────────────────
echo ""
echo "========================================================"
echo "  Fichero de commit: $FICHERO_COMMIT"
echo "  ¿Confirmas el commit y push a '$RAMA'? (s/n)"
echo "========================================================"
read -r CONFIRMAR

if [ "$CONFIRMAR" != "s" ] && [ "$CONFIRMAR" != "S" ]; then
    echo "Operación cancelada. Deshaciendo git add..."
    git restore --staged . 2>/dev/null || true
    rm -f "$FICHERO_COMMIT"
    exit 0
fi

# ─── 5. Commit ────────────────────────────────────────────────────────────────
echo ""
echo "[4/6] Realizando commit..."
git commit -F "$FICHERO_COMMIT"
echo "  ✓ Commit: $(git log --oneline -1)"

# ─── 6. Push ──────────────────────────────────────────────────────────────────
echo ""
echo "[5/6] Push a GitHub..."
git push origin "$RAMA"

echo ""
echo "========================================================"
echo "  ✓ Push completado"
echo "  Fichero de commit guardado en el repo: $FICHERO_COMMIT"
echo "========================================================"
echo ""
echo "[6/6] Últimos 3 commits:"
git log --oneline -3
