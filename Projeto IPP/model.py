import json
from datetime import datetime, timedelta

class Paciente:
    def __init__(self, id_paciente, nome, data_nascimento, sexo, grupo_risco, contacto, historico_consultas=None, consultas_agendadas=None):
        self.id_paciente = id_paciente
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.grupo_risco = grupo_risco
        self.contacto = contacto
        self.historico_consultas = historico_consultas or []
        self.consultas_agendadas = consultas_agendadas or []

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
    
    def agendar_consulta(self, data, hora, id_medico):
        self.consultas_agendadas.append({
            "data": data,
            "hora": hora,
            "id_medico": id_medico
        })
    
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
    def __init__(self, id_medico, nome, data_nascimento, sexo, especialidade, contacto, horario_atendimento, disponibilidade, consultas_agendadas):
        self.id_medico = id_medico
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.especialidade = especialidade
        self.contacto = contacto
        self.horario_atendimento = horario_atendimento
        self.disponibilidade = disponibilidade or []
        self.consultas_agendadas = consultas_agendadas or []
    
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
    
    def info_agenda(self):
        # Ordenar as consultas por data e hora
        consultas_ordenadas = sorted(
            self.consultas_agendadas,
            key=lambda x: datetime.strptime(f"{x['data']} {x['hora']}", "%d-%m-%Y %H:%M")
        )
        
        # Criar a lista formatada já ordenada
        return [f"{consulta['data']} às {consulta['hora']} - {self.nome} ({self.especialidade})" 
                for consulta in consultas_ordenadas]

    def verificar_agenda(self, data_escolhida, hora_escolhida):
        # Primeiro verifica se já tem consulta marcada nessa data e hora
        for consulta in self.consultas_agendadas:
            if consulta["data"] == data_escolhida and consulta["hora"] == hora_escolhida:
                return False  # já está ocupada

        # Em seguida, verifica se esse horário está ativo na disponibilidade padrão semanal
        from datetime import datetime
        data = datetime.strptime(data_escolhida, "%d-%m-%Y")
        dia_semana = data.weekday()  # segunda = 0, ..., domingo = 6

        if hora_escolhida not in self.horario_atendimento:
            return False  # hora inválida para este médico

        idx_hora = self.horario_atendimento.index(hora_escolhida)
        self.disponibilidade[dia_semana][idx_hora] == 1
        return True  # horário disponível
    
    def agendar_consulta(self, data, hora, id_paciente):
        if not self.verificar_agenda(data, hora):
            return False  # Não disponível ou já ocupado

        # Adicionar a consulta à agenda
        self.consultas_agendadas.append({
            "data": data,
            "hora": hora,
            "id_paciente": id_paciente
        })

        return True  # Consulta agendada com sucesso
    
    def disponibilidade_semanal(self, data_inicio):
        data_inicio = datetime.strptime(data_inicio, "%d-%m-%Y")
        dias_da_semana = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]

        semana = {}

        for i in range(7):  # 7 dias da semana
            data_dia = data_inicio + timedelta(days=i)
            dia_str = data_dia.strftime("%d-%m-%Y")
            dia_semana_idx = data_dia.weekday()  # 0 a 6

            disponibilidade_dia = self.disponibilidade[dia_semana_idx][:]  # cópia

            for consulta in self.consultas_agendadas:
                if consulta["data"] == dia_str:
                    if consulta["hora"] in self.horario_atendimento:
                        idx_hora = self.horario_atendimento.index(consulta["hora"])
                        disponibilidade_dia[idx_hora] = 0  # ocupado
            
            semana[dia_str] = disponibilidade_dia
        return semana

    def formatar_horario_disponibilidade(self, semana):
        horario = "Horário Semanal:\n\n"
        dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        
        for data, disponibilidade in semana.items():
            data_obj = datetime.strptime(data, "%d-%m-%Y")
            dia_semana = dias_semana[data_obj.weekday()]
            horario += f"{dia_semana} - {data}\n"
            horario += "Horários:\n"
            for idx, disp in enumerate(disponibilidade):
                hora = self.horario_atendimento[idx]
                status = "Disponível" if disp == 1 else "Ocupado"
                horario += f"{hora}: {status}\n"
            horario += "-" * 30 + "\n"
        return horario

    def get_semana_disponibilidade(self, offset_semanas=0):
        """Get disponibilidade para uma semana específica (0=atual, 1=próxima, -1=anterior)"""
        hoje = datetime.today()
        inicio_semana = hoje - timedelta(days=hoje.weekday())  # Segunda-feira
        inicio_semana += timedelta(weeks=offset_semanas)  # Ajusta para semana desejada
        return self.disponibilidade_semanal(inicio_semana.strftime("%d-%m-%Y"))

    def eliminar_consulta(self, data_escolhida, hora_escolhida):
        for consulta in self.consultas_agendadas:
            if consulta["data"] == data_escolhida and consulta["hora"] == hora_escolhida:
                # Atualizar a disponibilidade
                data = datetime.strptime(data_escolhida, "%d-%m-%Y")
                dia_semana = data.weekday()
                idx_hora = self.horario_atendimento.index(hora_escolhida)
                self.disponibilidade[dia_semana][idx_hora] = 1  # 1 indica disponível
                
                # Remover a consulta
                self.consultas_agendadas.remove(consulta)
                return True
        return False

def gerar_agenda_semanal(medicos, pacientes, data_inicio, offset_semanas=0):
    if isinstance(data_inicio, str):
        data_inicio = datetime.strptime(data_inicio, "%d-%m-%Y")
    
    data_inicio = data_inicio + timedelta(weeks=offset_semanas)
    data_inicio = data_inicio - timedelta(days=data_inicio.weekday())
    
    agenda = {dia: "" for dia in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]}

    for paciente in pacientes:
        for consulta in paciente.consultas_agendadas:
            data_consulta = datetime.strptime(consulta["data"], "%d-%m-%Y")
            if data_inicio <= data_consulta < data_inicio + timedelta(days=7):
                dia_semana = data_consulta.weekday()
                dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
                dia = dias_semana[dia_semana]
                agenda[dia] += f"{consulta['hora']} - {paciente.nome}\n"

    return agenda, data_inicio.strftime("%d-%m-%Y")

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

