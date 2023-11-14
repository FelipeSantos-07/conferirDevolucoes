# IMPORTANTS.PY -> MÓDULO COM AS VARIÁVEIS MAIS IMPORTANTES DO SISTEMA

# < ACESSO AO TINY >
usuario = "emailLogin@teste.com" # EMAIL PARA LOGIN
senha = "senha123456789" # SENHA PARA LOGIN

# FILTRO DO INTERVALO DAS DATAS (INICIAL e FINAL) PARA GERAÇÃO DO .XLS
dataInicial = "01/10/2023"
dataInicial = dataInicial.replace('/', '')

dataFinal = "31/10/2023"
dataFinal = dataFinal.replace('/','')

# LOCAL ONDE OS ARQUIVOS BAIXADOS VÃO (pasta de Downloads)
localDownload = "C://Users/" 

# CAMINHO PARA ONDE EU QUERO QUE MEU XLS FINAL VÁ
localFinal = "C://Users/"

# # URL das abas do Tiny
urlVendas = 'https://erp.tiny.com.br/vendas#list'
urlDevolucoes = 'https://erp.tiny.com.br/devolucoes_vendas' 