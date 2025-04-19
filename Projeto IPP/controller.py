import PySimpleGUI as sg
from model import *
from view import *

window_menu = layout_menu_principal()
window_gerir_pacientes = None
window_gerir_medicos = None
pacientes = carregar_pacientes()
medicos = carregar_medicos()

while True:
    window, event, values = sg.read_all_windows()

    if window == window_menu:
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
            
    elif window == window_gerir_pacientes:
        if event == sg.WINDOW_CLOSED or event == "voltar" or event == "sair":
            window_gerir_pacientes.close()
            window_menu = layout_menu_principal()
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
        if event == sg.WINDOW_CLOSED or event == "voltar" or event == "sair":
            window_gerir_medicos.close()
            window_menu = layout_menu_principal()
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
            else:
                sg.popup("Seleciona um médico primeiro.")
        
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






