# General

Este projeto foi dividido em 4 partes, seguindo um racional para fluxo de dados. Essas partes são: Ingestão, Transformação, Loading e Analytics. 

As etapas de Ingestão, Transformação abrangem as questões de 1 a 4 do desafio e são realizadas pelos arquivos: src/1_extraction.py, notebooks/01_datacleaniing.ipynb. Já as etapas Loading e Analytics são realizadas pelos arquivos src/3_loading.py e através da criação do dashboard disposto na pasta BI, além do link abaixo. 

link Bi: https://app.powerbi.com/view?r=eyJrIjoiOTEyOTIxZDktYzIxYi00MzdmLThlMGMtODQ1YTAzN2IzYjYxIiwidCI6ImRmNzFmNmJiLWUzY2MtNGY1Yi1iNTMyLTc5ZGUyNjFiNTFhMiJ9

# Etapa 1 - 4: Resposta das questôes 1 a 4 

O primeiro problema a ser resolvido foi extrair o arquivo zipado e loading no sqlite. Isso está disposto no arquivo src/1_extraction.py
Após essa etapa, faz-se alguns tratamentos, conforme se segue. Todas as etapas do tratamento estão dispostas no arquivo notebooks/01_datacleaning.ipynb

1. Colocação no DuckDb

O primeiro passo foi copiar os dados do sqlite para o duckdb. Escolhemos essa opção, pois o duckdb apresenta algumas facilidades em função do banco de dados ser embarcado, servir para o propósito mesmo de analitycs, mais performático, etc.

2. Resolvendo Questões 2 e 3

Antes de fazer a junção entre as tabelas escolas_alunos, foi resolvido fazer uma limpeza inicial dos dados em cada tabela, separadamente, devido ao tamanho expressivo dos dados.

Começando pela tabela escolas. Foi feita a exclusão de colunas desnecessárias, seguido pela retirada dos espaçamentos de espaço ou caractere dos valores das colunas de texto. Após isso, foi excluido o conjunto dos valores duplicados na coluna 'codesc'. 
Em seguida, foi trabalhado as colunas verificadas como 'date_columns', porém ainda não no formato adequado. Trabalhou-se essas colunas deixando a tabela muito mais leve e limpa para trabalhar, uma redução de 6MB para 600KB. 

No segundo momento, tratou-se da tabela escolas. Essa tabela é muito pesada, e possui dados extramamente irregulares. Foi escolhido de modo arbitrário quais seriam as colunas mais importantes ali para trabalhar. Como a maioria das colunas muito irregulares tinham texto como dados, resolveu-se fazer as limpezas gerais de acentuação, espaçamento, remoção de caracteres especiais e/ou númericos.

Em função da irregularidade dos dados, algumas colunas foi necessário um 'replacement' manual, sem dúvida a etapa mais dificultosa e com maior tempo demandado do desafio, isto é, conseguir enxergar e definir os "replacements" manuais. 

Após essas limpezas em cada dataset separadamente, faz-se a juncao das duas tabelas, formando a tabela escolas_alunos. 

# Etapa 5: Resposta a questão 5

No arquivo src/3_loading.py é feito a carga do arquivo para um csv. Esse csv vai alimentar o BI. Foi utilizado o Power BI como ferramenta de dataviz. 

As questões que foram tomadas como base são:

# Analytics Questions

## Alunos
- Quantidade Atual de Alunos na Rede?
- Qual a região de maior demanda? ( Aluno x Região)
- Qual o turno de maior demanda? (Aluno x Turno)
- Quantidade de Alunos x Ano? 
- Qual a escola com maior e menor Quantidade de Alunos?
- Idade Média dos Alunos?
- Idade Média x Turno?
- Qtd Alunos x Modalidade?

## Escolas

- Quantidade de Escolas na Rede ?
- Quantidade de Escolas por Região?
- Crescimento Escolas x Ano?
- Quanto das escolas são convenio vs prefeitura?

Em seguida fizemos o BI, que está disposto no link abaixo. 

link Bi: https://app.powerbi.com/view?r=eyJrIjoiOTEyOTIxZDktYzIxYi00MzdmLThlMGMtODQ1YTAzN2IzYjYxIiwidCI6ImRmNzFmNmJiLWUzY2MtNGY1Yi1iNTMyLTc5ZGUyNjFiNTFhMiJ9

# Observações

Alguns pontos de atenção são: 
* A parte mais trabalhosa e que tem algum nível de arbitrariedade são as colunas que possuem valores muito específicos, ou não tem um padrão claro, daí, todo o ajuste é feito manualmente, isso pode gerar alguns problemas de descarte não reparados ou ainda informações deprezadas, que pode prejudicar a análise posteriormente. 
* As colunas foram escolhidas para tratamento de modo mais ou menos arbitrário, considerando algumas e desprezando outras, em função da visão do analista para a situação, o que pode incorrer em erros, etc. 
* Como linha geral, 80% do trabalho foi ajustes e tratamento do dataset, e 20% dataviz.








