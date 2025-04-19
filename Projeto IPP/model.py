import json
from datetime import datetime

class Paciente:
    def __init__(self, id_paciente, nome, data_nascimento, sexo, grupo_risco, contacto, historico_consultas=None):
        self.id_paciente = id_paciente
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.grupo_risco = grupo_risco
        self.contacto = contacto
        self.historico_consultas = historico_consultas or []

    def idade(self):
        data_nasc = datetime.strptime(self.data_nascimento, "%d-%m-%Y")
        hoje = datetime.today()
        return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
    
    def info_paciente(self):
        return {
            "id": self.id_paciente,
            "nome": self.nome,
            "idade": self.idade(),
            "sexo": self.sexo,
            "grupo_risco": self.grupo_risco,
            "contacto": self.contacto
        }
    
    def adicionar_consulta(self, consulta):
        """Adiciona uma nova consulta ao topo da pilha (histórico)"""
        self.historico_consultas.append(consulta)
    
    def remover_ultima_consulta(self):
        """Remove e retorna a consulta mais recente"""
        if self.historico_consultas:
            return self.historico_consultas.pop()
        return None
    
    def ver_historico(self):
        if not self.historico_consultas:
            return "Sem histórico de consultas"
        
        historico = ""
        for consulta in self.historico_consultas:
            historico += f"""
Data: {consulta["data"]}
Médico: {consulta["medico"]}
Especialidade: {consulta["especialidade"]}
Diagnóstico: {consulta["diagnostico"]}
-----------------------------------------
"""
        return historico

def guardar_pacientes(lista):
    with open("C:\\Users\\ze05p\\OneDrive\\Documentos\\Licenciatura em Engenharia Biomédica\\2º Ano\\2º Semestre\\Paradigmas da Programação\\Projeto IPP\\Data\\pacientes.json", "w", encoding="utf-8") as f:
        json.dump([p.__dict__ for p in lista], f, indent=4, ensure_ascii=False)

def carregar_pacientes():
    try:
        with open("C:\\Users\\ze05p\\OneDrive\\Documentos\\Licenciatura em Engenharia Biomédica\\2º Ano\\2º Semestre\\Paradigmas da Programação\\Projeto IPP\\Data\\pacientes.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            pacientes = [Paciente(**p) for p in dados]
            return pacientes
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return []
    
#############################################################################

class Medico:
    def __init__(self, id_medico, nome, data_nascimento, sexo, especialidade, contacto, disponibilidade=None):
        self.id_medico = id_medico
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.especialidade = especialidade
        self.contacto = contacto
        self.disponibilidade = disponibilidade or []
    
    def idade(self):
        data_nasc = datetime.strptime(self.data_nascimento, "%d-%m-%Y")
        hoje = datetime.today()
        return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

    def info_medico(self):
        return {
            "id": self.id_medico,
            "nome": self.nome,
            "idade": self.idade(),
            "sexo": self.sexo,
            "especialidade": self.especialidade,
            "contacto": self.contacto
        }

def guardar_medicos(lista):
    with open("C:\\Users\\ze05p\\OneDrive\\Documentos\\Licenciatura em Engenharia Biomédica\\2º Ano\\2º Semestre\\Paradigmas da Programação\\Projeto IPP\\Data\\medicos.json", "w", encoding="utf-8") as f:
        json.dump([m.__dict__ for m in lista], f, indent=4, ensure_ascii=False)

def carregar_medicos():
    try:
        with open("C:\\Users\\ze05p\\OneDrive\\Documentos\\Licenciatura em Engenharia Biomédica\\2º Ano\\2º Semestre\\Paradigmas da Programação\\Projeto IPP\\Data\\medicos.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            medicos = [Medico(**m) for m in dados]
            return medicos
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return []

