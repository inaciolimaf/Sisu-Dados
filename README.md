# Sisu-Dados
## Resultados
Os resultados obtidos para o SISU 2023.1 estão disponiveis nos arquivos do repositório ou pelo <a href="https://docs.google.com/spreadsheets/d/1BvtCRN2tsA06cD_zlFRjHz9iR3-IlGSq/edit?usp=share_link&ouid=112517535618268926052&rtpof=true&sd=true">Google Drive</a>
## Como obter os dados
Para usar o códgio basta ter instalado o seleninum, o Chrome Driver já é instalado automaticamente, depois é só executar o arquivo main.py e digitar qual dia de SISU será analisado. Com isso o programa automaticamente cria um arquivo com o nome do dia digitado e se tiver outro arquivo com um dia anterior já junta os dados anteriores automaticamente.
## Como funciona
O código busca uma api do SISU que contém todos os dados, inicialmente busca cada universidade por estado e depois os curso de cada universidade, com issso busca em cada curso todas as informações necessárias para montar a planilha.

O código usa o Selenium porque nos teste o request retornava um código de erro e demorava mais para encontrar os dados, por isso foi melhor usar o Selenium.
