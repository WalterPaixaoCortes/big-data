# Aula de Big Data

Repositório de notebooks e material de apoio sobre **Engenharia de Dados e Big Data**, organizado em torno de um projeto aplicado: um pipeline de dados de eventos de RH em arquitetura de Lakehouse.

## Estrutura do repositório

```
big-data/
├── aula-big-data/                 # Notebooks Jupyter
├── data/landing/                  # Dados de origem sintéticos (landing zone)
│   ├── funcionarios/dt=AAAA-MM-DD/
│   ├── departamentos/dt=AAAA-MM-DD/
│   ├── cargos/dt=AAAA-MM-DD/
│   └── eventos/dt=AAAA-MM-DD/
├── scripts/
│   ├── generate_source_data.py    # Gera os dados sintéticos da landing zone
│   ├── fabric/                    # Notebooks PySpark de Silver/Gold para o Microsoft Fabric
│   │   ├── silver.ipynb
│   │   └── gold.ipynb
│   └── databricks/                # Mesma lógica, para o Databricks (Unity Catalog)
│       ├── silver.ipynb
│       └── gold.ipynb
├── PROJETO_HR_DATA_PIPELINE.md    # Especificação do projeto aplicado
├── PROJETO_HR_DATA_PIPELINE.pdf   # Mesma especificação, em PDF
└── requirements.txt                # Dependências Python para rodar os notebooks
```

## Notebooks (`aula-big-data/`)

| Notebook | Conteúdo |
|---|---|
| `conceitos-basicos-de-big-data.ipynb` | Fundamentos de Big Data: os 5 V's (origem histórica, Doug Laney), armazenamento e processamento distribuído (Google File System, MapReduce, Spark), arquitetura Lakehouse e camadas Medalhão (Bronze/Silver/Gold), modelagem de dados (OLTP vs. OLAP, modelo estrela, fatos e dimensões, os três tipos de tabela fato, dimensões conformadas/degeneradas/junk/role-playing, Slowly Changing Dimensions) e os tipos de analytics que esse modelo viabiliza (descritiva, diagnóstica, preditiva, prescritiva), além da distinção entre processamento batch e streaming. Traz referências a artigos e papers originais (Nature, Google Research, USENIX, VLDB, CIDR, Kimball Group, entre outros) e um exercício prático com os dados reais da landing zone. |
| `demonstracao-lakehouse-medalhao.ipynb` | Demonstração prática: comparativo de funcionalidades das principais plataformas de Big Data/Lakehouse do mercado (Databricks, Microsoft Fabric, Snowflake, AWS, Google Cloud), um mini Lakehouse com arquitetura medalhão rodando localmente em pandas (Bronze → Silver → Gold sobre `departamentos`, com orquestração simplificada), a evolução desse pipeline para um esquema estrela completo (`dim_funcionario` em SCD Tipo 2, tabela fato `fato_eventos_rh` com join temporal), e um passo a passo de como implementar o mesmo padrão, com pipeline orquestrado, no **Microsoft Fabric** e no **Databricks** (incluindo os notebooks Silver/Gold prontos em `scripts/fabric/` e `scripts/databricks/`). |

Cada notebook é autossuficiente e traz um badge para abrir diretamente no Google Colab. O notebook de demonstração gera uma pasta local `data/lakehouse/` (Bronze/Silver/Gold) ao ser executado — esses arquivos são derivados/regeneráveis e ficam fora do controle de versão (ver `.gitignore`).

## Dados (`data/landing/`)

Dados sintéticos que simulam a exportação periódica de um sistema de RH/HCM, gerados por `scripts/generate_source_data.py` e organizados em partições `dt=AAAA-MM-DD` (uma pasta por mês de extração):

| Tabela | Conteúdo | Padrão de chegada |
|---|---|---|
| `funcionarios` | Cadastro de funcionários (nome, cargo, departamento, status, datas) | Snapshot completo a cada carga mensal |
| `departamentos` | Cadastro de departamentos (nome, centro de custo, hierarquia) | Snapshot completo a cada carga mensal |
| `cargos` | Cadastro de cargos (nome, nível, faixa salarial) | Snapshot completo a cada carga mensal |
| `eventos` | Eventos de RH (admissão, promoção, transferência, desligamento, alteração salarial, avaliação) | Incremental / append-only |

Para gerar (ou regenerar) os dados:

```bash
python scripts/generate_source_data.py --meses 12 --seed 42
```

## Scripts de nuvem (`scripts/fabric/`, `scripts/databricks/`)

Versões em PySpark do esquema estrela construído em pandas na seção "Modelagem Dimensional na Prática" de `demonstracao-lakehouse-medalhao.ipynb`: as mesmas transformações (dimensões `departamentos`/`cargos` em SCD Tipo 1, `dim_funcionario` em SCD Tipo 2, e as tabelas Gold `estrutura_organizacional`/`fato_eventos_rh`, com o join temporal entre fato e dimensão), portadas de `pandas`/CSV para `PySpark`/Delta Lake.

| Pasta | Ambiente | Como referenciar tabelas |
|---|---|---|
| `scripts/fabric/` | Microsoft Fabric | Tabelas de um Lakehouse anexado ao notebook (`spark.read.table("lh_bronze.departamentos")`) |
| `scripts/databricks/` | Databricks (Unity Catalog) | Namespace de três níveis (`spark.table(f"{catalogo}.bronze.departamentos")`) |

Cada pasta tem um notebook `silver.ipynb` e um `gold.ipynb`, para rodar nessa ordem. Eles não rodam localmente nem no Colab — pressupõem um workspace do Fabric ou do Databricks já com a camada Bronze populada (ver o passo a passo em `demonstracao-lakehouse-medalhao.ipynb`).

## Projeto aplicado (`PROJETO_HR_DATA_PIPELINE.md`)

Especificação de um projeto de Data Engineering: construir, a partir dos dados da landing zone, um pipeline em arquitetura de Lakehouse (Bronze → Silver → Gold) que popula um modelo estrela na camada Gold (`fato_eventos_rh` e dimensões com SCD Tipo 2), orquestrado e testado, alimentando um dashboard de métricas de RH (headcount, turnover, tempo de casa, taxa de promoção). O arquivo `.pdf` é uma exportação do mesmo documento.

## Ambiente

O ambiente virtual Python local (`.venv/`, ignorado pelo git) segue as dependências listadas em `requirements.txt`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab   # ou: jupyter notebook
```

Os notebooks também podem ser abertos direto no Google Colab pelo badge no topo de cada um; nesse caso, é preciso clonar este repositório dentro do próprio Colab antes de rodar as células que leem os dados de `data/landing/` (instrução incluída no início de cada notebook).
