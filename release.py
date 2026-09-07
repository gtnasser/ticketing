#!/usr/bin/env python3
"""Adiciona uma nova versão ao history.log.

Uso:
    python release.py <versão> "tipo: descrição" ["tipo: descrição" ...]

Exemplo:
    python release.py 1.6.0 "feat: página de relatório" "fix: ordenação da pesquisa"
"""

import sys
from datetime import date

HISTORY_FILE = "history.log"

# Tipos de conventional commits com emoji e rótulo em português
TIPO_EMOJI = {
    "feat": "✨ Nova funcionalidade",
    "fix": "🐛 Correção de bug",
    "refactor": "♻️ Refatoração",
    "docs": "📝 Documentação",
    "style": "🎨 Estilo",
    "perf": "⚡ Performance",
    "test": "✅ Testes",
    "chore": "🔧 Manutenção",
    "security": "🔒 Segurança",
}

def main():
    if len(sys.argv) < 3:
        print('Uso: python release.py <versão> "tipo: descrição" ["tipo: descrição" ...]')
        print('Ex.: python release.py 1.6.0 "feat: página de relatório" "fix: ordenação"')
        sys.exit(1)

    version = sys.argv[1]
    changes = sys.argv[2:]
    today = date.today().isoformat()

    # Agrupa as alterações por tipo
    groups = {}
    for change in changes:
        tipo, desc = change.split(":", 1)
        tipo = tipo.strip().lower()
        desc = desc.strip()
        groups.setdefault(tipo, []).append(desc)

    # Monta o bloco da nova versão
    lines = [f"# {version} — {today}", ""]
    for tipo, descs in groups.items():
        heading = TIPO_EMOJI.get(tipo, tipo)
        lines.append(f"### {heading}")
        for d in descs:
            lines.append(f"- {d}")
        lines.append("")

    block = "\n".join(lines).rstrip() + "\n\n---\n\n"

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        current = f.read()
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write(block + current)

    print(f"Versão {version} adicionada ao history.log")

if __name__ == "__main__":
    main()