# UTILS.PY -> MÓDULO COM AS FUNÇÕES
from config import navegador
from importants import usuario, senha
from selenium.webdriver.common.by import By
from time import sleep
import importants
import os

localDownload = importants.localDownload

def noNavegador(modo='nome'.lower(), componente='', funcao=''.lower(), texto=None, tempo=1):

    '''
    < PARÂMETROS >
    - Modo = "Notação ponto" que vai junto com o By, do atributo by. No sistema usamos três: NAME (utilizando o nome do componente pelo HTML/CSS), o CSS_SELECTOR (código utilizado para determinar as regras do componente) e o ID (que é o identificador do componente))
    - Componente (value) = Nome do Modo escolhido, presente no HTML/CSS do componente (identificador)
    - Funcao = Utilizamos três tipos de funções:
          I. [Função CLICAR] O de somente clicar num botão e aguardar um TEMPO
          II. [Função INSERIR] Quando precisamos inserir algum TEXTO e aguardar um TEMPO
          III. [Função LIMPARINSERIR] Quando eu preciso limpar os dados do componente para inserir um novo TEXTO e também aguardar um TEMPO
      Nesse atributo, podemos ver a necessidade de outros dois atributos: o Texto (que eu quero que seja inserido) e o Tempo (de sleep que eu quero de uma função até a outra)

    < EXEMPLO >
    Exemplo: utils.noNavegador('nome', 'password', 'inserir', texto='Ne@06062023', tempo=0.5)

    Isso é o mesmo que:     VARIÁVEL = CONEXAO_PÁGINA.find_element(by=By.NAME,value="password")
                            VARIÁVEL.send_keys('Ne@06062023') 
                            sleep(0.5)
    '''
    if modo == 'nome':
        Modo = By.NAME
    elif modo == 'css':
        Modo = By.CSS_SELECTOR
    elif modo == 'id':
        Modo = By.ID
    

    funcaoNoNavegador = navegador.find_element(by=Modo,value=componente)

    #sleep(8)
    if funcao == 'clicar':
        funcaoNoNavegador.click()
        sleep(tempo)
        
    elif funcao == 'inserir':
        funcaoNoNavegador.send_keys(texto) 
        sleep(tempo)

    elif funcao == 'limparinserir':
        funcaoNoNavegador.clear()
        funcaoNoNavegador.send_keys(texto) 
        sleep(tempo)

def arquivoRecente():
    listaArquivos = os.listdir(localDownload) # Todos os arquivos contidos na pasta

    listaDatas = []
    
    retorno = "cod123#202004"
    for arquivo in listaArquivos:
        # Descobrir a data desse arquivo
        if "planilha_vendas" in arquivo:
            dataModificacao = os.path.getmtime(os.path.join(localDownload, arquivo))
            listaDatas.append((dataModificacao, arquivo))
    
    if listaDatas:
        listaDatas.sort(reverse=True)
        retorno = listaDatas[0][1] # Esse é o nome do arquivo mais recente baixado
    else:
        print("Não há arquivo baixado. O sistema será encerrado.")
    
    return retorno

def loginSite(urlTiny):
    # Inserção do usuário e a senha seguindo com o clique no botão de login e o de continuar
    noNavegador('nome', 'username','inserir', usuario, 0.5)
    noNavegador('nome', 'password', 'inserir', senha, 0.5)
    noNavegador('css', '.sc-ispOId.fPZXsr', 'clicar', tempo=2)
    noNavegador('css', '.btn.btn-sm.btn-primary ', 'clicar', tempo=5)
    navegador.get(url=urlTiny)
    sleep(5)