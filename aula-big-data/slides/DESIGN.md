---
version: alpha
name: "Aula de Big Data — Engenharia de Dados"
description: "Identidade visual para o material didático deste repositório (notebooks, slides e diagramas sobre Big Data, arquitetura Lakehouse e modelagem dimensional). Proposta original, sem guia de marca, site ou assets prévios — ver seção Overview."
colors:
  primary: "#16213E"
  primaryDark: "#0D1526"
  secondary: "#3A6EA5"
  accent: "#D9A441"
  background: "#F7F8FA"
  surface: "#FFFFFF"
  border: "#E2E5EA"
  textPrimary: "#1A1D23"
  textSecondary: "#5B6270"
  textInverse: "#F7F8FA"
  success: "#166B44"
  warning: "#D9A441"
  error: "#C24444"
  info: "#3A6EA5"
  layerBronze: "#B08D57"
  layerSilver: "#A7B0B8"
  layerGold: "#D9A441"
typography:
  display:
    fontFamily: "Inter, 'Segoe UI', system-ui, sans-serif"
    fontSize: "40px"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  h1:
    fontFamily: "Inter, 'Segoe UI', system-ui, sans-serif"
    fontSize: "32px"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.005em"
  h2:
    fontFamily: "Inter, 'Segoe UI', system-ui, sans-serif"
    fontSize: "24px"
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "0em"
  h3:
    fontFamily: "Inter, 'Segoe UI', system-ui, sans-serif"
    fontSize: "19px"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0em"
  body:
    fontFamily: "Inter, 'Segoe UI', system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "0em"
  small:
    fontFamily: "Inter, 'Segoe UI', system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "0.01em"
  code:
    fontFamily: "'JetBrains Mono', 'Fira Code', ui-monospace, monospace"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0em"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "40px"
  xxl: "64px"
rounded:
  sm: "4px"
  md: "8px"
  lg: "16px"
  pill: "999px"
components:
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.textPrimary}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
  buttonPrimary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.textInverse}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm} {spacing.lg}"
  buttonSecondary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm} {spacing.lg}"
  badge:
    backgroundColor: "{colors.border}"
    textColor: "{colors.textPrimary}"
    rounded: "{rounded.pill}"
    padding: "{spacing.xs} {spacing.sm}"
  badgeLayerBronze:
    backgroundColor: "{colors.layerBronze}"
    textColor: "{colors.textPrimary}"
    rounded: "{rounded.pill}"
    padding: "{spacing.xs} {spacing.sm}"
  badgeLayerSilver:
    backgroundColor: "{colors.layerSilver}"
    textColor: "{colors.textPrimary}"
    rounded: "{rounded.pill}"
    padding: "{spacing.xs} {spacing.sm}"
  badgeLayerGold:
    backgroundColor: "{colors.layerGold}"
    textColor: "{colors.textPrimary}"
    rounded: "{rounded.pill}"
    padding: "{spacing.xs} {spacing.sm}"
  codeBlock:
    backgroundColor: "{colors.primaryDark}"
    textColor: "{colors.textInverse}"
    typography: "{typography.code}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  callout:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.textSecondary}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  diagramNode:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.textPrimary}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm} {spacing.md}"
  metricHighlight:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.textPrimary}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm} {spacing.md}"
  statusSuccess:
    backgroundColor: "{colors.success}"
    textColor: "{colors.textInverse}"
    rounded: "{rounded.pill}"
    padding: "{spacing.xs} {spacing.sm}"
  statusWarning:
    backgroundColor: "{colors.warning}"
    textColor: "{colors.textPrimary}"
    rounded: "{rounded.pill}"
    padding: "{spacing.xs} {spacing.sm}"
  statusError:
    backgroundColor: "{colors.error}"
    textColor: "{colors.textInverse}"
    rounded: "{rounded.pill}"
    padding: "{spacing.xs} {spacing.sm}"
  statusInfo:
    backgroundColor: "{colors.info}"
    textColor: "{colors.textInverse}"
    rounded: "{rounded.pill}"
    padding: "{spacing.xs} {spacing.sm}"
---

# Aula de Big Data — Engenharia de Dados

## Overview

Esta identidade cobre o material didático deste repositório: notebooks Jupyter, slides/apresentações (consumidos, por exemplo, pela skill `criar-slides-html`) e diagramas de arquitetura (Lakehouse, modelo estrela, pipelines Bronze/Silver/Gold).

**Este documento é uma proposta original.** Não havia guia de marca, site, CSS, tokens, logo ou apresentações anteriores para extrair — o repositório contém apenas notebooks e dados sintéticos, sem material de identidade visual (ver inventário abaixo). Todos os valores aqui são decisões de design tomadas para este propósito, não fatos extraídos de uma fonte existente, e ficam abertos a ajuste.

**Inventário de fontes consultadas:**

- Repositório do projeto (`README.md`, `PROJETO_HR_DATA_PIPELINE.md`, notebooks) — forneceu apenas o domínio de conteúdo (Big Data, Lakehouse, modelagem dimensional, RH), não valores visuais.
- Nenhum guia de marca, CSS, tokens, logo ou deck anterior encontrados.
- Direção de tom e tema definidos por decisão do responsável pelo curso: personalidade **técnico-corporativa** (alinhada ao universo de plataformas como Databricks, Microsoft Fabric e Snowflake) e tema **claro** como padrão para slides e demais artefatos.

**Personalidade:** sóbria, confiável, precisa — evita ilustração decorativa e prioriza clareza sobre dados, código e diagramas de arquitetura.

**Pendências explícitas** (não fabricadas, marcadas como lacuna):

- Não existe logo ou wordmark. Até que um seja fornecido, usar o nome por extenso ("Aula de Big Data") em `typography.h1` ou `typography.display` como substituto textual.
- Não há iconografia própria definida; usar um set neutro (ex.: Lucide/Feather) até decisão em contrário.
- Fontes (`Inter`, `JetBrains Mono`) são escolhas por adequação ao contexto técnico e por serem gratuitas/distribuíveis, não por herança de marca.

## Colors

Paleta técnico-corporativa: azul-marinho como cor de identidade, ouro âmbar como único acento de destaque, tons neutros para superfícies e texto.

| Token | Valor | Papel |
|---|---|---|
| `colors.primary` | `#16213E` | Cor de identidade — títulos de destaque, botão primário, cabeçalhos de slide |
| `colors.primaryDark` | `#0D1526` | Fundos escuros pontuais (blocos de código, rodapés de slide) |
| `colors.secondary` | `#3A6EA5` | Links, ícones ativos, botão secundário, `info` |
| `colors.accent` | `#D9A441` | Destaque único — métricas-chave, CTA, marcação de "atenção aqui". Usar com moderação; nunca como cor de fundo de grandes áreas |
| `colors.background` | `#F7F8FA` | Fundo padrão de página/slide (tema claro) |
| `colors.surface` | `#FFFFFF` | Cartões, tabelas, blocos elevados sobre o fundo |
| `colors.border` | `#E2E5EA` | Bordas, divisores, fundo de badge neutro |
| `colors.textPrimary` | `#1A1D23` | Texto principal sobre `background`/`surface` (contraste 15.9:1 / 16.9:1) |
| `colors.textSecondary` | `#5B6270` | Texto de apoio, legendas, metadados (contraste ≥5.7:1 sobre `background`/`surface`) |
| `colors.textInverse` | `#F7F8FA` | Texto sobre `primary`/`primaryDark` (contraste 15:1) |
| `colors.success` | `#166B44` | Estados de sucesso/positivo — texto/ícone sobre `background`/`surface`, ou fundo de badge com texto `textInverse` (contraste 6.1:1) |
| `colors.warning` | `#D9A441` | Estados de alerta — mesmo valor de `accent`, papel semântico distinto |
| `colors.error` | `#C24444` | Estados de erro/negativo |
| `colors.info` | `#3A6EA5` | Estados informativos — mesmo valor de `secondary` |

**Trio de camadas do Lakehouse** (uso restrito a diagramas de arquitetura Bronze/Silver/Gold, badges de camada e legendas de pipeline — não usar como paleta de UI geral):

| Token | Valor | Camada |
|---|---|---|
| `colors.layerBronze` | `#B08D57` | Bronze (dados brutos) |
| `colors.layerSilver` | `#A7B0B8` | Silver (dados limpos/conformados) |
| `colors.layerGold` | `#D9A441` | Gold (modelo estrela, consumo analítico) — mesmo valor de `accent`, reforça a leitura de "Gold = destaque" |

Regra fixa: ao representar as três camadas lado a lado (diagramas, legendas, badges), manter sempre a ordem Bronze → Silver → Gold e sempre com texto em `colors.textPrimary` sobre o preenchimento (contraste 5.5:1 a 7.7:1 verificado); não usar texto branco sobre essas cores.

## Typography

Família única (`Inter`) para toda a hierarquia de leitura, com `JetBrains Mono` reservado a código — coerente com o conteúdo do curso, que mistura prosa técnica e trechos de código/notebook.

| Token | Tamanho / peso / entrelinha | Uso |
|---|---|---|
| `typography.display` | 40px / 700 / 1.15 | Capa de slide, título de seção principal |
| `typography.h1` | 32px / 700 / 1.2 | Título de slide, título de notebook |
| `typography.h2` | 24px / 600 / 1.25 | Subtítulo de slide, seção de notebook |
| `typography.h3` | 19px / 600 / 1.3 | Subseção, rótulo de bloco/card |
| `typography.body` | 16px / 400 / 1.55 | Texto corrido |
| `typography.small` | 13px / 400 / 1.4 | Legendas, rodapés, metadados, fontes de dados |
| `typography.code` | 14px / 400 / 1.5 | Código inline e blocos de código, nomes de tabelas/colunas |

Fallback: se `Inter` não puder ser distribuída (ex.: ambiente sem acesso a Google Fonts), usar `system-ui`/`'Segoe UI'` conforme já declarado em `fontFamily`. Se `JetBrains Mono` não estiver disponível, usar `Fira Code` e, na ausência de ambas, `ui-monospace`.

## Layout

- Grade de espaçamento em base 8px (`spacing.xs` a `spacing.xxl`), com `spacing.md` (16px) como unidade de respiro padrão entre elementos de um mesmo bloco e `spacing.lg`/`spacing.xl` entre blocos distintos.
- Para slides em palco fixo 1920×1080 (padrão da skill `criar-slides-html`), tratar os valores de `spacing` como escaláveis proporcionalmente (ex.: `spacing.lg` vira a margem interna mínima de um card de conteúdo).
- Conteúdo textual em notebooks/handouts: largura de leitura confortável, sem coluna única forçada além do necessário — os notebooks já controlam isso via renderizador do Jupyter/Colab.
- Diagramas de arquitetura (Lakehouse, modelo estrela) fluem preferencialmente da esquerda para a direita ou de cima para baixo, refletindo o fluxo real Bronze → Silver → Gold.

## Elevation & Depth

Uso discreto de sombra — o material é predominantemente flat/técnico, elevação serve só para indicar hierarquia de cartões e nós de diagrama, não para efeito decorativo.

| Token | Valor | Uso |
|---|---|---|
| nível 0 | `none` | Elementos no mesmo plano do fundo (texto, ícones inline) |
| nível 1 | `0 1px 2px rgba(13, 21, 38, 0.06)` | Cards, nós de diagrama, tabelas — o nível padrão de `components.card` e `components.diagramNode` |
| nível 2 | `0 2px 8px rgba(13, 21, 38, 0.10)` | Elementos em foco/hover, modais leves |
| nível 3 | `0 8px 24px rgba(13, 21, 38, 0.14)` | Elementos flutuantes sobre conteúdo (tooltip, menu) |

Estes valores não são expressos como tokens de frontmatter porque a especificação alpha do `DESIGN.md` não reconhece um grupo `elevation` nem uma propriedade `boxShadow` em `components` — ficam registrados aqui como regra de prosa a ser aplicada em CSS pela ferramenta consumidora (ex.: `criar-slides-html`). Pelo mesmo motivo, bordas de 1px em `colors.border` (usadas em card, callout, diagram node e botão secundário) também são descritas em prosa, não como sub-token de componente.

## Shapes

- `rounded.sm` (4px): botões, badges retangulares, blocos de código.
- `rounded.md` (8px): cards, nós de diagrama, callouts — o raio padrão do sistema.
- `rounded.lg` (16px): blocos de destaque grandes (ex.: capa de slide).
- `rounded.pill` (999px): badges de status e tags de camada (Bronze/Silver/Gold).

## Components

- **Card** (`components.card`): contêiner padrão para agrupar conteúdo relacionado em slides e handouts. Fundo `surface`, texto `textPrimary`; adicionar borda 1px `colors.border` e sombra nível 1 (ver Elevation & Depth) no CSS consumidor.
- **Button primary/secondary** (`components.buttonPrimary`/`buttonSecondary`): primário para a ação/mensagem central do slide; secundário para ações de apoio. Nunca usar os dois lado a lado com o mesmo peso visual. `buttonSecondary` leva borda 1px `colors.primary`.
- **Badge** (`components.badge`): rótulo neutro curto (ex.: status genérico de tabela).
- **Badge de camada** (`components.badgeLayerBronze` / `badgeLayerSilver` / `badgeLayerGold`): variantes fixas do badge para identificar a camada Bronze, Silver ou Gold em diagramas e legendas — usar sempre com `textColor: colors.textPrimary`, nunca texto branco.
- **Code block** (`components.codeBlock`): trechos de código/PySpark/SQL extraídos dos notebooks. Fundo `primaryDark`, texto `textInverse`, tipografia `typography.code`.
- **Callout** (`components.callout`): observação, nota metodológica ou referência bibliográfica destacada do corpo do texto. Texto em `textSecondary` para reforçar que é conteúdo de apoio; adicionar borda 1px `colors.border` no CSS consumidor.
- **Diagram node** (`components.diagramNode`): unidade básica dos diagramas de arquitetura (uma tabela, uma camada, um serviço). Combinar com as variantes de badge de camada quando representar Bronze/Silver/Gold.
- **Metric highlight** (`components.metricHighlight`): destaque de uma métrica única em slide (ex.: "Turnover: 4.2%"). Usa `colors.accent` — por isso deve aparecer no máximo uma vez por tela.
- **Status badges** (`components.statusSuccess` / `statusWarning` / `statusError` / `statusInfo`): indicadores curtos de estado, úteis em telas sobre qualidade/carga de dados do pipeline (ex.: status de uma execução Bronze→Silver→Gold).

## Do's and Don'ts

- Usar `colors.accent`/`colors.layerGold` como destaque pontual (uma métrica, um CTA, a camada Gold em um diagrama) — não como cor de fundo extensa nem em múltiplos elementos na mesma tela.
- Manter o texto sobre `layerBronze`/`layerSilver`/`layerGold` sempre em `colors.textPrimary`; não usar texto branco sobre essas três cores.
- `colors.success` foi calibrado para funcionar tanto como texto/ícone sobre `background`/`surface` (contraste 6.1:1) quanto como fundo de badge com texto `textInverse` (contraste 6.1:1) — não é necessário reservá-lo a texto grande.
- Preservar a ordem Bronze → Silver → Gold sempre que as três cores de camada aparecerem juntas — inverter a ordem contradiz a arquitetura real do curso.
- Não introduzir uma segunda família de display/heading; toda a hierarquia tipográfica usa `Inter`, variando peso e tamanho, para manter o material coeso entre notebook, slide e diagrama.
- Não fabricar um logo ou wordmark estilizado a partir desta paleta sem validação — a pendência de identidade gráfica (logo/ícone) segue em aberto até material ser fornecido.
