# Sisu-Dados
##
## Como usar
Para usar o códgio basta ter instalado o seleninum, o Chrome Driver já é instalado automaticamente, depois é só executar o arquivo main.py e digitar qual dia de SISU será analisado. Com isso o programa automaticamente cria um arquivo com o nome do dia digitado e se tiver outro arquivo com um dia anterior já junta os dados anteriores automaticamente.
## Como funciona
O código busca uma api do SISU que contém todos os dados, inicialmente busca cada universidade por estado e depois os curso de cada universidade, com issso busca em cada curso todas as informações necessárias para montar a planilha.

O código usa o Selenium porque nos teste o request retornava um código de erro e demorava mais para encontrar os dados, por isso foi melhor usar o Selenium.