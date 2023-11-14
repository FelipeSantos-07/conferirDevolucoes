# VERSÃO 1.0
from importants import dataInicial, dataFinal, urlDevolucoes, localFinal
from config import navegador
from utils import noNavegador, loginSite
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import sys
from tqdm import tqdm


# LOGIN NO SITE e FILTROS ------------
loginSite(urlDevolucoes)
noNavegador('css', '.filter-label.filter-toggle.has-tipsy-top', 'clicar', tempo=1.5)
noNavegador('id', 'opc-per-periodo', 'clicar', tempo=1.5)
noNavegador('id', 'data-ini', 'limparinserir', dataInicial, 0.5)
noNavegador('id', 'data-fim', 'limparinserir', dataFinal, 0.5)
noNavegador('css', '.btn.btn-primary.filter-apply', 'clicar', tempo=5)


# QUANTIDADE DE PEDIDOS COM O FILTRO
quantidadePedidos = navegador.find_elements(By.XPATH, "//span[@data-total-id]")
for pedido in quantidadePedidos:
    quantidade = pedido.get_attribute("outerHTML")
    data_total_id = pedido.get_attribute("data-total-id")
    if data_total_id == "geral":
        #print(quantidade)
        break

totalQuantidade = ''
for caractere in quantidade[52:]:
    if caractere != '<':
        totalQuantidade = totalQuantidade + caractere
    else:
        if totalQuantidade == "":
            print(f"Não há devoluções nesse dia!")
            sys.exit()
        else:
            totalQuantidade = int(totalQuantidade)
            break


# ENCONTRAR O ID DO PEDIDO MAIS RECENTE
trs = navegador.find_element(By.XPATH, "//tr[@iddevolucao]")
codigoHTML = trs.get_attribute("outerHTML")
idDevolucao = codigoHTML[17:22]
idDevolucao = int(idDevolucao)

# LISTAS COM OS DADOS PARA O DATAFRAME
lista_dataDevolucao = []
lista_nroPedido = []
lista_dataPedido = []
lista_nomeAtendente = []
lista_tipoDeposito = []
lista_situacaoPedido = []
lista_tipoDaDevolucao = []
lista_motivosDasDevolucoes = []
lista_tipoDeTransporte = []
lista_destinoDaPeca = []
lista_triagemDeDevolucao = []
lista_marcadoresDeCancelamento = []
lista_controleNf = []
lista_tipoDePagamento = []
lista_posTriagem = []
lista_outrosMarcadores = []

# VERIFICAR PEDIDO POR PEDIDO
contador = 1
with tqdm(total=totalQuantidade, desc="Progresso", unit='') as pbar:
    while contador <= totalQuantidade:
        try:
            navegador.get(f"https://erp.tiny.com.br/devolucoes_vendas#edit/{idDevolucao}")
            wait = WebDriverWait(navegador, 1.5)
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal-dialog.modal-md")))
            sleep(1.8)
            noNavegador('css', '.btn.btn-sm.btn-default.btn-ghost', 'clicar', tempo=1)
        except Exception as e:

            # PEGAR O NÚMERO DO PEDIDO
            nroPedido_1 = navegador.find_element(By.XPATH, "//small[@id='tituloNumeroOrigemDevolucao']")
            nroPedido_2 = nroPedido_1.get_attribute("outerHTML")
            nroPedido = nroPedido_2[65:71]
            #print(nroPedido, end=' - ')

            # PEGAR SITUAÇÃO DO PEDIDO
            situacaoPedido_1 = navegador.find_element(By.XPATH, "//div[@class='view-info-situacao']")
            situacaoPedido_2 = situacaoPedido_1.get_attribute("outerHTML")
            situacaoPedido = situacaoPedido_1.text.capitalize()
            #print(situacaoPedido, end=' - ')

            # PEGAR OS DADOS DE DEVOLUÇÃO
            form_devolucao_etapa_1 = navegador.find_element(By.ID, "form-devolucao-etapa-1")
            secao_dados_gerais_devolucao = form_devolucao_etapa_1.find_element(By.ID, "secao-dados-gerais-devolucao")

            col_elements = secao_dados_gerais_devolucao.find_elements(By.XPATH, ".//div[contains(@class, 'col-sm-4 col-md-3 form-group')]")

            # PEGAR O NOME DO ATENDENTE
            for col in col_elements:
                label = col.find_element(By.XPATH, ".//label")
                if label.get_attribute("for") == "usuarioDevolucao":
                    atendente = col.find_element(By.XPATH, ".//p[@class='form-control-static viewing-input']")
            nomeAtendente = str(atendente.text)
            #print(nomeAtendente, end=' - ')

            # PEGAR O TIPO DE DEPÓSITO
            for col in col_elements:
                label = col.find_element(By.XPATH, ".//label")
                if label.get_attribute("for") == "idDepositoDevolucao":
                    deposito = col.find_element(By.XPATH, ".//p[@class='form-control-static viewing-input']")
            tipoDeposito = str(deposito.text.capitalize())
            #print(tipoDeposito, end=' - ')

            # PEGAR A DATA DA VENDA/PEDIDO
            for col in col_elements:
                label = col.find_element(By.XPATH, ".//label")
                if label.get_attribute("for") == "dataVendaDevolucao":
                    dataPedido = col.find_element(By.XPATH, ".//p[@class='form-control-static viewing-input']")
            dataPedido = str(dataPedido.text)
            #print(dataPedido, end=' - ')

            # PEGAR A DATA DA DEVOLUÇÃO
            for col in col_elements:
                label = col.find_element(By.XPATH, ".//label")
                if label.get_attribute("for") != "usuarioDevolucao" and label.get_attribute("for") != "idDepositoDevolucao" and label.get_attribute("for") != "dataVendaDevolucao":
                    dataDevolucao = col.find_element(By.XPATH, ".//p[@class='form-control-static viewing-input']")
            dataDevolucao = str(dataDevolucao.text)
            #print(dataDevolucao, end=' - ')

            # PEGAR MARCADORES
            element = WebDriverWait(navegador, 10).until(
                EC.visibility_of_element_located((By.ID, "form-devolucao-etapa-2"))
            )

            element1 = navegador.find_element(By.ID, "form-devolucao-etapa-2")
            element4 = element1.find_element(By.ID, "listaMarcacoesObjeto")

            li_elements = element4.find_elements(By.TAG_NAME, "li")
            quantidadeElementos = int(len(li_elements))
            contadorElementos = 1

            lista_marcadores = []

            for li in li_elements:
                if contadorElementos < quantidadeElementos:
                    i_element = li.find_element(By.XPATH, ".//span[@class='tagit-label']")
                    i_element_2 = i_element.get_attribute("outerHTML")
                    lista_marcadores.append(i_element.text.lower())
                    contadorElementos += 1
                else:
                    break

            # GRUPOS DE MARCADORES
            tipoDaDevolucao = 'N/D'
            motivosDasDevolucoes = 'N/D'
            tipoDeTransporte = 'N/D'
            destinoDaPeca = 'N/D'
            triagemDeDevolucao = 'N/D'
            marcadoresDeCancelamento = 'N/D'
            controleNf = 'N/D'
            tipoDePagamento = 'N/D'
            posTriagem = 'N/D'
            outrosMarcadores = 'N/D'

            for tag in lista_marcadores:
                if tag in ('troca', 'devolução', 'dev aut', 'estornodef'):
                    if tipoDaDevolucao == "N/D":
                        tipoDaDevolucao = str(tag).capitalize()
                    else:
                        continue
                elif tag in ('comprou errado', 'ee', 'er', 'ver', 'arrependimento', 'defeito', 'qualidade', 'avaria'):
                    if motivosDasDevolucoes == "N/D":
                        motivosDasDevolucoes = str(tag).capitalize()
                    else:
                        continue
                elif tag in ('transporte', 'mb', 'r'):
                    if tipoDeTransporte == "N/D":
                        tipoDeTransporte = str(tag).capitalize()
                    else:
                        continue
                elif tag in ('estoque', 'teste', 'refugo'):
                    if destinoDaPeca == "N/D":
                        destinoDaPeca = str(tag).capitalize()
                    else:
                        continue
                elif tag in ('triadas'):
                    if triagemDeDevolucao == "N/D":
                        triagemDeDevolucao = str(tag).capitalize()
                    else:
                        continue
                elif tag in ('ec', 'cancelamento', 'se', 'tray', 'nf'):
                    if marcadoresDeCancelamento == "N/D":
                        marcadoresDeCancelamento = str(tag).capitalize()
                    else:
                        continue
                elif tag in ('nf cancel', 'nf dev'):
                    if controleNf == "N/D":
                        controleNf = str(tag).capitalize()
                    else:
                        continue
                elif tag in ('estorno', 'dev crédito'):
                    if tipoDePagamento == "N/D":
                        tipoDePagamento = str(tag).capitalize()
                    else:
                        continue
                elif tag in ('brigar', 'resolvido', 'perdemos'):
                    if posTriagem  == "N/D":
                        posTriagem = str(tag).capitalize()
                    else:
                        continue
                else:
                    if outrosMarcadores == 'N/D':
                        outrosMarcadores = str(tag).capitalize()
                    else:
                        outrosMarcadores = f"{outrosMarcadores}, {str(tag).capitalize}"
                

            # ARMAZENANDO OS DADOS
            lista_dataDevolucao.append(dataDevolucao)
            lista_nroPedido.append(nroPedido)
            lista_dataPedido.append(dataPedido)
            lista_nomeAtendente.append(nomeAtendente)
            lista_tipoDeposito.append(tipoDeposito)
            lista_situacaoPedido.append(situacaoPedido)
            lista_tipoDaDevolucao.append(tipoDaDevolucao)
            lista_motivosDasDevolucoes.append(motivosDasDevolucoes)
            lista_tipoDeTransporte.append(tipoDeTransporte)
            lista_destinoDaPeca.append(destinoDaPeca)
            lista_triagemDeDevolucao.append(triagemDeDevolucao)
            lista_marcadoresDeCancelamento.append(marcadoresDeCancelamento)
            lista_controleNf.append(controleNf)
            lista_tipoDePagamento.append(tipoDePagamento)
            lista_posTriagem.append(posTriagem)
            lista_outrosMarcadores.append(outrosMarcadores)

            contador += 1 # CASO O PEDIDO EXISTA, É INCREMENTADO ATÉ DAR A QUANTIDADE DE PEDIDOS
            pbar.update(1)
        idDevolucao -= 1


# Após o loop, crie o dataframe usando o pandas
dadosDevolucao = pd.DataFrame({
    'Data da devolucao': lista_dataDevolucao,
    'Número do pedido': lista_nroPedido,
    'Data do pedido': lista_dataPedido,
    'Nome do atendente': lista_nomeAtendente,
    'Tipo de deposito': lista_tipoDeposito,
    'Situação do pedido': lista_situacaoPedido,
    'Tipo da devolucao': lista_tipoDaDevolucao,
    'Motivo da devolução': lista_motivosDasDevolucoes,
    'Tipo de transporte': lista_tipoDeTransporte,
    'Destino da peça': lista_destinoDaPeca,
    'Triagem de devolucao': lista_triagemDeDevolucao,
    'Marcadores de cancelamento': lista_marcadoresDeCancelamento,
    'Controle da nota fiscal': lista_controleNf,
    'Tipo de pagamento': lista_tipoDePagamento,
    'Pós-triagem': lista_posTriagem,
    'Outros marcadores': lista_outrosMarcadores
})

caminho_saida_excel_confereDev = f"{localFinal}/confereDev.xlsx"

# Salvar o DataFrame como um arquivo Excel
dadosDevolucao.to_excel(caminho_saida_excel_confereDev, index=False)