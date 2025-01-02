# Relatório do Projeto: Sistema de Gestão de Publicações Científicas

## Autores
José Ferriera, A107278
Filipa Figueiredo, A107239
Andreia Ferreira, A107234

## Data
03/03/2025

## Visão Geral
No ambito da unidade curricular Algoritmos e Técnicas de Programação foi nos proposto o desenvolvimento de um sistema de gestão de publicações científicas em Python.

## Requesitos do Sistema
Em relação ao sistema que nos foi propsoto desenvolver havia alguns requesitos essenciais que o sistema devia ter deforma a analisar com efeciencia uma base de dados fornecida com as publicações cientificas.
Requisitos:
### 1. Carregar Base de Dados
O programa deve ser capaz, antes de tudo, de carregar para a memória interna o conjunto de dados presente num ficheiro JSON com a seguinte estrutura:

    ```json
    [
        {
            "title": "Título da publicação",
            "abstract": "Resumo do conteúdo da publicação",
            "keywords": "Palavras-chave relacionadas com a publicação",
            "authors": [
                {
                    "name": "Nome do autor",
                    "affiliation": "Nome da afiliação do autor",
                    "orcid": "Identificador aberto de investigador e contribuidor"
                }
            ],
            "doi": "Identificador de objeto digital",
            "pdf": "Caminho do ficheiro PDF da publicação",
            "publish_date": "Data da publicação (AAAA-MM-DD)",
            "url": "Endereço web da publicação"
        }
    ]
    ```
O dataset consiste numa lista de dicionários e cada um corresponde a um publicação. Dentro destes há "Keys" para título, resumo, palavras-chave, autores, DOI, PDF, data de publicação e URL. em relação aos autores estes são mais uma lista de dicionários em que cada dicionário corresponde a um autor onde estão presente as Keys para nome, afiliação e ORCID

### 2. Criar Publicações
O programa deve permitir que o utilizador crie uma nova publicação, especificando título, resumo, palavras-chave, DOI, autores (com nome, afiliação e ORCID), caminho para o PDF, data da publicação e URL da publicação.

### 3. Atualizar Publicações
O programa deve permitir que o utilizador atualize as informações de uma dada publicação. Estas informações incluem o título, resumo, palavras-chave, autores (nome, afiliação e ORCID), DOI, caminho para o PDF, data da publicação e URL da publicação.

### 4. Consultar Publicações
O programa deve permitir que o utilizador consulte as publicações através de filtros por título, autor, afiliação, data de publicação e palavras-chave. Após encontrar as publicações, deve ainda ser possível ordená-las pelos títulos e pela data de publicação.

### 5. Analisar Publicações por Autor
O programa deve permitir que os autores sejam listados de modo a que o utilizador possa ver as publicações correspondentes a um dado autor. Esta listagem de autores deve ser ordenada pela frequência de publicações e/ou por ordem alfabética.

### 6. Analisar Publicações por Palavras-Chave
O programa deve permitir a visualização das palavras-chave existentes no conjunto de dados, de modo a que o utilizador possa visualizar as publicações correspondentes a uma dada palavra-chave. As palavras-chave devem aparecer ordenadas pela sua frequência e/ou por ordem alfabética.

### 7. Estatísticas das Publicações
O programa deve permitir que o utilizador veja estatísticas referentes às publicações presentes no conjunto de dados. Estas estatísticas devem ser apresentadas como gráficos para os seguintes tópicos:
- Distribuição de publicações por ano.
- Distribuição de publicações por mês de um determinado ano.
- Número de publicações por autor (top 20 autores).
- Distribuição de publicações de um autor por anos.
- Distribuição de palavras-chave pela sua frequência (top 20 palavras-chave).
- Distribuição de palavras-chave mais frequente por ano

### 8. Armazenamento dos Dados
O programa deve guardar as informações alteradas ou adicionadas em memória no ficheiro de suporte.

### 9. Importação de Dados
O programa deve permitir que, a qualquer momento, seja possível importar novos registos de um outro conjunto de dados com a mesma estrutura mencionada anteriormente.

### 10. Exportação Parcial de Dados
O programa deve permitir que seja possível exportar para um ficheiro os registos resultantes de uma pesquisa.

## Algoritmo
### Tecnologias Utilizadas
- Python
- PySimpleGUI
- Matplotlib
- JSON

### Importação de Bibliotecas e Módulos
Para o desenvolvimento de sistema foi necessária a importação de bibliotecas e módulos de modo a conseguir realizar o programa da forma mais efeciente possível. As bibliotecas e os módulos em questão são:
- ```import PySimpleGUI as sg```
    - PySimpleGUI é uma biblioteca que simplifica a criação de interfaces gráficas em Python. 
    - No contexto de projeto esta biblioteca foi utilizada para desenvolver toda a interface do sistema de forma clara e objetiva.
- ```from datetime import datetime```
    - datetime é um módulo da biblioteca padrão do Python que fornece classes para manipulação de datas e horas.
    - No contexto do projeto este módulo foi utilizado para uma melhor manipulação das datas de forma a tornar o código mais efeciente.
- ```import webbrowser```
    - webbrowser é um módulo da biblioteca padrão do Python que permite a interação com URL para abrir diretamente na Web.
    - No contexto do projeto foi utilizado para ser possível ter uma interação com os links fornecidos nas publicações.
- ```import json```
    - json é um módulo da biblioteca padrão do Python que fornece uma maneira simples de codificar e decodificar dados no formato JSON (JavaScript Object Notation). Ele é usado para ler e escrever dados em arquivos JSON.
    - No contexto do programa, uma vez que o dataset se encontrava guardado em um ficheiro JSON, esta biblioteca foi usada para conseguir ler e escrever os dados das publicações
- ```import matplotlib.pyplot as plt```
    - matplotlib.pyplot é um módulo da biblioteca Matplotlib que fornece uma interface de estilo MATLAB para a criação de gráficos e visualizações. 
    - No contexto do programa este módulo da biblioteca Matplotlib foi usado para representar gráficamente as estatísticas requeridas pela inunciado.
- ```from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg```
    - FigureCanvasTkAgg é uma classe do módulo matplotlib.backends.backend_tkagg que permite integrar gráficos Matplotlib em interfaces Tkinter. Ele é usado para desenhar gráficos em um widget Tkinter Canvas
    - No contexto do programa este módulo foi necessário para apresentar os gráficos na interface da melhor forma possível.

### 1. Gestão de Ficheiros
#### 1.1 Carregar ficheiros JSON
Para carregar o dataset presente no ficheiro JSON, com a estrutura anterior mente mencionada, foi utilizado código já desenvolvido nas aulas com algumas adaptações para a interface.
``` py
def carregar(caminho_ficheiro):
    try:
        with open(caminho_ficheiro, 'r', encoding ='utf-8') as file:
            return json.load(file)
    except Exception as e:
        sg.popup_error(f"Error loading file: {e}")
        return None 
```

#### 1.2 Guardar publicações
Para guardar as publicações atualizadas ou criadas foi necessário desenvolver uma função para guardar os dados no mesmo ficheiro que foram carregados.
``` py
def guardar(caminho_ficheiro, dados):
    try:
        with open(caminho_ficheiro, 'w', encoding='utf-8') as file:
            json.dump(dados, file, indent=4)
            sg.popup("File saved successfully!")
    except Exception as e:
        sg.popup_error(f"Error saving file: {e}")
```

#### 1.3 Exportar resultados de pesquisa
Para exportar resultados de uma pesquisa desenvolvemos duas maneiras possíveis para o fazer.
- Uma que permite exportar em formato txt com uma estrutura defenida por nós
```py
def guardar(caminho_ficheiro, dados):
    try:
        with open(caminho_ficheiro, 'w', encoding='utf-8') as file:
            json.dump(dados, file, indent=4)
            sg.popup("File saved successfully!")
    except Exception as e:
        sg.popup_error(f"Error saving file: {e}")
```
- Outra que permite exportar em formato de json com a mesma estrutura do dataset

```py
elif event_save == "-SAVE_JSON-":
    caminho_arquivo_save = sg.popup_get_file("Save as", save_as=True, no_window=True, file_types=(("JSON Files", "*.json"),))
    if caminho_arquivo_save:
        try:
            with open(caminho_arquivo_save, 'r', encoding='utf-8') as file:
                dados_existentes = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            dados_existentes = []

        if isinstance(dados, list):
            dados_existentes.extend(dados)
        else:
            dados_existentes.append(dados)

        guardar(caminho_arquivo_save, dados_existentes)
```


### 2. Gestão de Publicações
#### 2.1 Adicionar novas publicações
Para adicionar novas publicações desenolvemos uma interface clara onde é possivel inserir todas as informações da publicação tendo como obrigatoriedade o título e o DOI, uma vez que são parametros importantes para a identificação da publicação como no exemplo a seguir:

<p align="center">
    <img src="Fotos%20Projeto/Add%20Publication%20.png" alt="logo" width="600"/>
</p>

```py
def criar_publicacoes(publicacoes, values, autores, keywords):
    title = values["-TITLE-"]
    abstract = values["-ABSTRACT-"]
    doi = values["-DOI-"]
    pdf = values["-PDF-"]
    url = values["-URL-"]
    publish_date = values["-PUBLISH_DATE-"]

    if verificar_duplicados(publicacoes, title, doi):
        return False 
    
    nova_publicacao = {
        "title": title,
        "abstract": abstract,
        "doi": doi,
        "pdf": pdf,
        "url": url,
        "publish_date": publish_date,
        "autores": autores,
        "keywords": keywords
    }

    publicacoes.append(nova_publicacao)
    return True
```

Para adicionar novas palavras-chave e novos autores, as seguintes janelas são apresentadas ao utilizador:
<p align="center">
    <img src="Fotos%20Projeto/Add%20Keyword.png" alt="Descrição da Imagem" width="400"/>
    <img src="Fotos%20Projeto/Add%20Author.png" alt="Descrição da Imagem" width="400"/>
</p>


Caso o utilizador deseje remover alguma das palavras-chave ou autores que tenham adicionado, as seguintes janelas são apresentadas ao utilizador:
<p align="center">
    <img src="Fotos%20Projeto/Remove%20Keyword.png" alt="Descrição da Imagem" width="400"/>
    <img src="Fotos%20Projeto/Remove%20Author.png" alt="Descrição da Imagem" width="400"/>
</p>

```py
def remover_keywords(window, values, keywords):
    selected_keywords = values["-KEYWORDS-"]
    if selected_keywords:
        if sg.popup_yes_no("Confirm", "Are you sure you want to remove the selected keywords?", 
                          icon=sg.SYSTEM_TRAY_MESSAGE_ICON_WARNING) == "Yes":
            keywords_list = keywords.split(", ")
            for keyword in selected_keywords:
                if keyword in keywords_list:
                    keywords_list.remove(keyword)
            keywords = ", ".join(keywords_list)
            window["-KEYWORDS-"].update(keywords_list)
    else:
        sg.popup("Please select a keyword to remove", title="No Selection")
    return keywords

def remover_autores(window_popup, autores, selected_authors):
    for author in selected_authors:
        for autor in autores:
            if f"Name: {autor['name']}; Affiliation: {autor['affiliation']}" == author:
                autores.remove(autor)
    authors_info = [f"Name: {autor['name']}; Affiliation: {autor['affiliation']}" for autor in autores]
    window_popup["-AUTHORS-"].update(authors_info)
    return autores

```

Em caso do utilizador tentar guardar a publicação sem título ou DOI, um aviso será mostrado como no exemplo a seguir:
<p align="center">
    <img src="Fotos%20Projeto/Title%20or%20DOI.png" alt="logo" width="300"/>
</p>

Se porventura for inserido um título ou um DOI já existente, um aviso será mostrado como no exemplo a seguir:
<p align="center">
    <img src="Fotos%20Projeto/Duplicated%20Title.png" alt="Descrição da Imagem" width="300"/>
    <img src="Fotos%20Projeto/Duplicated%20DOI.png" alt="Descrição da Imagem" width="300"/>
</p>

```py
def verificar_duplicados(publicacoes, title, doi, current_pub=None):
    for publicacao in publicacoes:
        if publicacao != current_pub: 
            if title and title.strip() == publicacao.get("title", ""):
                sg.popup("Title already exists in dataset")
                return True
            
            if doi and doi.strip() == publicacao.get("doi", ""):
                sg.popup("DOI already exists in dataset") 
                return True       
    return False
```

Após inserir as informações corretamente e guardar a nova publicação, a janela seguinte será exposta:
<p align="center">
    <img src="Fotos%20Projeto/File%20Saved.png" alt="logo" width="300"/>
</p>

#### 2.2 Atualizar publicações existentes
Para atualizar as informações de uma publicação já existente no dataset desenvolvemos uma interface clara onde serão exibidos todos os parâmentros devidamente preenchidos com as informações da publicação mas com a possibilidade de mudar. Apesar da estrutura e de funções muito semelhante à janela de adicionar publicação, esta apresenta dois novos botões: "Edit" para editar autores já existentes, e "Delete Post" para apagar a publicação do dataset.
<p align="center">
    <img src="Fotos%20Projeto/Edit%20Publication.png" alt="logo" width="600"/>
</p>

```py
def atualizar_publicacao(values, keywords, autores, publicacao_encontrada, caminho_ficheiro, publicacoes):
    title = values["-EDIT_TITLE-"].strip()
    doi = values["-EDIT_DOI-"].strip()

    if verificar_duplicados(publicacoes, title, doi, publicacao_encontrada):
        return
    
    updated_publication = {
        "title": values["-EDIT_TITLE-"].strip(),
        "abstract": values["-EDIT_ABSTRACT-"].strip(),
        "publish_date": values["-EDIT_DATE-"].strip(),
        "doi": values["-EDIT_DOI-"].strip(),
        "pdf": values["-EDIT_PDF-"].strip(),
        "url": values["-EDIT_URL-"].strip(),
        "keywords": keywords,
        "authors": autores
    }

    for key, value in updated_publication.items():
        publicacao_encontrada[key] = value

    if caminho_ficheiro:
        guardar(caminho_ficheiro, publicacoes)
        sg.popup("Publication successfully updated!")
    else:
        sg.popup("No file selected for saving")
```

No caso do utilizador querer editar os autores ja existentes ao selecionar essa opção, o seguinta janela será exibida:
<p align="center">
    <img src="Fotos%20Projeto/Edit%20Author.png" alt="logo" width="600"/>
</p>

Na hipótese do utilizador querer apagar a publicação do dataset, o seguinte aviso será mostrado:
<p align="center">
    <img src="Fotos%20Projeto/Delete%20Post.png" alt="logo" width="400"/>
</p>

```py
def remover_publicacao(publicacao_encontrada, caminho_ficheiro, publicacoes):
    publicacoes.remove(publicacao_encontrada)
    sg.popup("Publication removed successfully!")
    guardar(caminho_ficheiro, publicacoes)
```

### 3. Capacidades de Pesquisa
#### 3.1 Pesquisa com filtros
O programa é capaz de encontrar publicações utilizando vários filtros, tais como, palavra-chave, autor, afiliação, intervalo de tempo. Para realizar a pesquisa a seguinte janela é exibida:
<p align="center">
    <img src="Fotos%20Projeto/Search%20Filters.png" alt="logo" width="500"/>
</p>

Se não existir nenhuma publicação com os parâmetros submetidos, esta será apresentada:
<p align="center">
    <img src="Fotos%20Projeto/No%20Filter%20Search.png" alt="logo" width="400"/>
</p>

Após o programa procurar as publicações que apresentem os parâmentros preenchidos, será mostrada na seguinte janela as informações todas das publicações, os links que dão para interagrir direcionando diretamente para a Web
<p align="center">
    <img src="Fotos%20Projeto/Document%20Information.png" alt="logo" width="500"/>
</p>

O botão "Save Search" aprsentado na janela serve para o utilizador poder guardar a pesquisa em ficheiro txt ou em um ficheiro json com a mesma estrutura do dataset.
<p align="center">
    <img src="Fotos%20Projeto/Save%20Search.png" alt="Descrição da Imagem" width="200"/>
</p>
<p align="center">
    <img src="Fotos%20Projeto/Txt%20File.png" alt="Descrição da Imagem" width="500"/>
    <img src="Fotos%20Projeto/JSON%20File.png" alt="Descrição da Imagem" width="500"/>
</p>

#### 3.2 Pesquisa por título
O programa tem a funcionalidade de apresentar uma lista com todos os títulos das publicações presentes no dataset, com a possibilidade de os organizar por ordem alfabética ou por data de publicação.
<p align="center">
    <img src="Fotos%20Projeto/Title%20List.png" alt="Descrição da Imagem" width="600"/>
</p>

Se o utilizador selecionar um dos títulos apresentados, uma janela igual à função anterior aparecerá com as informações da publicação e com o botão para salvar a pesquisa.

#### 3.3 Pesquisa por autor
O programa tem a funcionalidade de apresentar uma lista com todos os autores das publicações presentes no dataset, com a possibilidade de os organizar por ordem alfabética ou pela sua frequencia.
<p align="center">
    <img src="Fotos%20Projeto/Author%20List.png" alt="Descrição da Imagem" width="400"/>
</p>

Se o utilizador selecionar um dos autores apresentados, uma janela igual à função anterior aparecerá com as informações da publicação e com o botão para salvar a pesquisa.

#### 3.4 Pesquisa por afiliação
O programa tem a funcionalidade de apresentar uma lista com todas as afiliações das publicações presentes no dataset, com a possibilidade de os organizar por ordem alfabética ou pela sua frequencia.
<p align="center">
    <img src="Fotos%20Projeto/Afilliation%20List.png" alt="Descrição da Imagem" width="600"/>
</p>

Se o utilizador selecionar uma das afiliações apresentados, uma janela igual à função anterior aparecerá com as informações da publicação e com o botão para salvar a pesquisa.

#### 3.5 Pesquisa por palavras-chave
O programa tem a funcionalidade de apresentar uma lista com todas as palavras-chave das publicações presentes no dataset, com a possibilidade de os organizar por ordem alfabética ou pela sua frequencia.
<p align="center">
    <img src="Fotos%20Projeto/Keyword%20List.png" alt="Descrição da Imagem" width="600"/>
</p>

Se o utilizador selecionar uma das palavras-chave apresentados, uma janela igual à função anterior aparecerá com as informações da publicação e com o botão para salvar a pesquisa.

#### 3.6 Pesquisa por intervalo de datas
O programa tem a funcionalidade de procurar publicações num dado intervalo de tempo.
<p align="center">
    <img src="Fotos%20Projeto/Search%20Date.png" alt="Descrição da Imagem" width="300"/>
</p>

Após inserida as datas uma janela igual à função anterior aparecerá com as informações da publicação e com o botão para salvar a pesquisa. Se não houver nenhuma publicação no dado intervalo de tempo a seguinte janela será exibida:
<p align="center">
    <img src="Fotos%20Projeto/No%20Search%20Date.png" alt="Descrição da Imagem" width="400"/>
</p>

### 4. Análise Estatística
#### 4.1 Distribuição de publicações por ano
O programa é capaz de exibir um gráfico com a distribuição de publicações por ano.
<p align="center">
    <img src="Fotos%20Projeto/No%20Search%20Date.png" alt="Descrição da Imagem" width="400"/>
</p>
- Distribuição mensal de publicações
- Métricas de publicação por autor
- Análise de frequência de palavras-chave

### 5. Interface do Utilizador
- Organização do menu principal
- Formulários de publicação
- Interfaces de pesquisa
- Janelas de visualização estatística

## Detalhes de Implementação

### Estrutura de Dados
Descrição de como os dados das publicações são estruturados e armazenados

### Funções Principais
Destaque das funções mais importantes e seus papéis:
- Funções de gestão de publicações
- Funções de pesquisa
- Funções de análise estatística
- Funções de visualização de dados

## Desafios e Soluções
Discussão dos principais desafios encontrados durante o desenvolvimento e como foram resolvidos

## Melhorias e Trabalho Futuro
Potenciais melhorias e funcionalidades que poderiam ser adicionadas no futuro

## Conclusão
Resumo das conquistas do projeto e resultados de aprendizagem

## Capturas de Ecrã
Incluir capturas de ecrã relevantes da interface e visualizações
