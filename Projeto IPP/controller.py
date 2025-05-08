import PySimpleGUI as sg
from model import *
from view import *

pacientes = carregar_pacientes()
medicos = carregar_medicos()
data_atual = datetime.today()
agenda_dias_menu, _ = gerar_agenda_semanal(medicos, pacientes, data_atual, 0)  
agenda_dias, data_semana = gerar_agenda_semanal(medicos, pacientes, data_atual, 0) 
dias_semana = ["segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo"]
window_menu = layout_menu_principal(agenda_dias)
window_gerir_pacientes = None
window_gerir_medicos = None
window_gerir_consultas = None
semana_offset_consultas = 0
semana_offset = 0
menu_semana_offset = 0

while True:
    window, event, values = sg.read_all_windows()

    if window == window_menu:

    # Atualizar a coluna de "Agendamentos" com as consultas da semana
        for dia in dias_semana:
            if agenda_dias_menu.get(dia.capitalize()):
                window[f"agenda_{dia}"].update(agenda_dias_menu[dia.capitalize()])

        if event == sg.WINDOW_CLOSED or event == "sair":
            break

        elif event == "gerir_pacientes":
            pacientes = carregar_pacientes()
            window_gerir_pacientes = layout_gerir_pacientes(pacientes)
            window_menu.close()
        
        elif event == "gerir_medicos":
            medicos = carregar_medicos()
            window_gerir_medicos = layout_gerir_medicos(medicos)
            window_menu.close()  

        elif event == "gerir_consultas":
            # Gerar as consultas da semana atual
            agenda_dias, data_semana = gerar_agenda_semanal(medicos, pacientes, data_atual, semana_offset)
            consultas_semanais = ""
            for dia, consultas in agenda_dias.items():
                consultas_semanais += f"{dia.capitalize()}:\n{consultas}\n\n"

            # Criar a janela de "Gerir Consultas" com as consultas semanais
            window_gerir_consultas = layout_gerir_consultas(medicos, consultas_semanais, titulo_semana="Semana Atual")
            window_menu.close()
            
    elif window == window_gerir_pacientes:
        if event == sg.WINDOW_CLOSED or event == "voltar" or event == "sair":
            window_gerir_pacientes.close()
            window_menu = layout_menu_principal(agenda_dias_menu)
            window_gerir_pacientes = None
            continue

        elif event == "ver_detalhes_paciente":
            selecionado = values["paciente_selecionado"]
            if selecionado:
                nome = selecionado[0]
                paciente = next((p for p in pacientes if p.nome == nome), None)
                if paciente:
                    info = paciente.info_paciente()
                    window["id"].update(f"ID: {info['id']}")
                    window["nome"].update(f"Nome: {info['nome']}")
                    window["idade"].update(f"Idade: {info['idade']} anos")
                    window["sexo"].update(f"Sexo: {info['sexo']}")
                    window["grupo_risco"].update(f"Grupo de Risco: {info['grupo_risco']}")
                    window["contacto"].update(f"Contacto: {info['contacto']}")
                    window["historico_consultas"].update(paciente.ver_historico())
            else:
                sg.popup("Seleciona um paciente primeiro.")
            


        elif event == "registar_paciente":
            popup = popup_formulario_registar()
    
            while True:
                evento_popup, valores_popup = popup.read()
                if evento_popup == "Cancelar" or evento_popup == sg.WINDOW_CLOSED:
                    popup.close()
                    break

                elif evento_popup == "Guardar":
                    try:
                        novo = Paciente(
                            id_paciente=len(pacientes) + 1,
                            nome=valores_popup["nome"],
                            data_nascimento=valores_popup["data_nascimento"],
                            sexo=valores_popup["sexo"],
                            grupo_risco=valores_popup["grupo"],
                            contacto=valores_popup["contacto"]
                        )
                        pacientes.append(novo)
                        guardar_pacientes(pacientes)
                        sg.popup("Paciente adicionado com sucesso!")
                        popup.close()
                        window["paciente_selecionado"].update(values=[p.nome for p in pacientes])
                        break
                    except Exception as e:
                        sg.popup("Erro ao adicionar paciente:", str(e))
        
        elif event == "editar_paciente":
            selecionado = values["paciente_selecionado"]
            if selecionado:
                nome = selecionado[0]
                paciente = next((p for p in pacientes if p.nome == nome), None)
                if paciente:
                    popup = popup_formulario_editar(paciente)

                    while True:
                        evento_popup, valores_popup = popup.read()
                        if evento_popup == "Cancelar" or evento_popup == sg.WINDOW_CLOSED:
                            popup.close()
                            break

                        elif evento_popup == "Guardar":
                            try:
                                index = pacientes.index(paciente)
                                paciente_atualizado = Paciente(
                                    id_paciente=paciente.id_paciente,
                                    nome=valores_popup["nome"],
                                    data_nascimento=valores_popup["data_nascimento"],
                                    sexo=valores_popup["sexo"],
                                    grupo_risco=valores_popup["grupo"],
                                    contacto=valores_popup["contacto"]
                                )
                                pacientes[index] = paciente_atualizado
                                guardar_pacientes(pacientes)
                                sg.popup("Paciente editado com sucesso!")
                                popup.close()
                                window["paciente_selecionado"].update(values=[p.nome for p in pacientes])
                                info = paciente_atualizado.info_paciente()
                                window["id"].update(f"ID: {info['id']}")
                                window["nome"].update(f"Nome: {info['nome']}")
                                window["idade"].update(f"Idade: {info['idade']} anos")
                                window["sexo"].update(f"Sexo: {info['sexo']}")
                                window["grupo_risco"].update(f"Grupo de Risco: {info['grupo_risco']}")
                                window["contacto"].update(f"Contacto: {info['contacto']}")
                                break
                            except Exception as e:
                                sg.popup("Erro ao editar paciente:", str(e))

        elif event == "eliminar_paciente":
            selecionado = values["paciente_selecionado"]
            if selecionado:
                nome = selecionado[0]
                paciente = next((p for p in pacientes if p.nome == nome), None)
                if paciente:
                    if sg.popup_yes_no("Tem certeza que deseja eliminar este paciente?", title="Confirmar eliminação") == "Yes":
                        try:
                            pacientes.remove(paciente)
                            guardar_pacientes(pacientes)
                            sg.popup("Paciente eliminado com sucesso!")
                            window["id"].update("ID: ")
                            window["nome"].update("Nome: ")
                            window["idade"].update("Idade: ")
                            window["sexo"].update("Sexo: ")
                            window["grupo_risco"].update("Grupo de Risco: ")
                            window["contacto"].update("Contacto: ")
                            window["paciente_selecionado"].update(values=[p.nome for p in pacientes])
                        except Exception as e:
                            sg.popup("Erro ao eliminar paciente:", str(e))
            else:
                sg.popup("Seleciona um paciente primeiro.")
    
    elif window == window_gerir_medicos:
        current_offset = 0  # Track which week we're viewing
        current_medico = None  # Track selected medico
        
        semana_offset = 0  # Variável para controlar qual semana mostrar

        if event == sg.WINDOW_CLOSED or event == "voltar" or event == "sair":
            window_gerir_medicos.close()
            window_menu = layout_menu_principal(agenda_dias_menu)
            window_gerir_medicos = None
            continue

        elif event == "ver_detalhes_medico":
            selecionado = values["medico_selecionado"]
            if selecionado:
                nome = selecionado[0]
                medico = next((m for m in medicos if m.nome == nome), None)
                if medico:
                    info = medico.info_medico()
                    window["id"].update(f"ID: {info['id']}")
                    window["nome"].update(f"Nome: {info['nome']}")
                    window["idade"].update(f"Idade: {info['idade']} anos")
                    window["sexo"].update(f"Sexo: {info['sexo']}")
                    window["especialidade"].update(f"Especialidade: {info['especialidade']}")
                    window["contacto"].update(f"Contacto: {info['contacto']}")
                    semana = medico.get_semana_disponibilidade(semana_offset)
                    window["disponibilidade_semanal"].update(medico.formatar_horario_disponibilidade(semana))

        elif event == "semana_anterior":
            if values["medico_selecionado"]:
                semana_offset -= 1
                medico = next((m for m in medicos if m.nome == values["medico_selecionado"][0]), None)
                if medico:
                    semana = medico.get_semana_disponibilidade(semana_offset)
                    window["disponibilidade_semanal"].update(medico.formatar_horario_disponibilidade(semana))

        elif event == "semana_seguinte":
            if values["medico_selecionado"]:
                semana_offset += 1
                medico = next((m for m in medicos if m.nome == values["medico_selecionado"][0]), None)
                if medico:
                    semana = medico.get_semana_disponibilidade(semana_offset)
                    window["disponibilidade_semanal"].update(medico.formatar_horario_disponibilidade(semana))

        elif event == "registar_medico":
            popup = popup_formulario_registar_medico()
    
            while True:
                evento_popup, valores_popup = popup.read()
                if evento_popup == "Cancelar" or evento_popup == sg.WINDOW_CLOSED:
                    popup.close()
                    break

                elif evento_popup == "Guardar":
                    try:
                        novo = Medico(
                            id_medico=len(medicos) + 1,
                            nome=valores_popup["nome"],
                            data_nascimento=valores_popup["data_nascimento"],
                            sexo=valores_popup["sexo"],
                            especialidade=valores_popup["especialidade"],
                            contacto=valores_popup["contacto"]
                        )
                        medicos.append(novo)
                        guardar_medicos(medicos)
                        sg.popup("Medico adicionado com sucesso!")
                        popup.close()
                        window["medico_selecionado"].update(values=[m.nome for m in medicos])
                        break
                    except Exception as e:
                        sg.popup("Erro ao adicionar medico:", str(e))
        
        elif event == "editar_medico": 
            selecionado = values["medico_selecionado"]
            if selecionado:
                nome = selecionado[0]
                medico = next((m for m in medicos if m.nome == nome), None)
                if medico:
                    popup = popup_formulario_editar_medico(medico)

                    while True:
                        evento_popup, valores_popup = popup.read()
                        if evento_popup == "Cancelar" or evento_popup == sg.WINDOW_CLOSED:
                            popup.close()
                            break

                        elif evento_popup == "Guardar":
                            try:
                                index = medicos.index(medico)
                                medico_atualizado = Medico(
                                    id_medico=medico.id_medico,
                                    nome=valores_popup["nome"],
                                    data_nascimento=valores_popup["data_nascimento"],
                                    sexo=valores_popup["sexo"],
                                    especialidade=valores_popup["especialidade"],
                                    contacto=valores_popup["contacto"]
                                )
                                medicos[index] = medico_atualizado
                                guardar_medicos(medicos)
                                sg.popup("Medico editado com sucesso!")
                                popup.close()
                                window["medico_selecionado"].update(values=[m.nome for m in medicos])
                                info = medico_atualizado.info_medico()
                                window["id"].update(f"ID: {info['id']}")
                                window["nome"].update(f"Nome: {info['nome']}")
                                window["idade"].update(f"Idade: {info['idade']} anos")
                                window["sexo"].update(f"Sexo: {info['sexo']}")
                                window["especialidade"].update(f"Especialidade: {info['especialidade']}")
                                window["contacto"].update(f"Contacto: {info['contacto']}")
                                break
                            except Exception as e:
                                sg.popup("Erro ao editar medico:", str(e))

        elif event == "eliminar_medico":
            selecionado = values["medico_selecionado"]
            if selecionado:
                nome = selecionado[0]
                medico = next((m for m in medicos if m.nome == nome), None)
                if medico:  
                    if sg.popup_yes_no("Tem certeza que deseja eliminar este médico?", title="Confirmar eliminação") == "Yes":
                        try:
                            medicos.remove(medico)
                            guardar_medicos(medicos)
                            sg.popup("Médico eliminado com sucesso!")
                            window["id"].update("ID: ")
                            window["nome"].update("Nome: ")
                            window["idade"].update("Idade: ")
                            window["sexo"].update("Sexo: ")
                            window["especialidade"].update("Especialidade: ")
                            window["contacto"].update("Contacto: ")
                            window["medico_selecionado"].update(values=[m.nome for m in medicos]) 
                        except Exception as e:
                            sg.popup("Erro ao eliminar medico:", str(e))
            else:
                sg.popup("Seleciona um medico primeiro.")


    elif window == window_gerir_consultas:
        if event == sg.WINDOW_CLOSED or event == "voltar" or event == "sair":
            window_gerir_consultas.close()
            window_menu = layout_menu_principal(agenda_dias_menu)
            window_gerir_consultas = None
            continue
            
        elif event == "ver_agenda_semanal":
            agenda_dias, data_semana = gerar_agenda_semanal(medicos, pacientes, data_atual, semana_offset)
            consultas_semanais = ""
            for dia, consultas in agenda_dias.items():
                consultas_semanais += f"{dia.capitalize()}:\n{consultas}\n\n"
            window["agenda_semanal"].update(consultas_semanais.strip())

        elif event == "semana_anterior":
            semana_offset -= 1
            agenda_dias, data_semana = gerar_agenda_semanal(medicos, pacientes, data_atual, semana_offset)
            consultas_semanais = ""
            for dia, consultas in agenda_dias.items():
                consultas_semanais += f"{dia.capitalize()}:\n{consultas}\n\n"
            window["agenda_semanal"].update(consultas_semanais.strip())
            window["titulo_semana"].update(f"Semana de {data_semana}")

        elif event == "semana_seguinte":
            semana_offset += 1
            agenda_dias, data_semana = gerar_agenda_semanal(medicos, pacientes, data_atual, semana_offset)
            consultas_semanais = ""
            for dia, consultas in agenda_dias.items():
                consultas_semanais += f"{dia.capitalize()}:\n{consultas}\n\n"
            window["agenda_semanal"].update(consultas_semanais.strip())
            window["titulo_semana"].update(f"Semana de {data_semana}")
        
        elif event == "ver_detalhes_consulta":
            selecionado = values["consulta_selecionada"]
    
            if selecionado:
                linha = selecionado[0]
                
                partes = linha.split(" às ")
                data = partes[0]
                restante = partes[1].split(" - ")
                hora = restante[0]
                nome_medico = restante[1].split(" (")[0]

                medico = next((m for m in medicos if m.nome == nome_medico), None)

                if medico:
                    consulta = next((c for c in medico.consultas_agendadas if c["data"] == data and c["hora"] == hora), None)

                    if consulta:
                        id_paciente = consulta.get("id_paciente")
                        paciente = next((p for p in pacientes if p.id_paciente == id_paciente), None)

                        info_medico = medico.info_medico()
                        info_paciente = paciente.info_paciente() if paciente else {"nome": "Desconhecido", "id": "-"}

                        window["data"].update(f"Data: {data}")
                        window["hora"].update(f"Hora: {hora}")
                        window["medico"].update(f"Médico: {info_medico['nome']}")
                        window["id_medico"].update(f"ID Médico: {info_medico['id']}")
                        window["especialidade"].update(f"Especialidade: {info_medico['especialidade']}")
                        window["paciente"].update(f"Paciente: {info_paciente['nome']}")
                        window["id_paciente"].update(f"ID Paciente: {info_paciente['id']}")
                        
                    else:
                        sg.popup("Seleciona uma consulta primeiro.")
        
        elif event == "agendar_consulta":
            popup = popup_formulario_agendar_consulta(medicos, pacientes)
    
            while True:
                evento_popup, valores_popup = popup.read()
                if evento_popup == sg.WIN_CLOSED or evento_popup == "Cancelar":
                    popup.close()
                    break
                
                elif evento_popup == "medico":
                    selected_medico = next((m for m in medicos if m.nome == valores_popup["medico"]), None)
                    if selected_medico:
                        popup["id_medico"].update(selected_medico.id_medico)
                        popup["especialidade"].update(selected_medico.especialidade)

                elif evento_popup == "Guardar":
                    try:
                        data = valores_popup["data"]
                        hora = valores_popup["hora"]
                        # Validate date/time format
                        datetime.strptime(data, "%d-%m-%Y")
                        datetime.strptime(hora, "%H:%M")
                        
                        medico = next((m for m in medicos if m.nome == valores_popup["medico"]), None)
                        paciente = next((p for p in pacientes if p.nome == valores_popup["paciente"]), None)

                        if medico and paciente:
                            # Use the class methods properly
                            if medico.agendar_consulta(data, hora, paciente.id_paciente):
                                # If successful, update patient's appointments
                                paciente.agendar_consulta(data, hora, medico.id_medico)
                                medico.agendar_consulta(data, hora, paciente.id_paciente)
                                guardar_medicos(medicos)
                                guardar_pacientes(pacientes)
                                sg.popup("Consulta agendada com sucesso!")
                                popup.close()
                                # Update consultation list
                                window["consulta_selecionada"].update(
                                    values=[consulta for m in medicos for consulta in m.info_agenda()]
                                )
                                break
                            else:
                                sg.popup("Médico não está disponível nesta data/hora.")
                        else:
                            sg.popup("Selecione um médico e um paciente.")
                    except ValueError:
                        sg.popup("Formato de data ou hora inválido.\nUse dd-mm-aaaa para data e hh:mm para hora.")
                    except Exception as e:
                        sg.popup(f"Erro ao agendar consulta: {str(e)}")
            
        elif event == "eliminar_consulta":
            selecionado = values["consulta_selecionada"]
            if selecionado:
                linha = selecionado[0]
                
                partes = linha.split(" às ")
                data = partes[0]
                restante = partes[1].split(" - ")
                hora = restante[0]
                nome_medico = restante[1].split(" (")[0]

                medico = next((m for m in medicos if m.nome == nome_medico), None)

                if medico:
                    consulta = next((c for c in medico.consultas_agendadas if c["data"] == data and c["hora"] == hora), None)

                    if consulta:
                        id_paciente = consulta.get("id_paciente")
                        paciente = next((p for p in pacientes if p.id_paciente == id_paciente), None)

                        if sg.popup_yes_no("Tem certeza que deseja eliminar esta consulta?", title="Confirmar eliminação") == "Yes":
                            try:
                                medico.consultas_agendadas.remove(consulta)
                                paciente.consultas_agendadas.remove(consulta)
                                guardar_medicos(medicos)
                                guardar_pacientes(pacientes)
                                sg.popup("Consulta eliminada com sucesso!")
                                window["consulta_selecionada"].update(values=[consulta for m in medicos for consulta in m.info_agenda()])
                            except Exception as e:
                                sg.popup("Erro ao eliminar consulta:", str(e))
                    else:
                        sg.popup("Seleciona uma consulta primeiro.")
        
        elif event == "editar_consulta":
            selecionado = values["consulta_selecionada"]
            if selecionado:
                linha = selecionado[0]
                partes = linha.split(" às ")
                data = partes[0]
                restante = partes[1].split(" - ")
                hora = restante[0]
                nome_medico = restante[1].split(" (")[0]

                medico_atual = next((m for m in medicos if m.nome == nome_medico), None)
                if medico_atual:
                    consulta_atual = next((c for c in medico_atual.consultas_agendadas 
                                         if c["data"] == data and c["hora"] == hora), None)
                    if consulta_atual:
                        paciente_atual = next((p for p in pacientes 
                                             if p.id_paciente == consulta_atual["id_paciente"]), None)
                        
                        if paciente_atual:
                            # Abrir popup de edição com os dados atuais
                            popup = popup_formulario_editar_consulta(medicos, pacientes, consulta_atual, medico_atual, paciente_atual)

                            while True:
                                evento_popup, valores_popup = popup.read()
                                if evento_popup == sg.WIN_CLOSED or evento_popup == "Cancelar":
                                    popup.close()
                                    break

                                elif evento_popup == "medico":
                                    # Atualizar ID e especialidade ao mudar médico
                                    selected_medico = next((m for m in medicos if m.nome == valores_popup["medico"]), None)
                                    if selected_medico:
                                        popup["id_medico"].update(selected_medico.id_medico)
                                        popup["especialidade"].update(selected_medico.especialidade)

                                elif evento_popup == "Guardar":
                                    try:
                                        # Remover consulta antiga
                                        medico_atual.eliminar_consulta(data, hora)
                                        
                                        # Pegar novo médico e paciente
                                        novo_medico = next((m for m in medicos if m.nome == valores_popup["medico"]), None)
                                        novo_paciente = next((p for p in pacientes if p.nome == valores_popup["paciente"]), None)
                                        
                                        if novo_medico and novo_paciente:
                                            # Agendar nova consulta
                                            if novo_medico.agendar_consulta(
                                                valores_popup["data"], 
                                                valores_popup["hora"], 
                                                novo_paciente.id_paciente
                                            ):
                                                guardar_medicos(medicos)
                                                guardar_pacientes(pacientes)
                                                sg.popup("Consulta atualizada com sucesso!")
                                                popup.close()
                                                # Atualizar lista de consultas
                                                window["consulta_selecionada"].update(
                                                    values=[consulta for m in medicos for consulta in m.info_agenda()]
                                                )
                                                break
                                            else:
                                                sg.popup("Horário não disponível para o médico selecionado.")
                                        else:
                                            sg.popup("Médico ou paciente não encontrado.")
                                    except ValueError:
                                        sg.popup("Formato de data ou hora inválido.")
                                    except Exception as e:
                                        sg.popup(f"Erro ao atualizar consulta: {str(e)}")
                            
            else:
                sg.popup("Selecione uma consulta primeiro.")


