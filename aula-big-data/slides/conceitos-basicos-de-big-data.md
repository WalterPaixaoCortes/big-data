# Roteiro — Conceitos Básicos de Big Data (Aula 01)

Contexto: aula ao vivo guiada pelo instrutor. Densidade baixa — os slides são apoio visual para a exposição falada, não um substituto do notebook. Fonte: `aula-big-data/conceitos-basicos-de-big-data.ipynb`.

---

## 1. Abertura
- **Título:** Conceitos Básicos de Big Data
- **Subtítulo:** Big Data não é sobre o tamanho do dado — é sobre o limite das suas ferramentas
- **Visual:** slide de capa, sem elementos adicionais além do título/subtítulo.
- **Nota do apresentador:** —

## 2. Agenda
- **Título:** O caminho desta aula
- **Bullets finais (lista numerada):**
  - Big Data: além do modismo
  - O ecossistema que resolve o problema
  - Fundamentos de modelagem dimensional
  - Fechamento e onde se aprofundar
- **Visual:** lista de agenda (`.agenda-list`), quatro itens numerados; link discreto no rodapé para `github.com/WalterPaixaoCortes/big-data`.
- **Nota:** mapa da aula em um slide — cada item corresponde a um bloco macro do roteiro abaixo. Link do repositório repetido aqui como preview do que vem no slide de fechamento.

## 3. O modismo por trás do termo
- **Título:** Big Data: além do modismo
- **Subtítulo:** Um termo citado — e mal definido
- **Bullets finais:**
  - "Muitos dados"? "Spark e Hadoop"? "Jargão de marketing"?
  - O objetivo desta aula: sair do modismo, chegar a critérios objetivos
- **Visual:** texto centralizado, sem imagem — slide de contexto/gancho (Ethos).
- **Nota:** reforçar oralmente que a aula não vai cobrir implementação de nenhuma ferramenta específica, só vocabulário e critérios.

## 4. Big Data, afinal
- **Título:** Big Data: além do modismo
- **Citação (blockquote):** "When you're hitting the limits of your technology, that's when data gets big."
- **Fonte (citação em destaque menor):** Jeff Kelly, analista de Big Data da Wikibon — citado por Network World (2012)
- **Visual:** citação em destaque (quote/callout grande), tom de definição-chave da aula, com tradução livre e atribuição ao autor.
- **Nota:** contextualizar o cenário "clássico" antes: um arquivo, um programa, uma máquina, cabendo na RAM (ex.: Pandas). A frase não é uma citação literal de nenhum paper — é a formulação de Jeff Kelly (Wikibon), reportada pela Network World, que capta a mesma ideia central usada como tese de abertura da aula.

## 5. Os três limites
- **Título:** Big Data: além do modismo
- **Subtítulo:** Quando as ferramentas tradicionais param de funcionar
- **Bullets finais:**
  - Volume — não cabe na memória de uma máquina
  - Velocidade — dados chegam mais rápido do que dá para processar
  - Variedade — formatos e fontes demais para um modelo único de tabela
- **Visual:** três cards lado a lado (grid 3 colunas).
- **Nota:** perguntar à turma: "os seus dados cabem confortavelmente na memória da sua máquina?" — se sim, provavelmente não precisa de Big Data.

## 6. Um problema mais antigo que o termo
- **Título:** Big Data: além do modismo
- **Citação (blockquote):** "It's sink or swim as a tidal wave of data approaches." — Nature, 1999 (Reichhardt)
- **Visual:** citação/destaque editorial, tom histórico (Pathos), sem imagem real da revista (não copiar asset de terceiros).
- **Nota:** genômica e astronomia já enfrentavam o mesmo problema, dez anos antes do termo "Big Data" pegar — o vocabulário mudou ("maré de dados" → "Big Data"), o diagnóstico é o mesmo.

## 7. Os 5 V's do Big Data
- **Título:** Big Data: além do modismo
- **Subtítulo:** Os 5 V's do Big Data
- **Bullets finais (grid de 5):**
  - Volume — quantidade total de dados
  - Velocidade — frequência de chegada
  - Variedade — formatos e estruturas diferentes
  - Veracidade — confiabilidade e qualidade
  - Valor — só se justifica se gerar decisão
- **Visual:** grid/cards de 5 itens.
- **Nota:** deixar claro que Volume/Velocidade/Variedade são os originais de 2001 (Doug Laney, META Group/Gartner); Veracidade e Valor vieram depois, via IBM e mercado. Mencionar rapidamente que existem 6º/7º V's (Variabilidade, Visualização) dependendo da fonte, mas os 5 já bastam.

## 8. Os dados que vamos usar
- **Título:** Big Data: além do modismo
- **Subtítulo:** Os dados que vamos usar
- **Bullets finais (grid de 3):**
  - Funcionários — dados de RH de uma empresa fictícia: nome, cargo, departamento, status, data de admissão
  - CSV particionado por mês — cada extração mensal vira sua própria pasta, padrão comum em pipelines de ingestão de sistemas de RH/HCM
  - 12 meses — de set/2025 a ago/2026, cada partição é uma fotografia completa da base naquele momento
- **Visual:** 3 cards lado a lado, com o caminho `data/landing/funcionarios/dt=AAAA-MM-DD/funcionarios.csv` em destaque monoespaçado abaixo.
- **Nota:** contextualizar a origem dos dados antes do gráfico de crescimento — deixar claro que é o mesmo dataset usado no notebook (`conceitos-basicos-de-big-data.ipynb`), e que "fotografia completa" antecipa o gancho da duplicidade no próximo slide.

## 9. Mão na massa: crescimento da base
- **Título:** Big Data: além do modismo
- **Subtítulo:** Medindo o crescimento da base, mês a mês
- **Visual:** gráfico de linha (recriar a partir dos dados reais do notebook: 12 pontos, de 150 em 2025-09 a 219 em 2026-08) — regenerar como gráfico próprio do deck, não capturar screenshot do notebook.
- **Nota:** dado real do repositório (`data/landing/funcionarios/`), particionado por `dt=AAAA-MM-DD`.

## 10. A armadilha da duplicidade
- **Título:** Big Data: além do modismo
- **Subtítulo:** Nem toda linha é um funcionário novo
- **Bullets finais:**
  - 2.224 linhas somando todas as partições
  - 219 funcionários únicos
  - Cada partição é uma extração completa — não só os novos do mês
- **Visual:** dois números grandes em destaque (comparação lado a lado / stat cards).
- **Nota:** gancho para Slowly Changing Dimensions, que será retomado na seção de modelagem. Mencionar que em escala real (500 mil funcionários, 10 anos) isso vira um problema de Big Data de verdade.

## 11. Quando Pandas (e Excel) não bastam mais
- **Título:** Big Data: além do modismo
- **Subtítulo:** Três sinais de que chegou a hora
- **Bullets finais:**
  - Os dados não cabem na memória de uma máquina
  - O tempo de processamento é inviável
  - Os dados estão espalhados em múltiplas fontes
- **Visual:** lista numerada / 3 cards.
- **Nota:** reforçar que ferramentas de Big Data funcionam bem com dados pequenos também — a diferença é que continuam funcionando quando os dados crescem.

## 12. O ecossistema de Big Data
- **Título:** O ecossistema que resolve o problema
- **Subtítulo:** Quatro peças que resolvem o problema
- **Bullets finais:** Armazenamento distribuído · Processamento distribuído · Arquitetura em camadas · Orquestração
- **Visual:** diagrama de fluxo (baseado no mermaid do notebook): Armazenamento → Processamento → Camadas, com Orquestração coordenando as três.
- **Nota:** slide-mapa da seção — cada peça vira um slide próprio a seguir.

## 13. Armazenamento distribuído — GFS
- **Título:** O ecossistema que resolve o problema
- **Subtítulo:** Armazenamento Distribuído
- **Fonte (citação em destaque menor):** Google File System — Ghemawat, Gobioff & Leung, SOSP '03 (2003)
- **Bullets finais:**
  - Arquivo dividido em chunks de 64 MB
  - Cada chunk replicado em 3 máquinas
  - Master guarda só os metadados de localização
- **Visual:** diagrama (arquivo → chunks → 3 chunkservers + master), baseado no mermaid do notebook.
- **Nota:** ideia central do paper — assumir que componentes vão falhar o tempo todo é parte do design, não exceção. Amazon S3 como exemplo real equivalente.

## 14. Processamento distribuído — MapReduce e Spark
- **Título:** O ecossistema que resolve o problema
- **Subtítulo:** Processamento Distribuído
- **Fonte (citação em destaque menor):** MapReduce (Dean & Ghemawat, OSDI '04) → Apache Spark (Zaharia et al., NSDI '12)
- **Bullets finais:**
  - Map: processa cada registro, gera pares chave/valor
  - Shuffle: agrupa por chave
  - Reduce: combina os valores de cada chave
- **Visual:** diagrama de fluxo map → shuffle → reduce, baseado no mermaid do notebook.
- **Nota:** Spark resolveu a limitação de gravar em disco entre etapas com RDDs em memória — ganho relatado de ~10x em cargas iterativas, mantendo tolerância a falhas via lineage.

## 15. Arquitetura Lakehouse e camadas Medalhão
- **Título:** O ecossistema que resolve o problema
- **Subtítulo:** Arquitetura Lakehouse e Camadas Medalhão
- **Fonte (citação em destaque menor):** Armbrust, Ghodsi, Xin & Zaharia — CIDR '21
- **Bullets finais:**
  - Bronze — dados crus + metadados de auditoria
  - Silver — limpo, deduplicado, tipado
  - Gold — modelado para consumo analítico
- **Visual:** diagrama de fluxo Landing → Bronze → Silver → Gold → Dashboards, com as cores de camada do DESIGN.md (badges Bronze/Silver/Gold).
- **Nota:** Lakehouse resolve os 4 problemas do modelo "lake + warehouse": confiabilidade, desatualização, analytics avançado limitado, custo duplicado. Estatística: 86% dos analistas usam dados desatualizados (citada no paper).

## 16. Orquestração
- **Título:** O ecossistema que resolve o problema
- **Subtítulo:** Orquestração
- **Fonte (citação em destaque menor):** Apache Airflow — Beauchemin, Airbnb Engineering (2015)
- **Visual:** diagrama do DAG do notebook: `Bronze: funcionarios` → `Silver: dim_funcionario` e `Bronze: eventos` → `Silver: eventos`, convergindo em `Gold: fato_eventos_rh`.
- **Nota:** DAG = grafo acíclico dirigido; garante, por exemplo, que Silver só comece depois que Bronze terminar com sucesso. Esse DAG específico antecipa o projeto aplicado do curso.

## 17. Transição: da camada Gold ao modelo de dados
- **Título:** Fundamentos de modelagem dimensional
- **Subtítulo:** "Modelado para consumo analítico" — o que isso quer dizer?
- **Texto de apoio:** Modelagem dimensional: tanta teoria — e tanta história — quanto o próprio Big Data.
- **Visual:** slide de transição/section-mark, texto centralizado.
- **Nota:** marca a virada de assunto (ecossistema → modelagem), reduz a chance de a turma achar que já terminou a aula.

## 18. OLTP vs. OLAP
- **Título:** Fundamentos de modelagem dimensional
- **Subtítulo:** OLTP vs. OLAP
- **Visual:** comparação lado a lado (duas colunas).
  - Coluna 1 — OLTP: muitas transações pequenas e simultâneas; modelo relacional normalizado (Codd, 1970); ótimo para escrita.
  - Coluna 2 — OLAP: poucas consultas, porém pesadas, sobre histórico; dados desnormalizados de propósito; papel da camada Gold.
- **Nota:** normalização é ótima para escrita, cara para leitura analítica (pergunta simples pode exigir juntar dezenas de tabelas).

## 19. Os quatro tipos de analytics
- **Título:** Fundamentos de modelagem dimensional
- **Subtítulo:** Antes de modelar: para que serve o modelo?
- **Fonte (citação em destaque menor):** Delen & Demirkan (2013) — escada de complexidade e valor crescentes
- **Bullets finais:**
  - Descritiva — "O que aconteceu?"
  - Diagnóstica — "Por que aconteceu?"
  - Preditiva — "O que vai acontecer?"
  - Prescritiva — "O que devemos fazer?"
- **Visual:** diagrama de progressão horizontal (4 estágios), baseado no mermaid do notebook.
- **Nota:** não é hierarquia de "melhor" — a maioria das organizações usa os quatro o tempo todo. O modelo dimensional que vem a seguir viabiliza os quatro a partir do mesmo conjunto de tabelas.

## 20. Fatos e dimensões
- **Título:** Fundamentos de modelagem dimensional
- **Subtítulo:** O Modelo Dimensional: Fatos e Dimensões
- **Fonte (citação em destaque menor):** Ralph Kimball — medições numéricas cercadas de contexto descritivo
- **Bullets finais:**
  - Fato — medições (quantidade, valor, duração) + chaves para as dimensões
  - Dimensão — o "quem", "o quê", "onde", "quando" de cada medição
- **Visual:** diagrama de esquema estrela (fato central + 4 dimensões ao redor), baseado no erDiagram do notebook (fato de vendas: produto, cliente, loja, data).
- **Nota:** o desenho lembra uma estrela → star schema. Quando dimensões também são normalizadas, vira snowflake schema.

## 21. O grão (grain)
- **Título:** Fundamentos de modelagem dimensional
- **Citação (blockquote):** "Antes de desenhar a fato: declare o grão. O que, exatamente, representa uma linha da tabela?"
- **Fonte (citação em destaque menor):** Kimball, "Keep to the Grain in Dimensional Modeling" (2007)
- **Visual:** citação em destaque, com nota de rodapé de atribuição.
- **Nota:** o grão deve partir do nível mais atômico possível, determinado pela realidade física da coleta na origem — não pelas perguntas de negócio de hoje. Mencionar rapidamente o debate Inmon (top-down) vs. Kimball (bottom-up) como nota de rodapé, sem aprofundar.

## 22. Três tipos de tabela fato
- **Título:** Fundamentos de modelagem dimensional
- **Subtítulo:** Três tipos de tabela fato
- **Bullets finais:**
  - Transação — uma linha por evento (ex.: admissão, promoção, desligamento)
  - Snapshot periódico — uma linha por período (ex.: headcount mensal por departamento)
  - Snapshot cumulativo — uma linha por processo, atualizada a cada etapa
- **Visual:** 3 cards lado a lado.
- **Nota:** as extrações mensais de `funcionarios`/`departamentos` da aula têm cara de snapshot periódico — mas na Gold viram matéria-prima de dimensão, não de fato. A fronteira fato/dimensão depende da pergunta de negócio.

## 23. Outros tipos de dimensão
- **Título:** Fundamentos de modelagem dimensional
- **Subtítulo:** Além da Estrela Básica
- **Bullets finais:**
  - Degenerada — identificador sem tabela própria (ex.: número de pedido)
  - Conformada — mesma dimensão reutilizada por várias fatos
  - Junk — vários indicadores de baixa cardinalidade agrupados
  - Role-playing — mesma dimensão física, papéis diferentes (ex.: data do pedido / data de entrega)
- **Visual:** grid 2x2 de cards.
- **Nota:** todas continuam a mesma regra de ouro — fato mede, dimensão descreve.

## 24. Slowly Changing Dimensions
- **Título:** Fundamentos de modelagem dimensional
- **Subtítulo:** Modelando Mudanças ao Longo do Tempo
- **Visual:** comparação lado a lado.
  - Tipo 1 — sobrescreve o valor antigo; simples, mas perde histórico
  - Tipo 2 — insere nova linha com surrogate key, `data_inicio_vigencia`/`data_fim_vigencia`/`is_current`; preserva histórico completo
- **Nota:** retomando a duplicidade que vimos na prática (slide 10). Mencionar de passagem que existem Tipos 0, 3 e 4–7 (mais avançados), mas Tipo 1 e Tipo 2 cobrem a grande maioria dos casos reais.

## 25. Batch vs. Streaming
- **Título:** Fundamentos de modelagem dimensional
- **Subtítulo:** Batch vs. Streaming
- **Bullets finais:**
  - Batch — dados acumulados por um período, processados de uma vez (o caso desta aula: extrações mensais)
  - Streaming — cada evento processado assim que chega, latência de segundos ou menos
- **Visual:** diagrama comparativo (baseado no mermaid do notebook: eventos acumulando em buffer vs. eventos processados na hora).
- **Nota:** não são mutuamente exclusivos — arquiteturas modernas combinam os dois. O Dataflow Model (Akidau et al., 2015) trata batch como caso particular de streaming.

## 26. Fechamento
- **Título:** Fechamento e onde se aprofundar
- **Subtítulo:** O que você leva desta aula
- **Bullets finais:**
  - Critérios objetivos para reconhecer um problema de Big Data (volume, velocidade, variedade além do limite de uma máquina)
  - As quatro peças do ecossistema: armazenamento, processamento, camadas, orquestração
  - Os fundamentos que sustentam a camada Gold: OLTP vs. OLAP, fato/dimensão, grão, SCD
  - Os quatro tipos de analytics e a distinção batch vs. streaming
- **Visual:** slide de encerramento, sem imagem adicional.
- **Nota:** gancho para a próxima aula/notebook: a demonstração prática (`demonstracao-lakehouse-medalhao.ipynb`), que implementa esse mesmo vocabulário em código.

## 27. Para se aprofundar
- **Título:** Fechamento e onde se aprofundar
- **Subtítulo:** Para se aprofundar
- **Bullets finais (seleção dos mais citados em aula, não a lista completa de 15 papers):**
  - Codd (1970) — A Relational Model of Data for Large Shared Data Banks
  - Ghemawat, Gobioff & Leung (2003) — The Google File System
  - Dean & Ghemawat (2004) — MapReduce
  - Zaharia et al. (2012) — Resilient Distributed Datasets (Spark)
  - Armbrust et al. (2021) — Lakehouse (CIDR '21)
  - Kimball Group — Fact Tables and Dimension Tables, Slowly Changing Dimensions
- **Visual:** lista simples, tipografia menor (`typography.small`), sem grid decorativo — é slide de referência, não de destaque.
- **Nota:** mencionar oralmente que a lista completa (15 referências, em ordem cronológica) está no notebook, seção "Os Artigos Originais, Reunidos", e que basta ler o abstract de cada uma para acompanhar a aula. Não incluir URLs no slide (ilegíveis em projeção) — indicar que os links estão no notebook.

## 28. Obrigado
- **Título:** Obrigado!
- **Subtítulo:** Dúvidas, sugestões ou feedback sobre a aula? Manda um e-mail.
- **Contato:** wpcortes@gmail.com (link `mailto:`, pill estilo `.repo-card`)
- **Visual:** imagem lateral (`assets/images/gato-perguntas.jpg`, gato curioso — tema Q&A/perguntas) ocupando a faixa direita do palco, com fade suave para o fundo claro à esquerda; texto e contato à esquerda.
- **Nota:** slide de encerramento puro (fora dos 4 blocos da agenda) — convite direto para contato por e-mail.

---

## Fora do escopo deste roteiro

- Diagramas mermaid do notebook são recriados como diagramas nativos do deck (SVG/HTML), não incorporados como imagem — para acompanhar a paleta do `DESIGN.md` e permitir animação/entrada progressiva se necessário.
