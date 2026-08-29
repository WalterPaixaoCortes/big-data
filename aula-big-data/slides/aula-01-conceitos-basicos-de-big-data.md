# Roteiro — Conceitos Básicos de Big Data (Aula 01)

Contexto: aula ao vivo guiada pelo instrutor. Densidade baixa — os slides são apoio visual para a exposição falada, não um substituto do notebook. Fonte: `aula-big-data/aula-01-conceitos-basicos-de-big-data.ipynb`.

---

## 1. Abertura
- **Título:** Conceitos Básicos de Big Data
- **Subtítulo:** Big Data não é sobre o tamanho do dado — é sobre o limite das suas ferramentas
- **Visual:** slide de capa, sem elementos adicionais além do título/subtítulo.
- **Nota do apresentador:** —

## 2. O modismo por trás do termo
- **Título:** Um termo citado — e mal definido
- **Bullets finais:**
  - "Muitos dados"? "Spark e Hadoop"? "Jargão de marketing"?
  - O objetivo desta aula: sair do modismo, chegar a critérios objetivos
- **Visual:** texto centralizado, sem imagem — slide de contexto/gancho (Ethos).
- **Nota:** reforçar oralmente que a aula não vai cobrir implementação de nenhuma ferramenta específica, só vocabulário e critérios.

## 3. Big Data, afinal
- **Título:** Não é sobre o tamanho do dado
- **Subtítulo (frase de destaque):** É sobre o limite das suas ferramentas.
- **Visual:** citação em destaque (quote/callout grande), tom de definição-chave da aula.
- **Nota:** contextualizar o cenário "clássico" antes: um arquivo, um programa, uma máquina, cabendo na RAM (ex.: Pandas).

## 4. Os três limites
- **Título:** Quando as ferramentas tradicionais param de funcionar
- **Bullets finais:**
  - Volume — não cabe na memória de uma máquina
  - Velocidade — dados chegam mais rápido do que dá para processar
  - Variedade — formatos e fontes demais para um modelo único de tabela
- **Visual:** três cards lado a lado (grid 3 colunas).
- **Nota:** perguntar à turma: "os seus dados cabem confortavelmente na memória da sua máquina?" — se sim, provavelmente não precisa de Big Data.

## 5. Um problema mais antigo que o termo
- **Título:** "Tidal wave of data" — 1999, dez anos antes do termo pegar
- **Subtítulo:** Nature, 1999 (Reichhardt) — genômica e astronomia já enfrentavam o mesmo problema
- **Visual:** citação/destaque editorial, tom histórico (Pathos), sem imagem real da revista (não copiar asset de terceiros).
- **Nota:** o vocabulário mudou ("maré de dados" → "Big Data"), o diagnóstico é o mesmo.

## 6. Os 5 V's do Big Data
- **Título:** Os 5 V's do Big Data
- **Subtítulo:** 3 V's originais (Doug Laney, 2001) + 2 incorporados depois pelo mercado
- **Bullets finais (grid de 5):**
  - Volume — quantidade total de dados
  - Velocidade — frequência de chegada
  - Variedade — formatos e estruturas diferentes
  - Veracidade — confiabilidade e qualidade
  - Valor — só se justifica se gerar decisão
- **Visual:** grid/cards de 5 itens.
- **Nota:** deixar claro que Volume/Velocidade/Variedade são os originais de 2001 (META Group/Gartner); Veracidade e Valor vieram depois, via IBM e mercado. Mencionar rapidamente que existem 6º/7º V's (Variabilidade, Visualização) dependendo da fonte, mas os 5 já bastam.

## 7. Mão na massa: crescimento da base
- **Título:** Colocando a mão na massa
- **Subtítulo:** Medindo o crescimento da base de funcionários, mês a mês
- **Visual:** gráfico de linha (recriar a partir dos dados reais do notebook: 12 pontos, de 150 em 2025-09 a 219 em 2026-08) — regenerar como gráfico próprio do deck, não capturar screenshot do notebook.
- **Nota:** dado real do repositório (`data/landing/funcionarios/`), particionado por `dt=AAAA-MM-DD`.

## 8. A armadilha da duplicidade
- **Título:** Nem toda linha é um funcionário novo
- **Bullets finais:**
  - 2.224 linhas somando todas as partições
  - 219 funcionários únicos
  - Cada partição é uma extração completa — não só os novos do mês
- **Visual:** dois números grandes em destaque (comparação lado a lado / stat cards).
- **Nota:** gancho para Slowly Changing Dimensions, que será retomado na seção de modelagem. Mencionar que em escala real (500 mil funcionários, 10 anos) isso vira um problema de Big Data de verdade.

## 9. Quando Pandas (e Excel) não bastam mais
- **Título:** Três sinais de que chegou a hora
- **Bullets finais:**
  - Os dados não cabem na memória de uma máquina
  - O tempo de processamento é inviável
  - Os dados estão espalhados em múltiplas fontes
- **Visual:** lista numerada / 3 cards.
- **Nota:** reforçar que ferramentas de Big Data funcionam bem com dados pequenos também — a diferença é que continuam funcionando quando os dados crescem.

## 10. O ecossistema de Big Data
- **Título:** Quatro peças que resolvem o problema
- **Bullets finais:** Armazenamento distribuído · Processamento distribuído · Arquitetura em camadas · Orquestração
- **Visual:** diagrama de fluxo (baseado no mermaid do notebook): Armazenamento → Processamento → Camadas, com Orquestração coordenando as três.
- **Nota:** slide-mapa da seção — cada peça vira um slide próprio a seguir.

## 11. Armazenamento distribuído — GFS
- **Título:** Armazenamento Distribuído
- **Subtítulo:** Google File System (Ghemawat, Gobioff & Leung, SOSP '03, 2003)
- **Bullets finais:**
  - Arquivo dividido em chunks de 64 MB
  - Cada chunk replicado em 3 máquinas
  - Master guarda só os metadados de localização
- **Visual:** diagrama (arquivo → chunks → 3 chunkservers + master), baseado no mermaid do notebook.
- **Nota:** ideia central do paper — assumir que componentes vão falhar o tempo todo é parte do design, não exceção. Amazon S3 como exemplo real equivalente.

## 12. Processamento distribuído — MapReduce e Spark
- **Título:** Processamento Distribuído
- **Subtítulo:** MapReduce (Dean & Ghemawat, OSDI '04) → Apache Spark (Zaharia et al., NSDI '12)
- **Bullets finais:**
  - Map: processa cada registro, gera pares chave/valor
  - Shuffle: agrupa por chave
  - Reduce: combina os valores de cada chave
- **Visual:** diagrama de fluxo map → shuffle → reduce, baseado no mermaid do notebook.
- **Nota:** Spark resolveu a limitação de gravar em disco entre etapas com RDDs em memória — ganho relatado de ~10x em cargas iterativas, mantendo tolerância a falhas via lineage.

## 13. Arquitetura Lakehouse e camadas Medalhão
- **Título:** Arquitetura Lakehouse e Camadas Medalhão
- **Subtítulo:** Armbrust, Ghodsi, Xin & Zaharia — CIDR '21
- **Bullets finais:**
  - Bronze — dados crus + metadados de auditoria
  - Silver — limpo, deduplicado, tipado
  - Gold — modelado para consumo analítico
- **Visual:** diagrama de fluxo Landing → Bronze → Silver → Gold → Dashboards, com as cores de camada do DESIGN.md (badges Bronze/Silver/Gold).
- **Nota:** Lakehouse resolve os 4 problemas do modelo "lake + warehouse": confiabilidade, desatualização, analytics avançado limitado, custo duplicado. Estatística: 86% dos analistas usam dados desatualizados (citada no paper).

## 14. Orquestração
- **Título:** Orquestração
- **Subtítulo:** Apache Airflow (Beauchemin, Airbnb Engineering, 2015) — pipelines como DAGs
- **Visual:** diagrama do DAG do notebook: `Bronze: funcionarios` → `Silver: dim_funcionario` e `Bronze: eventos` → `Silver: eventos`, convergindo em `Gold: fato_eventos_rh`.
- **Nota:** DAG = grafo acíclico dirigido; garante, por exemplo, que Silver só comece depois que Bronze terminar com sucesso. Esse DAG específico antecipa o projeto aplicado do curso.

## 15. Transição: da camada Gold ao modelo de dados
- **Título:** "Modelado para consumo analítico" — o que isso quer dizer?
- **Subtítulo:** Modelagem dimensional: tanta teoria (e história) quanto o próprio Big Data
- **Visual:** slide de transição/section-mark, texto centralizado.
- **Nota:** marca a virada de assunto (ecossistema → modelagem), reduz a chance de a turma achar que already terminou a aula.

## 16. OLTP vs. OLAP
- **Título:** Dois mundos com objetivos diferentes
- **Visual:** comparação lado a lado (duas colunas).
  - Coluna 1 — OLTP: muitas transações pequenas e simultâneas; modelo relacional normalizado (Codd, 1970); ótimo para escrita.
  - Coluna 2 — OLAP: poucas consultas, porém pesadas, sobre histórico; dados desnormalizados de propósito; papel da camada Gold.
- **Nota:** normalização é ótima para escrita, cara para leitura analítica (pergunta simples pode exigir juntar dezenas de tabelas).

## 17. Os quatro tipos de analytics
- **Título:** Antes de modelar: para que serve o modelo?
- **Subtítulo:** Delen & Demirkan (2013) — escada de complexidade e valor crescentes
- **Bullets finais:**
  - Descritiva — "O que aconteceu?"
  - Diagnóstica — "Por que aconteceu?"
  - Preditiva — "O que vai acontecer?"
  - Prescritiva — "O que devemos fazer?"
- **Visual:** diagrama de progressão horizontal (4 estágios), baseado no mermaid do notebook.
- **Nota:** não é hierarquia de "melhor" — a maioria das organizações usa os quatro o tempo todo. O modelo dimensional que vem a seguir viabiliza os quatro a partir do mesmo conjunto de tabelas.

## 18. Fatos e dimensões
- **Título:** O Modelo Dimensional: Fatos e Dimensões
- **Subtítulo:** Ralph Kimball — medições numéricas cercadas de contexto descritivo
- **Bullets finais:**
  - Fato — medições (quantidade, valor, duração) + chaves para as dimensões
  - Dimensão — o "quem", "o quê", "onde", "quando" de cada medição
- **Visual:** diagrama de esquema estrela (fato central + 4 dimensões ao redor), baseado no erDiagram do notebook (fato de vendas: produto, cliente, loja, data).
- **Nota:** o desenho lembra uma estrela → star schema. Quando dimensões também são normalizadas, vira snowflake schema.

## 19. O grão (grain)
- **Título:** Antes de desenhar a fato: declare o grão
- **Subtítulo:** Kimball, "Keep to the Grain in Dimensional Modeling" (2007)
- **Visual:** citação em destaque — "o que, exatamente, representa uma linha da tabela?"
- **Nota:** o grão deve partir do nível mais atômico possível, determinado pela realidade física da coleta na origem — não pelas perguntas de negócio de hoje. Mencionar rapidamente o debate Inmon (top-down) vs. Kimball (bottom-up) como nota de rodapé, sem aprofundar.

## 20. Três tipos de tabela fato
- **Título:** Nem toda fato guarda o mesmo tipo de medição
- **Bullets finais:**
  - Transação — uma linha por evento (ex.: admissão, promoção, desligamento)
  - Snapshot periódico — uma linha por período (ex.: headcount mensal por departamento)
  - Snapshot cumulativo — uma linha por processo, atualizada a cada etapa
- **Visual:** 3 cards lado a lado.
- **Nota:** as extrações mensais de `funcionarios`/`departamentos` da aula têm cara de snapshot periódico — mas na Gold viram matéria-prima de dimensão, não de fato. A fronteira fato/dimensão depende da pergunta de negócio.

## 21. Outros tipos de dimensão
- **Título:** Além da estrela básica
- **Bullets finais:**
  - Degenerada — identificador sem tabela própria (ex.: número de pedido)
  - Conformada — mesma dimensão reutilizada por várias fatos
  - Junk — vários indicadores de baixa cardinalidade agrupados
  - Role-playing — mesma dimensão física, papéis diferentes (ex.: data do pedido / data de entrega)
- **Visual:** grid 2x2 de cards.
- **Nota:** todas continuam a mesma regra de ouro — fato mede, dimensão descreve.

## 22. Slowly Changing Dimensions
- **Título:** Modelando mudanças ao longo do tempo
- **Subtítulo:** Retomando a duplicidade que vimos na prática (slide 8)
- **Visual:** comparação lado a lado.
  - Tipo 1 — sobrescreve o valor antigo; simples, mas perde histórico
  - Tipo 2 — insere nova linha com surrogate key, `data_inicio_vigencia`/`data_fim_vigencia`/`is_current`; preserva histórico completo
- **Nota:** mencionar de passagem que existem Tipos 0, 3 e 4–7 (mais avançados), mas Tipo 1 e Tipo 2 cobrem a grande maioria dos casos reais.

## 23. Batch vs. Streaming
- **Título:** Batch vs. Streaming
- **Bullets finais:**
  - Batch — dados acumulados por um período, processados de uma vez (o caso desta aula: extrações mensais)
  - Streaming — cada evento processado assim que chega, latência de segundos ou menos
- **Visual:** diagrama comparativo (baseado no mermaid do notebook: eventos acumulando em buffer vs. eventos processados na hora).
- **Nota:** não são mutuamente exclusivos — arquiteturas modernas combinam os dois. O Dataflow Model (Akidau et al., 2015) trata batch como caso particular de streaming.

## 24. Fechamento
- **Título:** O que você leva desta aula
- **Bullets finais:**
  - Critérios objetivos para reconhecer um problema de Big Data (volume, velocidade, variedade além do limite de uma máquina)
  - As quatro peças do ecossistema: armazenamento, processamento, camadas, orquestração
  - Os fundamentos que sustentam a camada Gold: OLTP vs. OLAP, fato/dimensão, grão, SCD
  - Os quatro tipos de analytics e a distinção batch vs. streaming
- **Visual:** slide de encerramento, sem imagem adicional.
- **Nota:** gancho para a próxima aula/notebook: a demonstração prática (`demonstracao-lakehouse-medalhao.ipynb`), que implementa esse mesmo vocabulário em código.

## 25. Para se aprofundar
- **Título:** Para se aprofundar
- **Subtítulo:** As fontes originais por trás de cada conceito desta aula
- **Bullets finais (seleção dos mais citados em aula, não a lista completa de 15 papers):**
  - Codd (1970) — A Relational Model of Data for Large Shared Data Banks
  - Ghemawat, Gobioff & Leung (2003) — The Google File System
  - Dean & Ghemawat (2004) — MapReduce
  - Zaharia et al. (2012) — Resilient Distributed Datasets (Spark)
  - Armbrust et al. (2021) — Lakehouse (CIDR '21)
  - Kimball Group — Fact Tables and Dimension Tables, Slowly Changing Dimensions
- **Visual:** lista simples, tipografia menor (`typography.small`), sem grid decorativo — é slide de referência, não de destaque.
- **Nota:** mencionar oralmente que a lista completa (15 referências, em ordem cronológica) está no notebook, seção "Os Artigos Originais, Reunidos", e que basta ler o abstract de cada uma para acompanhar a aula. Não incluir URLs no slide (ilegíveis em projeção) — indicar que os links estão no notebook.

---

## Fora do escopo deste roteiro

- Diagramas mermaid do notebook são recriados como diagramas nativos do deck (SVG/HTML), não incorporados como imagem — para acompanhar a paleta do `DESIGN.md` e permitir animação/entrada progressiva se necessário.
