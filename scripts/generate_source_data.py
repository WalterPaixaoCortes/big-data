#!/usr/bin/env python3
"""
Gera dados de origem sintéticos (funcionários, cargos, departamentos, eventos de RH)
simulando o export de um sistema de RH/HCM, para alimentar a landing zone descrita em
PROJETO_HR_DATA_PIPELINE.md (seção 4: [Sistema de RH] -> [Fivetran] -> [S3 raw landing zone]).

Segue as premissas documentadas na seção 4.2/9.1 do projeto:
  - Dados mestres (departamentos, cargos, funcionarios) chegam como SNAPSHOT COMPLETO
    a cada carga mensal (uma pasta dt=<data> por mês, com o estado completo naquele
    ponto no tempo) -- input da comparação SCD2 na camada Gold.
  - Eventos chegam de forma INCREMENTAL/APPEND-ONLY: cada evento é imutável e só
    aparece uma vez, na pasta dt= do mês em que ocorreu.

Uso:
    python scripts/generate_source_data.py
    python scripts/generate_source_data.py --output data/landing --meses 12 --seed 42
    python scripts/generate_source_data.py --formato json
"""
from __future__ import annotations

import argparse
import csv
import json
import random
from dataclasses import dataclass, asdict
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

NOMES = [
    "Ana", "Bruno", "Carla", "Daniel", "Elaine", "Fábio", "Gabriela", "Hugo",
    "Isabela", "João", "Karina", "Lucas", "Mariana", "Nelson", "Otávio",
    "Patrícia", "Rafael", "Sabrina", "Tiago", "Vanessa", "Wesley", "Yasmin",
    "Camila", "Diego", "Eduarda", "Felipe", "Gustavo", "Helena", "Igor", "Juliana",
]
SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Almeida",
    "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho",
    "Araujo", "Barbosa", "Rocha", "Dias", "Nascimento", "Moreira",
]
GENEROS = ["Feminino", "Masculino", "Não informado"]
GENERO_PESOS = [0.48, 0.48, 0.04]

MOTIVOS_DESLIGAMENTO = [
    "Pedido de demissão", "Desligamento sem justa causa",
    "Fim de contrato de experiência", "Aposentadoria",
]
MOTIVOS_AJUSTE = ["Reajuste anual", "Ajuste de mercado", "Retenção de talento"]


@dataclass
class Departamento:
    departamento_id: str
    nome_departamento: str
    centro_custo: str
    departamento_pai_id: Optional[str] = None


@dataclass
class Cargo:
    cargo_id: str
    nome_cargo: str
    nivel: str
    faixa_salarial_min: float
    faixa_salarial_max: float


@dataclass
class Funcionario:
    funcionario_id: str
    nome: str
    data_nascimento: date
    genero: str
    email: str
    data_admissao: date
    departamento_id: str
    cargo_id: str
    salario_atual: float
    status: str = "Ativo"


DEPARTAMENTOS = [
    Departamento("D01", "Diretoria", "CC-100", None),
    Departamento("D02", "Recursos Humanos", "CC-210", "D01"),
    Departamento("D03", "Tecnologia", "CC-220", "D01"),
    Departamento("D04", "Financeiro", "CC-230", "D01"),
    Departamento("D05", "Vendas", "CC-240", "D01"),
    Departamento("D06", "Operações", "CC-250", "D01"),
    Departamento("D07", "Marketing", "CC-260", "D01"),
    Departamento("D08", "Atendimento ao Cliente", "CC-241", "D05"),
]

CARGOS = [
    Cargo("C01", "Analista Júnior", "Júnior", 3000, 4500),
    Cargo("C02", "Analista Pleno", "Pleno", 4500, 6500),
    Cargo("C03", "Analista Sênior", "Sênior", 6500, 9000),
    Cargo("C04", "Especialista", "Especialista", 9000, 12000),
    Cargo("C05", "Coordenador", "Coordenador", 10000, 14000),
    Cargo("C06", "Gerente", "Gerente", 14000, 20000),
    Cargo("C07", "Diretor", "Diretor", 22000, 35000),
    Cargo("C08", "Desenvolvedor Júnior", "Júnior", 3500, 5000),
    Cargo("C09", "Desenvolvedor Pleno", "Pleno", 5500, 8000),
    Cargo("C10", "Desenvolvedor Sênior", "Sênior", 8500, 12000),
    Cargo("C11", "Assistente Administrativo", "Júnior", 2200, 3200),
    Cargo("C12", "Vendedor", "Pleno", 3000, 6000),
    Cargo("C13", "Atendente", "Júnior", 2200, 3000),
    Cargo("C14", "Recrutador", "Pleno", 4000, 6000),
]

TRILHA_PROMOCAO = {
    "C01": "C02", "C02": "C03", "C03": "C04",
    "C08": "C09", "C09": "C10", "C10": "C04",
    "C11": "C02", "C13": "C12", "C14": "C02",
    "C04": "C05", "C05": "C06", "C06": "C07",
}

CARGOS_POR_ID = {c.cargo_id: c for c in CARGOS}
DEPARTAMENTOS_POR_ID = {d.departamento_id: d for d in DEPARTAMENTOS}


def add_months(d: date, months: int) -> date:
    total = d.month - 1 + months
    year = d.year + total // 12
    month = total % 12 + 1
    return date(year, month, 1)


def gerar_email(nome: str, sobrenome: str, funcionario_id: str) -> str:
    base = f"{nome}.{sobrenome}".lower()
    base = (
        base.replace("á", "a").replace("ã", "a").replace("â", "a")
        .replace("é", "e").replace("ê", "e")
        .replace("í", "i")
        .replace("ó", "o").replace("õ", "o").replace("ô", "o")
        .replace("ú", "u").replace("ç", "c")
    )
    return f"{base}.{funcionario_id.lower()}@empresa.com.br"


class GeradorRH:
    def __init__(self, rng: random.Random, funcionario_seq: int = 1, evento_seq: int = 1):
        self.rng = rng
        self.funcionario_seq = funcionario_seq
        self.evento_seq = evento_seq
        self.funcionarios: dict[str, Funcionario] = {}
        self.departamentos = [Departamento(**asdict(d)) for d in DEPARTAMENTOS]
        self.cargos = [Cargo(**asdict(c)) for c in CARGOS]
        self.eventos_por_mes: dict[date, list[dict]] = {}
        self.snapshots_por_mes: dict[date, dict] = {}

    def novo_funcionario_id(self) -> str:
        fid = f"FUNC{self.funcionario_seq:05d}"
        self.funcionario_seq += 1
        return fid

    def novo_evento_id(self) -> str:
        eid = f"EVT{self.evento_seq:06d}"
        self.evento_seq += 1
        return eid

    def registrar_evento(self, mes_ref: date, **campos):
        self.eventos_por_mes.setdefault(mes_ref, []).append(campos)

    def contratar(self, data_admissao: date, mes_ref: date) -> Funcionario:
        nome = self.rng.choice(NOMES)
        sobrenome = self.rng.choice(SOBRENOMES)
        funcionario_id = self.novo_funcionario_id()
        cargo = self.rng.choice(CARGOS)
        departamento = self.rng.choice(DEPARTAMENTOS)
        salario = round(self.rng.uniform(cargo.faixa_salarial_min, cargo.faixa_salarial_max * 0.7), 2)
        idade_anos = self.rng.randint(20, 60)
        ano_nascimento = data_admissao.year - idade_anos
        func = Funcionario(
            funcionario_id=funcionario_id,
            nome=f"{nome} {sobrenome}",
            data_nascimento=date(ano_nascimento, self.rng.randint(1, 12), self.rng.randint(1, 28)),
            genero=self.rng.choices(GENEROS, weights=GENERO_PESOS)[0],
            email=gerar_email(nome, sobrenome, funcionario_id),
            data_admissao=data_admissao,
            departamento_id=departamento.departamento_id,
            cargo_id=cargo.cargo_id,
            salario_atual=salario,
        )
        self.funcionarios[funcionario_id] = func
        self.registrar_evento(
            mes_ref,
            evento_id=self.novo_evento_id(),
            funcionario_id=funcionario_id,
            data_evento=data_admissao,
            tipo_evento="Admissão",
            departamento_id=departamento.departamento_id,
            cargo_id=cargo.cargo_id,
            salario_anterior=None,
            salario_novo=salario,
            motivo="Contratação",
        )
        return func

    def promover(self, func: Funcionario, mes_ref: date, data_evento: date):
        novo_cargo_id = TRILHA_PROMOCAO.get(func.cargo_id)
        if novo_cargo_id is None:
            return
        cargo_antigo = CARGOS_POR_ID[func.cargo_id]
        cargo_novo = CARGOS_POR_ID[novo_cargo_id]
        salario_anterior = func.salario_atual
        salario_novo = round(max(salario_anterior * 1.1, cargo_novo.faixa_salarial_min), 2)
        func.cargo_id = novo_cargo_id
        func.salario_atual = salario_novo
        self.registrar_evento(
            mes_ref,
            evento_id=self.novo_evento_id(),
            funcionario_id=func.funcionario_id,
            data_evento=data_evento,
            tipo_evento="Promoção",
            departamento_id=func.departamento_id,
            cargo_id=novo_cargo_id,
            salario_anterior=salario_anterior,
            salario_novo=salario_novo,
            motivo=f"Promoção de {cargo_antigo.nome_cargo} para {cargo_novo.nome_cargo}",
        )

    def transferir(self, func: Funcionario, mes_ref: date, data_evento: date):
        destino = self.rng.choice([d for d in DEPARTAMENTOS if d.departamento_id != func.departamento_id])
        origem = DEPARTAMENTOS_POR_ID[func.departamento_id]
        func.departamento_id = destino.departamento_id
        self.registrar_evento(
            mes_ref,
            evento_id=self.novo_evento_id(),
            funcionario_id=func.funcionario_id,
            data_evento=data_evento,
            tipo_evento="Transferência",
            departamento_id=destino.departamento_id,
            cargo_id=func.cargo_id,
            salario_anterior=None,
            salario_novo=None,
            motivo=f"Transferência de {origem.nome_departamento} para {destino.nome_departamento}",
        )

    def ajustar_salario(self, func: Funcionario, mes_ref: date, data_evento: date):
        salario_anterior = func.salario_atual
        salario_novo = round(salario_anterior * self.rng.uniform(1.03, 1.12), 2)
        func.salario_atual = salario_novo
        self.registrar_evento(
            mes_ref,
            evento_id=self.novo_evento_id(),
            funcionario_id=func.funcionario_id,
            data_evento=data_evento,
            tipo_evento="Alteração Salarial",
            departamento_id=func.departamento_id,
            cargo_id=func.cargo_id,
            salario_anterior=salario_anterior,
            salario_novo=salario_novo,
            motivo=self.rng.choice(MOTIVOS_AJUSTE),
        )

    def avaliar(self, func: Funcionario, mes_ref: date, data_evento: date):
        nota = self.rng.randint(1, 5)
        self.registrar_evento(
            mes_ref,
            evento_id=self.novo_evento_id(),
            funcionario_id=func.funcionario_id,
            data_evento=data_evento,
            tipo_evento="Avaliação",
            departamento_id=func.departamento_id,
            cargo_id=func.cargo_id,
            salario_anterior=None,
            salario_novo=None,
            motivo=f"Avaliação de desempenho: nota {nota}/5",
        )

    def desligar(self, func: Funcionario, mes_ref: date, data_evento: date):
        salario_anterior = func.salario_atual
        func.status = "Inativo"
        self.registrar_evento(
            mes_ref,
            evento_id=self.novo_evento_id(),
            funcionario_id=func.funcionario_id,
            data_evento=data_evento,
            tipo_evento="Desligamento",
            departamento_id=func.departamento_id,
            cargo_id=func.cargo_id,
            salario_anterior=salario_anterior,
            salario_novo=None,
            motivo=self.rng.choice(MOTIVOS_DESLIGAMENTO),
        )

    def dia_aleatorio_do_mes(self, mes_ref: date) -> date:
        ultimo_dia_do_mes = (add_months(mes_ref, 1) - timedelta(days=1)).day
        return date(mes_ref.year, mes_ref.month, self.rng.randint(1, ultimo_dia_do_mes))

    def simular(
        self,
        data_inicio: date,
        meses: int,
        funcionarios_iniciais: int,
        admissoes_por_mes: tuple[int, int],
        taxa_desligamento: float,
        taxa_promocao: float,
        taxa_transferencia: float,
        taxa_ajuste_salarial: float,
        taxa_avaliacao: float,
    ):
        mes0 = data_inicio
        for _ in range(funcionarios_iniciais):
            dias_de_casa = self.rng.randint(0, 3 * 365)
            data_admissao = data_inicio - timedelta(days=dias_de_casa)
            self.contratar(data_admissao, mes0)

        for offset in range(meses):
            mes_ref = add_months(data_inicio, offset)

            if offset > 0:
                n_admissoes = self.rng.randint(*admissoes_por_mes)
                for _ in range(n_admissoes):
                    data_evento = self.dia_aleatorio_do_mes(mes_ref)
                    self.contratar(data_evento, mes_ref)

            ativos = [f for f in self.funcionarios.values() if f.status == "Ativo"]
            for func in ativos:
                data_evento = self.dia_aleatorio_do_mes(mes_ref)
                sorteio = self.rng.random()
                limiar = taxa_desligamento
                if sorteio < limiar:
                    self.desligar(func, mes_ref, data_evento)
                    continue
                limiar += taxa_promocao
                if sorteio < limiar:
                    self.promover(func, mes_ref, data_evento)
                    continue
                limiar += taxa_transferencia
                if sorteio < limiar:
                    self.transferir(func, mes_ref, data_evento)
                    continue
                limiar += taxa_ajuste_salarial
                if sorteio < limiar:
                    self.ajustar_salario(func, mes_ref, data_evento)
                    continue
                limiar += taxa_avaliacao
                if sorteio < limiar:
                    self.avaliar(func, mes_ref, data_evento)

            self._aplicar_mudancas_estruturais(offset, meses, mes_ref)
            self.snapshots_por_mes[mes_ref] = self.snapshot_mes(mes_ref)

    def _aplicar_mudancas_estruturais(self, offset: int, meses: int, mes_ref: date):
        if offset == meses // 2:
            tecnologia = next(d for d in self.departamentos if d.departamento_id == "D03")
            tecnologia.nome_departamento = "Tecnologia e Dados"
        if offset == (3 * meses) // 4:
            financeiro = next(d for d in self.departamentos if d.departamento_id == "D04")
            financeiro.centro_custo = "CC-231"
        if offset == meses // 3:
            desenvolvedor_sr = next(c for c in self.cargos if c.cargo_id == "C10")
            desenvolvedor_sr.faixa_salarial_max = 13500

    def snapshot_mes(self, mes_ref: date):
        return {
            "departamentos": [asdict(d) | {"data_extracao": mes_ref} for d in self.departamentos],
            "cargos": [asdict(c) | {"data_extracao": mes_ref} for c in self.cargos],
            "funcionarios": [
                {
                    "funcionario_id": f.funcionario_id,
                    "nome": f.nome,
                    "data_nascimento": f.data_nascimento,
                    "genero": f.genero,
                    "email": f.email,
                    "data_admissao": f.data_admissao,
                    "status": f.status,
                    "departamento_id": f.departamento_id,
                    "cargo_id": f.cargo_id,
                    "data_extracao": mes_ref,
                }
                for f in self.funcionarios.values()
                if f.data_admissao <= (add_months(mes_ref, 1) - timedelta(days=1))
            ],
        }


def escrever(registros: list[dict], caminho: Path, formato: str):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    for r in registros:
        for k, v in r.items():
            if isinstance(v, date):
                r[k] = v.isoformat()
    if not registros:
        return
    if formato == "csv":
        with open(caminho.with_suffix(".csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(registros[0].keys()))
            writer.writeheader()
            writer.writerows(registros)
    else:
        with open(caminho.with_suffix(".json"), "w", encoding="utf-8") as f:
            json.dump(registros, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", default="data/landing", help="Diretório raiz da landing zone (simula o bucket S3 raw).")
    parser.add_argument("--meses", type=int, default=12, help="Quantidade de cargas mensais a simular.")
    parser.add_argument("--funcionarios-iniciais", type=int, default=150)
    parser.add_argument("--admissoes-min", type=int, default=3)
    parser.add_argument("--admissoes-max", type=int, default=8)
    parser.add_argument("--taxa-desligamento", type=float, default=0.008)
    parser.add_argument("--taxa-promocao", type=float, default=0.02)
    parser.add_argument("--taxa-transferencia", type=float, default=0.015)
    parser.add_argument("--taxa-ajuste-salarial", type=float, default=0.03)
    parser.add_argument("--taxa-avaliacao", type=float, default=0.06)
    parser.add_argument("--data-inicio", default=None, help="YYYY-MM-DD do primeiro mês simulado (default: hoje - N meses).")
    parser.add_argument("--formato", choices=["csv", "json"], default="csv")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.data_inicio:
        y, m, d = (int(x) for x in args.data_inicio.split("-"))
        data_inicio = date(y, m, 1)
    else:
        hoje = date.today()
        data_inicio = add_months(date(hoje.year, hoje.month, 1), -args.meses + 1)

    rng = random.Random(args.seed)
    gerador = GeradorRH(rng)
    gerador.simular(
        data_inicio=data_inicio,
        meses=args.meses,
        funcionarios_iniciais=args.funcionarios_iniciais,
        admissoes_por_mes=(args.admissoes_min, args.admissoes_max),
        taxa_desligamento=args.taxa_desligamento,
        taxa_promocao=args.taxa_promocao,
        taxa_transferencia=args.taxa_transferencia,
        taxa_ajuste_salarial=args.taxa_ajuste_salarial,
        taxa_avaliacao=args.taxa_avaliacao,
    )

    output_root = Path(args.output)
    total_eventos = 0
    for offset in range(args.meses):
        mes_ref = add_months(data_inicio, offset)
        dt_str = mes_ref.isoformat()
        snap = gerador.snapshots_por_mes[mes_ref]

        escrever(snap["departamentos"], output_root / "departamentos" / f"dt={dt_str}" / "departamentos", args.formato)
        escrever(snap["cargos"], output_root / "cargos" / f"dt={dt_str}" / "cargos", args.formato)
        escrever(snap["funcionarios"], output_root / "funcionarios" / f"dt={dt_str}" / "funcionarios", args.formato)

        eventos_mes = gerador.eventos_por_mes.get(mes_ref, [])
        escrever(eventos_mes, output_root / "eventos" / f"dt={dt_str}" / "eventos", args.formato)
        total_eventos += len(eventos_mes)

    total_funcionarios = len(gerador.funcionarios)
    print(f"Landing zone gerada em: {output_root.resolve()}")
    print(f"Período simulado: {data_inicio.isoformat()} a {add_months(data_inicio, args.meses - 1).isoformat()} ({args.meses} cargas mensais)")
    print(f"Funcionários gerados (histórico completo): {total_funcionarios}")
    print(f"Eventos gerados: {total_eventos}")
    print(f"Departamentos: {len(DEPARTAMENTOS)} | Cargos: {len(CARGOS)}")


if __name__ == "__main__":
    main()
