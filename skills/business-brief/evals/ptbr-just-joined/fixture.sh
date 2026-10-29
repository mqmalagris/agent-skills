#!/usr/bin/env bash
set -euo pipefail
mkdir -p research

cat > research/notas-empresa.md <<'EOF'
# Colheita Direta, o que eu juntei (2026-10-20)

- O que é: marketplace que conecta pequenos produtores rurais a consumidores na Grande São
  Paulo. Entrega em até 2 dias.
- Como cobra: comissão de 12% sobre cada pedido, paga pelo produtor. O consumidor paga frete
  (R$ 9,90, grátis acima de R$ 120).
- Números da apresentação de onboarding (outubro de 2026): 1.200 produtores ativos, 45 mil
  pedidos por mês, ticket médio de R$ 85.
- Captação: Série A de R$ 40 milhões em 2025.
- CNPJ aberto em 2021, situação ativa.
- Reclame Aqui: nota 7,1. Reclamações mais comuns: "pedido atrasou", "produto veio diferente
  do anunciado", "cobrança em duplicidade no Pix".
- Concorrentes que o pessoal cita: iFood Mercado, apps de hortifrúti de bairro, feiras livres.
EOF

cat > research/meu-time.md <<'EOF'
# Meu time

- Entrei semana passada no time de Checkout: 4 devs e 1 PM. Stack: Next.js e Node.
- Ainda não sei por qual métrica o time é cobrado.
EOF
