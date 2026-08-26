# Projeto: Data Pipeline de Eventos de RH em Lakehouse (Arquitetura Medalhão)

## 1. Contexto

A área de Recursos Humanos da empresa precisa de uma base analítica confiável para acompanhar o histórico de eventos relacionados aos funcionários (admissões, promoções, transferências, desligamentos, mudanças salariais, avaliações, etc.), permitindo análises históricas consistentes mesmo quando atributos de dimensão (cargo, departamento, dados cadastrais do funcionário) mudam ao longo do tempo.

## 2. Objetivo do Projeto

Construir um **data pipeline em PySpark** que:

1. Recebe arquivos de origem (extraídos de sistemas de RH/HCM) via uma ferramenta de ingestão tipo **Fivetran** (ou similar), depositando-os em um **bucket S3**.
2. Processa esses dados através de um **Lakehouse com arquitetura medalhão** (Bronze → Silver → Gold).
3. Popula, na camada Gold, um **modelo estrela (star schema)** composto por:
   - **Tabela fato**: `fato_eventos_rh`
   - **Dimensão de Funcionários**: `dim_funcionario` (SCD Tipo 2)
   - **Dimensão de Departamento**: `dim_departamento` (SCD Tipo 2)
   - **Dimensão de Cargos**: `dim_cargo` (SCD Tipo 2)
   - **Dimensão de Tempo**: `dim_tempo` (estática/SCD Tipo 0)

## 3. Escopo

### 3.1 Dentro do escopo
- Pipeline de ingestão de arquivos (CSV/Parquet/JSON) do sistema de origem até o S3, via ferramenta de ELT (Fivetran ou equivalente open-source, ex.: Airbyte).
- Camada **Bronze**: ingestão raw, sem transformação, com metadados de auditoria (arquivo de origem, timestamp de ingestão, etc.).
- Camada **Silver**: limpeza, padronização, deduplicação, tipagem correta e enriquecimento leve dos dados.
- Camada **Gold**: modelagem dimensional (star schema), com lógica de **SCD Tipo 2** para as dimensões de funcionário, departamento e cargo.
- Orquestração do pipeline (ex.: Airflow, Databricks Workflows, ou similar) — ferramenta decidida na Fase 0, implementada na Fase 5.
- Testes de qualidade de dados e validações entre camadas.
- Documentação técnica e de negócio do modelo de dados.
- Criação de um **dashboard simples com as principais métricas de RH**, consumindo diretamente o modelo estrela da camada Gold (ver seção 5.6 e Fase 7).

### 3.2 Fora do escopo
- Construção de um BI corporativo completo ou de dashboards adicionais além do dashboard básico previsto na Fase 7 (aprofundamento analítico fica a cargo de outra frente).
- Implementação de sistemas de origem (assume-se que o sistema de RH já exporta arquivos).
- Governança de acesso/segurança avançada (mascaramento de PII pode ser mencionado como próximo passo, mas não é entregável obrigatório).

## 4. Arquitetura da Solução

```
[Sistema de RH / HCM]
        │  (export de arquivos: CSV/JSON)
        ▼
[Fivetran / ferramenta de ingestão similar]
        │
        ▼
[Amazon S3 - raw landing zone]
        │
        ▼
┌─────────────────────────────────────────────┐
│              LAKEHOUSE (Medalhão)            │
│                                               │
│  BRONZE  →  SILVER  →  GOLD (Star Schema)    │
│  (raw)      (limpo)     (fato + dimensões)   │
└─────────────────────────────────────────────┘
        │
        ▼
[Dashboard de Métricas de RH] ── [Consumo: BI / Analytics / Data Science]
```

### 4.1 Camada Bronze
- Armazena os dados **exatamente como recebidos** dos arquivos de origem.
- Adiciona colunas técnicas de auditoria: `_ingestion_timestamp`, `_source_file`, `_batch_id`.
- Sem deduplicação ou transformação de schema além do necessário para leitura (schema-on-read permissivo).
- Formato recomendado: Parquet ou Delta Lake, particionado por data de ingestão.

### 4.2 Camada Silver
- Aplica limpeza: tratamento de nulos, tipos de dados corretos, padronização de strings (trim, case), remoção de duplicatas.
- Validações de qualidade (ex.: chaves obrigatórias não nulas, datas válidas, domínios de valores esperados).
- Dados organizados em tabelas por entidade de negócio (funcionários, cargos, departamentos, eventos), ainda no grão original da fonte, mas já conformados/tipados.
- Pode conter pequenas junções/enriquecimentos que não envolvam ainda a lógica dimensional (SCD).
- **Modo de extração por entidade** (premissa a validar com a fonte real, ver seção 9):
  - **Dados mestres** (funcionários, cargos, departamentos): tratados como **snapshot completo** a cada carga. A camada Silver compara o snapshot atual com o último estado vigente para detectar alterações (input da lógica SCD2 da Gold).
  - **Eventos**: tratados como **incremental/append-only** — cada `evento_id` é imutável e chega uma única vez. A deduplicação na Silver usa `evento_id` como chave de idempotência.

### 4.3 Camada Gold
- Modelo dimensional **estrela**, otimizado para consultas analíticas.
- Implementação de **SCD Tipo 2** nas dimensões de funcionário, cargo e departamento, com colunas de controle:
  - `sk_<dimensao>` (surrogate key, chave técnica)
  - `<chave_natural>_id` (chave de negócio)
  - `data_inicio_validade`
  - `data_fim_validade`
  - `flag_atual` (booleano)
  - `versao` (opcional, número de versão do registro)
- A **dimensão de tempo** é estática (calendário), gerada uma única vez (ou reprocessada integralmente), sem histórico de mudanças (SCD Tipo 0/1 — não se aplica SCD2).

**Geração de surrogate key:** a SK deve ser **determinística** (ex.: hash `sha2(chave_natural || data_inicio_validade)`), nunca gerada via `monotonically_increasing_id()` ou equivalente — em Spark distribuído esses valores não são estáveis entre reprocessamentos, o que quebraria a idempotência exigida na seção 6.

**Convenção de intervalo de validade:** `data_inicio_validade` é **inclusiva** e `data_fim_validade` é **exclusiva** — intervalo `[data_inicio_validade, data_fim_validade)`. O registro vigente usa `data_fim_validade = '9999-12-31'`. Todo lookup temporal (ex.: FK da fato) deve usar essa convenção para evitar erro de borda (off-by-one) na data exata de uma mudança.

**Tipo 1 vs. Tipo 2 por atributo:** nem todo atributo de uma dimensão versionada deve disparar nova versão. Atributos classificados como **Tipo 1** são sobrescritos in-place (sem gerar histórico); atributos **Tipo 2** disparam fechamento da versão anterior e abertura de uma nova. A classificação de cada atributo está detalhada nas seções 5.2–5.4.

## 5. Modelo de Dados (Camada Gold)

### 5.1 `dim_tempo`
Grão: um dia por linha.

| Coluna | Descrição |
|---|---|
| `sk_tempo` | Chave substituta (ex.: `AAAAMMDD` como inteiro) |
| `data` | Data completa |
| `ano` | Ano |
| `mes` | Mês |
| `dia` | Dia |
| `trimestre` | Trimestre |
| `dia_semana` | Nome do dia da semana |
| `nome_mes` | Nome do mês |
| `flag_dia_util` | Indicador de dia útil |

### 5.2 `dim_funcionario` (SCD Tipo 2)
Grão: um registro por versão histórica do funcionário.

| Coluna | Descrição | Tipo SCD |
|---|---|---|
| `sk_funcionario` | Chave substituta | — |
| `funcionario_id` | Chave natural (ID do funcionário no sistema de origem) | — |
| `nome` | Nome completo | Tipo 2 (mudança de nome é um evento relevante, ex.: casamento) |
| `data_nascimento` | Data de nascimento | Tipo 1 (correção cadastral, não gera histórico) |
| `genero` | Gênero | Tipo 1 |
| `email` | E-mail corporativo | Tipo 1 |
| `data_admissao` | Data de admissão | — (imutável na origem) |
| `status` | Ativo/Inativo | Tipo 2 (crítico para cálculo de headcount por data) |
| `data_inicio_validade` | Início da validade do registro | — |
| `data_fim_validade` | Fim da validade do registro (null/9999-12-31 se atual) | — |
| `flag_atual` | Indica versão vigente | — |

### 5.3 `dim_departamento` (SCD Tipo 2)
Grão: um registro por versão histórica do departamento.

| Coluna | Descrição | Tipo SCD |
|---|---|---|
| `sk_departamento` | Chave substituta | — |
| `departamento_id` | Chave natural | — |
| `nome_departamento` | Nome do departamento | Tipo 2 |
| `centro_custo` | Centro de custo | Tipo 2 |
| `departamento_pai_id` | **Chave natural** (`departamento_id`) do departamento hierarquicamente superior (opcional) | Tipo 2 |
| `data_inicio_validade` | Início da validade | — |
| `data_fim_validade` | Fim da validade | — |
| `flag_atual` | Indica versão vigente | — |

> **Nota sobre hierarquia versionada:** `departamento_pai_id` armazena a **chave natural** do pai, não a `sk_departamento`. Isso evita que a referência fique "presa" a uma versão específica do pai que pode não estar mais vigente. Para navegar a hierarquia em uma data histórica, resolver a `sk_departamento` do pai vigente naquela data via o mesmo padrão de lookup temporal usado na tabela fato (seção 5.5), e não por join direto de SK.

### 5.4 `dim_cargo` (SCD Tipo 2)
Grão: um registro por versão histórica do cargo.

| Coluna | Descrição | Tipo SCD |
|---|---|---|
| `sk_cargo` | Chave substituta | — |
| `cargo_id` | Chave natural | — |
| `nome_cargo` | Título do cargo | Tipo 2 |
| `nivel` | Nível/senioridade | Tipo 2 |
| `faixa_salarial_min` | Faixa salarial mínima | Tipo 1 (revisão de mercado não representa mudança do cargo em si) |
| `faixa_salarial_max` | Faixa salarial máxima | Tipo 1 |
| `data_inicio_validade` | Início da validade | — |
| `data_fim_validade` | Fim da validade | — |
| `flag_atual` | Indica versão vigente | — |

### 5.5 `fato_eventos_rh`
Grão: um evento de RH por funcionário (ex.: admissão, promoção, transferência, mudança salarial, avaliação, desligamento).

| Coluna | Descrição |
|---|---|
| `sk_evento` | Chave substituta do evento |
| `evento_id` | Chave natural do evento (origem) |
| `sk_tempo` | FK para `dim_tempo` (data do evento) |
| `sk_funcionario` | FK para a versão vigente de `dim_funcionario` na data do evento |
| `sk_departamento` | FK para a versão vigente de `dim_departamento` na data do evento |
| `sk_cargo` | FK para a versão vigente de `dim_cargo` na data do evento |
| `tipo_evento` | Admissão / Promoção / Transferência / Desligamento / Alteração Salarial / Avaliação |
| `salario_anterior` | Salário antes do evento (aplicável a Alteração Salarial e Promoção; nulo caso contrário) |
| `salario_novo` | Salário após o evento (aplicável a Alteração Salarial, Promoção e Admissão; nulo caso contrário) |
| `motivo` | Motivo/observação do evento (quando aplicável) |

> **Nota sobre chaveamento SCD2 na fato:** as FKs da tabela fato devem apontar para a **surrogate key vigente na data do evento** (lookup pela data, não necessariamente `flag_atual = true`), garantindo que análises históricas reflitam o estado do funcionário/cargo/departamento no momento em que o evento ocorreu.

> **Nota sobre membros desconhecidos (late-arriving facts):** se um evento chegar referenciando uma chave natural (`funcionario_id`, `departamento_id` ou `cargo_id`) ainda não presente na dimensão correspondente na data do evento, a FK deve apontar para um registro **"unknown member"** reservado (ex.: `sk_funcionario = -1`) em vez de falhar a carga ou descartar o evento. O evento deve ser reprocessado/corrigido quando a dimensão for atualizada.

### 5.6 Métricas do Dashboard de RH

O dashboard consumirá diretamente o modelo estrela da camada Gold (`fato_eventos_rh` + dimensões). As 5 métricas selecionadas são:

| # | Métrica | Descrição | Fonte / Cálculo |
|---|---|---|---|
| 1 | **Headcount** | Número de funcionários ativos em um determinado período/data | Contagem de `dim_funcionario` com `status = Ativo` na versão vigente na data de referência (via `data_admissao` e ausência de evento de desligamento até a data) |
| 2 | **Taxa de Turnover (Rotatividade)** | % de funcionários desligados em relação ao headcount médio do período | `COUNT(eventos com tipo_evento = 'Desligamento' no período) / AVG(headcount do período)` |
| 3 | **Tempo Médio de Casa (Tenure)** | Tempo médio, em meses/anos, entre a admissão e o desligamento (ou data atual, para ativos) | `AVG(data_desligamento OU data_atual − data_admissao)` a partir de `dim_funcionario` / eventos de admissão e desligamento |
| 4 | **Taxa de Promoção** | % de funcionários que tiveram ao menos um evento de promoção no período, em relação ao headcount do período | `COUNT(DISTINCT funcionario_id com tipo_evento = 'Promoção' no período) / headcount do período` |
| 5 | **Headcount por Departamento** | Distribuição do número de funcionários ativos por departamento (permite ranking e comparação entre áreas) | Contagem de `dim_funcionario` ativos agrupada por `sk_departamento` vigente na data de referência |

> Todas as métricas devem ser calculáveis com granularidade temporal (ex.: por mês/trimestre/ano), aproveitando `dim_tempo` e o histórico SCD2 das dimensões para refletir corretamente o estado organizacional em cada ponto do tempo.

## 6. Requisitos Técnicos

- **Linguagem**: Python
- **Engine de processamento**: PySpark (Spark DataFrame API)
- **Armazenamento**: Amazon S3 (data lake), formato Delta Lake ou Parquet para as camadas Bronze/Silver/Gold
- **Ingestão**: Fivetran ou ferramenta ELT similar, entregando arquivos no bucket S3 (landing zone)
- **Modelagem**: Star schema com SCD Tipo 2 (exceto `dim_tempo`)
- **Idempotência**: o pipeline deve poder ser reexecutado sem duplicar dados (merge/upsert idempotente, especialmente na lógica de SCD2)
- **Particionamento**: recomenda-se particionar tabelas grandes por data de evento/ingestão para performance

## 7. Fases do Projeto e Entregáveis

### Fase 0 — Planejamento e Setup do Ambiente
**Objetivo:** preparar infraestrutura e definir contratos de dados.

**Entregáveis:**
- Definição da estrutura de buckets S3 (`raw/bronze`, `silver`, `gold`) e convenção de nomenclatura/particionamento.
- Configuração da ferramenta de ingestão (Fivetran ou similar) apontando para o bucket S3.
- Definição do layout/esquema dos arquivos de origem (dicionário de dados: funcionários, cargos, departamentos, eventos).
- **Decisão antecipada de plataforma e ferramentas** (movida para esta fase para reduzir risco de bloqueio nas Fases 1, 5 e 7): plataforma de execução Spark (local/Databricks/EMR/Glue) e ferramenta de orquestração (Airflow, Databricks Workflows, ou similar).
- **Definição do modo de extração por entidade**: snapshot completo (dados mestres) vs. incremental/append-only (eventos) — ver seção 4.2 — documentando o impacto na lógica de comparação SCD2.
- Setup do ambiente de desenvolvimento PySpark (na plataforma decidida acima).
- Repositório de código estruturado (ex.: `src/bronze`, `src/silver`, `src/gold`, `tests/`).

---

### Fase 1 — Ingestão e Camada Bronze
**Objetivo:** trazer os dados brutos da origem para o Lakehouse sem perda de informação.

**Entregáveis:**
- Pipeline de ingestão configurado (Fivetran/similar → S3 raw zone).
- Job PySpark que lê os arquivos da raw zone e grava na camada Bronze, adicionando colunas de auditoria (`_ingestion_timestamp`, `_source_file`, `_batch_id`).
- Estratégia de particionamento definida (ex.: por data de ingestão).
- Testes básicos de leitura/gravação (schema esperado, contagem de registros).

---

### Fase 2 — Camada Silver (Limpeza e Padronização)
**Objetivo:** transformar os dados brutos em dados confiáveis e padronizados.

**Entregáveis:**
- Jobs PySpark de limpeza para cada entidade (funcionários, cargos, departamentos, eventos): tipagem, tratamento de nulos, remoção de duplicatas, padronização de texto/datas.
- Validações de qualidade de dados (ex.: com Great Expectations, Pandera, ou validações customizadas em PySpark) com relatório de rejeições/anomalias.
- Tabelas Silver publicadas (uma por entidade de negócio).
- Testes unitários das funções de transformação.

---

### Fase 3 — Camada Gold: Dimensões (SCD Tipo 2 e Dimensão de Tempo)
**Objetivo:** construir as dimensões do modelo estrela com controle histórico.

**Entregáveis:**
- Job PySpark de geração/atualização de `dim_tempo` (calendário estático).
- Framework/função reutilizável de **merge SCD Tipo 2** (comparação de atributos, fechamento de versão anterior, abertura de nova versão, geração de surrogate key).
- Jobs PySpark para `dim_funcionario`, `dim_departamento` e `dim_cargo` aplicando a lógica SCD2 a partir da camada Silver.
- Testes validando cenários de SCD2: inserção de novo registro, atualização de atributo (nova versão), ausência de mudança (sem duplicação), fechamento correto de `data_fim_validade`/`flag_atual`.

---

### Fase 4 — Camada Gold: Tabela Fato
**Objetivo:** construir a tabela fato de eventos de RH, integrada às dimensões.

**Entregáveis:**
- Job PySpark que lê os eventos da camada Silver e realiza o **lookup temporal** das surrogate keys corretas em cada dimensão (versão vigente na data do evento).
- Tabela `fato_eventos_rh` publicada na camada Gold.
- Testes de integridade referencial (todas as FKs da fato existem nas dimensões) e de grão (sem duplicidade de eventos).
- Testes de idempotência (reprocessamento não duplica fatos).

---

### Fase 5 — Orquestração, Qualidade e Automação
**Objetivo:** tornar o pipeline executável de ponta a ponta de forma confiável e agendada.

**Entregáveis:**
- Orquestração dos jobs (usando a ferramenta decidida na Fase 0) cobrindo Bronze → Silver → Gold.
- Monitoramento e alertas básicos de falhas de pipeline.
- Testes de qualidade de dados automatizados incorporados ao fluxo (quality gates entre camadas).
- Logs e métricas de execução (volumetria por camada, tempo de execução).

---

### Fase 6 — Documentação e Entrega Final
**Objetivo:** consolidar o projeto e habilitar o consumo pelos times de análise.

**Entregáveis:**
- Documentação técnica da arquitetura (diagramas de fluxo, descrição de cada camada).
- Dicionário de dados completo do modelo Gold (fato + dimensões).
- Documentação da lógica de SCD Tipo 2 aplicada.
- Guia de execução do pipeline (setup, execução manual, execução orquestrada).
- Apresentação/demo final dos dados no modelo estrela (consulta de exemplo respondendo a uma pergunta de negócio, ex.: "headcount por departamento ao longo do tempo").

### Fase 7 — Dashboard de Métricas de RH
**Objetivo:** disponibilizar uma visualização simples e direta das principais métricas de RH para consumo pelos stakeholders.

**Entregáveis:**
- Definição da ferramenta de dashboard (ex.: Streamlit, Metabase, Power BI, Tableau ou similar — a definir conforme stack disponível).
- Conexão do dashboard à camada Gold do Lakehouse.
- Implementação das 5 métricas definidas na seção 5.6: Headcount, Taxa de Turnover, Tempo Médio de Casa (Tenure), Taxa de Promoção e Headcount por Departamento.
- Filtros básicos por período (mês/trimestre/ano) e por departamento.
- Validação dos números do dashboard contra consultas de referência feitas diretamente no modelo Gold (conferência manual).

---

## 8. Critérios de Sucesso

- Pipeline executa de ponta a ponta (ingestão → Bronze → Silver → Gold) sem intervenção manual.
- Dimensões refletem corretamente o histórico de mudanças (SCD2 validado com casos de teste).
- Tabela fato permite reconstruir o estado organizacional (cargo/departamento/dados do funcionário) válido em qualquer data histórica de evento.
- Pipeline é idempotente e reprocessável sem gerar duplicidade ou inconsistência.
- Documentação permite que outro desenvolvedor entenda e opere o pipeline sem suporte direto do autor original.
- Dashboard exibe corretamente as 5 métricas de RH definidas, com valores consistentes com o modelo Gold e filtros funcionais por período e departamento.

## 9. Premissas e Riscos

### 9.1 Premissas a validar com a fonte real
- O sistema de RH/HCM exporta `funcionario_id`, `departamento_id` e `cargo_id` de forma estável e consistente entre cargas (chave natural nunca muda de significado).
- Dados mestres (funcionários, cargos, departamentos) chegam como **snapshot completo** a cada carga; eventos chegam de forma **incremental/append-only** e são imutáveis após criados (ver seção 4.2). Caso a fonte real se comporte de outra forma, a lógica de comparação SCD2 e a estratégia de deduplicação precisam ser revistas.
- `evento_id` é único e estável na origem (base da deduplicação idempotente da fato).

### 9.2 Dados sensíveis (PII / LGPD)
O modelo contém dados pessoais sensíveis (`nome`, `data_nascimento`, `email`, `salario_anterior`/`salario_novo`). Mesmo que o mascaramento completo de PII esteja fora do escopo obrigatório (seção 3.2), o projeto deve, no mínimo:
- Restringir acesso à camada Gold (e especialmente às colunas de salário e dados cadastrais) por controle de permissão do lakehouse/catálogo.
- Documentar quais campos são pessoais, para viabilizar mascaramento ou anonimização como próximo passo, em conformidade com a LGPD.

### 9.3 Decisões técnicas pendentes (a fechar na Fase 0)
- Plataforma de execução Spark (local / Databricks / EMR / Glue).
- Ferramenta de orquestração (Airflow, Databricks Workflows, ou similar).
- Ferramenta de dashboard (Fase 7): Streamlit, Metabase, Power BI, Tableau ou similar, conforme stack disponível.

### 9.4 Riscos conhecidos
- Mudança no layout dos arquivos de origem sem aviso prévio pode quebrar a leitura na Bronze (mitigar com schema esperado explícito e validação na Fase 0/2).
- Sem SK determinística (seção 4.3), reprocessamentos podem gerar duplicidade de versões nas dimensões.
- Eventos que chegam antes da respectiva dimensão estar atualizada (late-arriving facts) exigem o tratamento de "unknown member" descrito na seção 5.5.
