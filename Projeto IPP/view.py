import PySimpleGUI as sg

FUNDO = "#E8F0FE"
TEXTO = "#1A1A1A"
BOTAO_COR = ("white", "#1976D2")

def layout_menu_principal(agenda_dias):
    sg.theme_background_color(FUNDO)
    window_size = sg.Window.get_screen_size()
    dias_semana = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]
    agenda_dias = agenda_dias

    frames_agendamentos = [
        sg.Frame(
            title=dia,
            layout=[[sg.Text(agenda_dias.get(dia, ""), size=(25, 2), background_color="white", text_color=TEXTO, font="Arial 12", key=f"agenda_{dia.lower()}")]],
            background_color=FUNDO,
            title_color=TEXTO,
            font="Arial 16 bold",
            pad=(10, 10)
        )
        for dia in dias_semana
    ]

    coluna_agendamentos = sg.Column(
        [[frame] for frame in frames_agendamentos],  # Cada frame em uma linha
        background_color=FUNDO,
        element_justification="center",
        vertical_alignment="top",
        pad=(10, 10),  # Permitir rolagem se necessário
        size=(400, 800)  # Ajustar o tamanho da coluna
    )
    
    layout = [
        [sg.Button("✕", key="sair", button_color=("white", "#FF0000"), size=(4, 2), font="Arial 16")],
        [sg.Column(
            [
                [sg.Text("Menu", font="Arial 28 bold", text_color=TEXTO, background_color=FUNDO, justification='left', expand_x=True)],
                [sg.Button("Gerir Pacientes", key="gerir_pacientes", size=(15, 3), button_color=BOTAO_COR, font="Arial 15")],
                [sg.Button("Gerir Médicos", key="gerir_medicos", size=(15, 3), button_color=BOTAO_COR, font="Arial 15")],
                [sg.Button("Gerir Consultas", key="gerir_consultas", size=(15, 3), button_color=BOTAO_COR, font="Arial 15")],
                [sg.Button("Gerir Campanhas", key="gerir_campanhas", size=(15, 3), button_color=BOTAO_COR, font="Arial 15")],
            ],
            background_color=FUNDO,
            element_justification="center",
            vertical_alignment="top",
            pad=(30, 30)
        ),

        sg.Column(
            [
                [sg.Text("Estatística do Hospital", font="Arial 28 bold", text_color=TEXTO, background_color=FUNDO, justification='left', expand_x=True)],
                [sg.Text("Total de Pacientes: 100", font="Arial 15", text_color=TEXTO, background_color=FUNDO, justification='left', expand_x=True)],
                [sg.Text("Total de Médicos: 20", font="Arial 15", text_color=TEXTO, background_color=FUNDO, justification='left', expand_x=True)],
            ],
            background_color=FUNDO,
            element_justification="center",
            vertical_alignment="top",
            pad=(30, 30)
        ),

        sg.Column(
            [
                [sg.Text("Agendamentos", font="Arial 28 bold", text_color=TEXTO, background_color=FUNDO, justification='left', expand_x=True)],
                [coluna_agendamentos]
            ],
            background_color=FUNDO,
            element_justification="center",
            vertical_alignment="top",
            pad=(30, 30)
        ),

        sg.Column(
            [
                [sg.Text("Campanhas", font="Arial 28 bold", text_color=TEXTO, background_color=FUNDO, justification='left', expand_x=True)],
                [sg.Text("Total de Campanhas: 5", font="Arial 15", text_color=TEXTO, background_color=FUNDO, justification='left', expand_x=True)],
                [sg.Text("Campanhas Ativas: 3", font="Arial 15", text_color=TEXTO, background_color=FUNDO, justification='left', expand_x=True)],
                [sg.Text("Campanhas Concluídas: 2", font="Arial 15", text_color=TEXTO, background_color=FUNDO, justification='left', expand_x=True)],
            ],
            background_color=FUNDO,
            element_justification="center",
            vertical_alignment="top",
            pad=(30, 30)
        )]
    ]

    return sg.Window("Menu Principal", layout, finalize=True, background_color=FUNDO, size=window_size, no_titlebar=True, margins=(0,0))

def layout_gerir_pacientes(pacientes):
    window_size = sg.Window.get_screen_size()
    layout = [
        [sg.Button("✕", key="sair", button_color=("white", "#FF0000"), size=(4, 2), font="Arial 16")],
        [sg.Column([
            [
                sg.Text("📋 Lista de Pacientes", font="Arial 20 bold", text_color=TEXTO, background_color=FUNDO, size=(20,1)),
                sg.Text("📋 Detalhes do Paciente", font="Arial 20 bold", text_color=TEXTO, background_color=FUNDO, size=(20,1), pad=((100,100),0)),
                sg.Text("📋 Histórico de Consultas", font="Arial 20 bold", text_color=TEXTO, background_color=FUNDO, size=(20,1))
            ],
            [
                sg.Column([
                    [sg.Listbox(values=[p.nome for p in pacientes], size=(35, 25), key="paciente_selecionado", background_color="white", text_color=TEXTO, font="Arial 12")],
                    [sg.Button("Ver Detalhes", key="ver_detalhes_paciente", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")],
                    [sg.Button("Registar Paciente", key="registar_paciente", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")],
                    [sg.Button("Voltar", key="voltar", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")]
                ], background_color=FUNDO),
                
                sg.Column([
                    [sg.Text("ID: ", size=(30,1), key="id", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Nome: ", size=(30,1), key="nome", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Idade: ", size=(30,1), key="idade", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Sexo: ", size=(30,1), key="sexo", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Grupo de Risco: ", size=(30,1), key="grupo_risco", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Contacto: ", size=(30,1), key="contacto", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Button("Editar", key="editar_paciente", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")],
                    [sg.Button("Eliminar", key="eliminar_paciente", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")]
                ], background_color=FUNDO, pad=((100,170),0)),
                
                sg.Column([
                    [sg.Multiline(size=(35, 25), key="historico_consultas", background_color="white", text_color=TEXTO, font="Arial 12", disabled=True)],
                    [sg.Button("Atualizar Histórico", key="atualizar_historico", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")]
                ], background_color=FUNDO),
            ]
        ], background_color=FUNDO, pad=(30,30))]
    ]
    return sg.Window("Gestão de Pacientes", layout, size=window_size, no_titlebar=True, background_color=FUNDO, finalize=True, margins=(0,0))

def popup_formulario_registar():
    window_size = sg.Window.get_screen_size()
    layout = [
        [sg.Button("✕", key="Cancelar", button_color=("white", "#FF0000"), size=(4, 2), font="Arial 16")],
        [sg.Column([
            [sg.Text("Nome:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="nome", font="Arial 16", size=(30,1))],
            [sg.Text("Data Nascimento (dd-mm-aaaa):", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="data_nascimento", font="Arial 16", size=(30,1))],
            [sg.Text("Sexo:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Combo(["M", "F"], key="sexo", font="Arial 16", size=(28,1))],
            [sg.Text("Grupo Risco:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="grupo", font="Arial 16", size=(30,1))],
            [sg.Text("Contacto:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="contacto", font="Arial 16", size=(30,1))],
            [sg.Button("Guardar", button_color=BOTAO_COR, size=(20, 2), font="Arial 16")]
        ], background_color=FUNDO, pad=(30, 30), element_justification='left')]
    ]
    return sg.Window("Novo Paciente", layout, size=window_size, no_titlebar=True, background_color=FUNDO, margins=(0,0))

def popup_formulario_editar(paciente):
    window_size = sg.Window.get_screen_size()
    layout = [
        [sg.Button("✕", key="Cancelar", button_color=("white", "#FF0000"), size=(4, 2), font="Arial 16")],
        [sg.Column([
            [sg.Text("Nome:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="nome", font="Arial 16", size=(30,1), default_text=paciente.nome)],
            [sg.Text("Data Nascimento (dd-mm-aaaa):", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="data_nascimento", font="Arial 16", size=(30,1), default_text=paciente.data_nascimento)],
            [sg.Text("Sexo:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Combo(["M", "F"], key="sexo", font="Arial 16", size=(28,1), default_value=paciente.sexo)],
            [sg.Text("Grupo Risco:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="grupo", font="Arial 16", size=(30,1), default_text=paciente.grupo_risco)],
            [sg.Text("Contacto:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="contacto", font="Arial 16", size=(30,1), default_text=paciente.contacto)],
            [sg.Button("Guardar", button_color=BOTAO_COR, size=(20, 2), font="Arial 16")]
        ], background_color=FUNDO, pad=(30, 30), element_justification='left')]
    ]
    return sg.Window("Editar Paciente", layout, size=window_size, no_titlebar=True, background_color=FUNDO, margins=(0,0))

def layout_gerir_medicos(medicos):
    window_size = sg.Window.get_screen_size()
    layout = [
        [sg.Button("✕", key="sair", button_color=("white", "#FF0000"), size=(4, 2), font="Arial 16")],
        [sg.Column([
            [
                sg.Text("📋 Lista de Médicos", font="Arial 20 bold", text_color=TEXTO, background_color=FUNDO, size=(20,1)),
                sg.Text("📋 Detalhes do Médico", font="Arial 20 bold", text_color=TEXTO, background_color=FUNDO, size=(20,1), pad=((100,100),0)),
                sg.Text("📋 Horário de Consultas", font="Arial 20 bold", text_color=TEXTO, background_color=FUNDO, size=(20,1))
            ],
            [
                sg.Column([
                    [sg.Listbox(values=[m.nome for m in medicos], size=(35, 25), key="medico_selecionado", background_color="white", text_color=TEXTO, font="Arial 12")],
                    [sg.Button("Ver Detalhes", key="ver_detalhes_medico", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")],
                    [sg.Button("Registar Médico", key="registar_medico", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")],
                    [sg.Button("Voltar", key="voltar", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")]
                ], background_color=FUNDO),
                
                sg.Column([
                    [sg.Text("ID: ", size=(30,1), key="id", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Nome: ", size=(30,1), key="nome", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Idade: ", size=(30,1), key="idade", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Sexo: ", size=(30,1), key="sexo", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Especialidade: ", size=(30,1), key="especialidade", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Contacto: ", size=(30,1), key="contacto", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Button("Editar", key="editar_medico", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")],
                    [sg.Button("Eliminar", key="eliminar_medico", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")]
                ], background_color=FUNDO, pad=((100,170),0)),
                
                sg.Column([
                    [sg.Multiline(size=(35, 25), key="horario_consultas", background_color="white", text_color=TEXTO, font="Arial 12", disabled=True)],
                    [sg.Button("Atualizar Horario", key="atualizar_horario", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")]
                ], background_color=FUNDO)
            ]
        ], background_color=FUNDO, pad=(30,30))]
    ]
    return sg.Window("Gestão de Médicos", layout, size=window_size, no_titlebar=True, background_color=FUNDO, finalize=True, margins=(0,0))

def popup_formulario_registar_medico():
    window_size = sg.Window.get_screen_size()
    layout = [
        [sg.Button("✕", key="Cancelar", button_color=("white", "#FF0000"), size=(4, 2), font="Arial 16")],
        [sg.Column([
            [sg.Text("Nome:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="nome", font="Arial 16", size=(30,1))],
            [sg.Text("Data Nascimento (dd-mm-aaaa):", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="data_nascimento", font="Arial 16", size=(30,1))],
            [sg.Text("Sexo:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Combo(["M", "F"], key="sexo", font="Arial 16", size=(28,1))],
            [sg.Text("Especialidade:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="especialidade", font="Arial 16", size=(30,1))],
            [sg.Text("Contacto:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="contacto", font="Arial 16", size=(30,1))],
            [sg.Button("Guardar", button_color=BOTAO_COR, size=(20, 2), font="Arial 16")]
        ], background_color=FUNDO, pad=(30, 30), element_justification='left')]
    ]
    return sg.Window("Novo Médico", layout, size=window_size, no_titlebar=True, background_color=FUNDO, margins=(0,0))

def popup_formulario_editar_medico(medico):
    window_size = sg.Window.get_screen_size()
    layout = [
        [sg.Button("✕", key="Cancelar", button_color=("white", "#FF0000"), size=(4, 2), font="Arial 16")],
        [sg.Column([
            [sg.Text("Nome:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="nome", font="Arial 16", size=(30,1), default_text=medico.nome)],
            [sg.Text("Data Nascimento (dd-mm-aaaa):", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="data_nascimento", font="Arial 16", size=(30,1), default_text=medico.data_nascimento)],
            [sg.Text("Sexo:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Combo(["M", "F"], key="sexo", font="Arial 16", size=(28,1), default_value=medico.sexo)],
            [sg.Text("Especialidade:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="especialidade", font="Arial 16", size=(30,1), default_text=medico.especialidade)],
            [sg.Text("Contacto:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="contacto", font="Arial 16", size=(30,1), default_text=medico.contacto)],
            [sg.Button("Guardar", button_color=BOTAO_COR, size=(20, 2), font="Arial 16")]
        ], background_color=FUNDO, pad=(30, 30), element_justification='left')]
    ]
    return sg.Window("Editar Medico", layout, size=window_size, no_titlebar=True, background_color=FUNDO, margins=(0,0))

def layout_gerir_consultas(medicos, consultas_semanais="", titulo_semana="Semana Atual"):
    window_size = sg.Window.get_screen_size()
    layout = [
        [sg.Button("✕", key="sair", button_color=("white", "#FF0000"), size=(4, 2), font="Arial 16")],
        [sg.Column([
            [
                sg.Text("📋 Lista de Consultas", font="Arial 20 bold", text_color=TEXTO, background_color=FUNDO, size=(20,1)),
                sg.Text("📋 Detalhes da Consulta", font="Arial 20 bold", text_color=TEXTO, background_color=FUNDO, size=(20,1), pad=((100,100),0)),
                sg.Text("Consultas Semanais", font="Arial 20 bold", text_color=TEXTO, background_color=FUNDO, size=(20,1))
            ],
            [
                sg.Column([
                    [sg.Listbox(values=[consulta for m in medicos for consulta in m.info_agenda()], size=(50, 25), key="consulta_selecionada", background_color="white", text_color=TEXTO, font="Arial 12")],
                    [sg.Button("Ver Detalhes", key="ver_detalhes_consulta", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")],
                    [sg.Button("Agendar Consulta", key="agendar_consulta", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")],
                    [sg.Button("Voltar", key="voltar", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")]
                ], background_color=FUNDO),
                
                sg.Column([
                    [sg.Text("Data: ", size=(30,1), key="data", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Hora: ", size=(30,1), key="hora", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Médico: ", size=(30,1), key="medico", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("ID Médico: ", size=(30,1), key="id_medico", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Especialidade: ", size=(30,1), key="especialidade", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("Paciente: ", size=(30,1), key="paciente", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Text("ID Paciente: ", size=(30,1), key="id_paciente", text_color=TEXTO, background_color=FUNDO, font="Arial 12")],
                    [sg.Button("Editar", key="editar_consulta", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")],
                    [sg.Button("Eliminar", key="eliminar_consulta", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")]
                ], background_color=FUNDO, pad=((100,0),0)),

                sg.Column([
                    [sg.Text(titulo_semana, key="titulo_semana", font="Arial 20 bold", text_color=TEXTO, background_color=FUNDO)],
                    [sg.Multiline(size=(50, 25), key="agenda_semanal", default_text=consultas_semanais, background_color="white", text_color=TEXTO, font="Arial 12", disabled=True)],
                    [sg.Button("Semana Anterior", key="semana_anterior", button_color=BOTAO_COR, size=(15, 2), font="Arial 12"),
                    sg.Button("Semana Seguinte", key="semana_seguinte", button_color=BOTAO_COR, size=(15, 2), font="Arial 12")],
                ], background_color=FUNDO)
            ]
        ], background_color=FUNDO, pad=(30,30))]
    ]
    return sg.Window("Gestão de Consultas", layout, size=window_size, no_titlebar=True, background_color=FUNDO, finalize=True, margins=(0,0))

def popup_formulario_agendar_consulta(medicos, pacientes):
    window_size = sg.Window.get_screen_size()
    layout = [
        [sg.Button("✕", key="Cancelar", button_color=("white", "#FF0000"), size=(4, 2), font="Arial 16")],
        [sg.Column([
            [sg.Text("Data (dd-mm-aaaa):", text_color=TEXTO, background_color=FUNDO, font="Arial 16"),
                sg.Input(key="data", font="Arial 16", size=(30,1))],
            [sg.Text("Hora (hh:mm):", text_color=TEXTO, background_color=FUNDO, font="Arial 16"),
                sg.Input(key="hora", font="Arial 16", size=(30,1))],
            [sg.Text("Médico:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"),
                sg.Combo([m.nome for m in medicos], key="medico", font="Arial 16", size=(28,1), enable_events=True)],
            [sg.Text("ID Médico:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"),
                sg.Input(key="id_medico", font="Arial 16", size=(30,1), readonly=True, disabled_readonly_background_color="white")],
            [sg.Text("Especialidade:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"),
                sg.Input(key="especialidade", font="Arial 16", size=(30,1), readonly=True, disabled_readonly_background_color="white")],
            [sg.Text("Paciente:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"),
                sg.Combo([p.nome for p in pacientes], key="paciente", font="Arial 16", size=(28,1))],
            [sg.Text("ID Paciente:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"),
                sg.Input(key="id_paciente", font="Arial 16", size=(30,1), readonly=True, disabled_readonly_background_color="white")],
            [sg.Button("Guardar", button_color=BOTAO_COR, size=(20, 2), font="Arial 16")]
        ], background_color=FUNDO, pad=(30, 30), element_justification='left')]
    ]
    return sg.Window("Agendar Consulta", layout, size=window_size, no_titlebar=True, background_color=FUNDO, margins=(0,0))

def popup_formulario_editar_consulta(medicos, pacientes, consulta_atual, medico_atual, paciente_atual):
    window_size = sg.Window.get_screen_size()
    layout = [
        [sg.Button("✕", key="Cancelar", button_color=("white", "#FF0000"), size=(4, 2), font="Arial 16")],
        [sg.Column([
            [sg.Text("Data (dd-mm-aaaa):", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="data", font="Arial 16", size=(30,1), default_text=consulta_atual["data"])],
            [sg.Text("Hora (hh:mm):", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Input(key="hora", font="Arial 16", size=(30,1), default_text=consulta_atual["hora"])],
            [sg.Text("Médico:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Combo([m.nome for m in medicos], key="medico", font="Arial 16", size=(28,1), 
                        default_value=medico_atual.nome, enable_events=True)],
            [sg.Text("ID Médico:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"),
                sg.Input(key="id_medico", font="Arial 16", size=(30,1), readonly=True, 
                        default_text=medico_atual.id_medico, disabled_readonly_background_color="white")],
            [sg.Text("Especialidade:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"),
                sg.Input(key="especialidade", font="Arial 16", size=(30,1), readonly=True, 
                        default_text=medico_atual.especialidade, disabled_readonly_background_color="white")],
            [sg.Text("Paciente:", text_color=TEXTO, background_color=FUNDO, font="Arial 16"), 
                sg.Combo([p.nome for p in pacientes], key="paciente", font="Arial 16", size=(28,1),
                        default_value=paciente_atual.nome)],
            [sg.Button("Guardar", button_color=BOTAO_COR, size=(20, 2), font="Arial 16")]
        ], background_color=FUNDO, pad=(30, 30), element_justification='left')]
    ]
    return sg.Window("Editar Consulta", layout, size=window_size, no_titlebar=True, background_color=FUNDO, margins=(0,0))

def layout_gerir_campanhas():
    window_size = sg.Window.get_screen_size()
    layout = [
        [sg.Button("✕", key="sair", button_color=("white", "#FF0000"), size=(4, 2), font="Arial 12")]
        # ...existing code...
    ]
    return sg.Window("Gestão de Campanhas", layout, size=window_size, no_titlebar=True, background_color=FUNDO, margins=(0,0))
