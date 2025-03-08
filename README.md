## Fonte dos dados
Esses dados foram baixados e importados para dentro de um bucket de um projeto no Google Cloud Storage.

Kaggle: [Acesse os dados aqui](https://www.kaggle.com/datasets/nosbielcs/brazilian-delivery-center).

Em seguida, foi criada uma nova base de dados no BigQuery e a partir do Google Cloud CLI foi executado o seguinte comando para transformar o ecommerce.csv em uma tabela com base nos parâmetros que podem ser visualizados em '/data/schema.json':

```
bq load --source_format=CSV --skip_leading_rows=1 --schema=schema.json etl_ecommerce.tb_compras gs://info_compras/dados/ecommerce.csv
```

## Script
O notebook 'transform.ipynb' foi implementado dentro do Google Cloud Platform, para executar no VSCode, é necessário autenticar com uma conta do Google. No notebook primeiro é feito a extração dos dados via BigQuery, depois é realizado a limpeza e manipulação dos mesmos e exportado para uma nova tabela limpa.
Dentro do mesmo arquivo, após exportar a tabela, é feito o cálculo das métricas de receita total, vendas por país, vendas por mês e ano e vendas por categoria, e cada métrica é exportado para uma tabela diferente.

Para fazer a autenticação mude o diretório no CLI da Google Cloud para o do seu projeto com cd "caminho" em seguida execute o seguinte comando e faça a autenticação na web com sua conta do Google.
```
gcloud auth application-default login
```

## Automatização
A parte de automação do script é feita no próprio GCP, onde foi configurado para o script rodar todo dia, mas também é possível executa-lo a hora que quiser com apenas um clique.

## Pequeno vídeo demonstrativo
A partir do seguinte vídeo é possível acompanhar como as tabelas foram estruturadas, assim como, o que acontece após a parte de automação ser executada dentro da nuvem:

Youtube: [Acesse o vídeo aqui](https://youtu.be/JJkR8Wr0WbY).

OBS: Nesse exemplo, as novas tabelas foram criadas, porém caso seja necessário apenas atualizar invés de criar, o script funciona corretamente.

## Dashboard
Dashboard feito com o Looker Studio e sincronizado com base de dados do BigQuery, sendo atualizado conforme os dados mudam.

Looker: [Acesse o Dashboard aqui](https://lookerstudio.google.com/s/uVzmjlEjxI4).

PDF: [Visualize uma prévia](Dashboard-Ecommerce.pdf).

## Desafios
Este foi meu primeiro contato com a Google Cloud Platform. No início, tive um pouco de dificuldade para me familiarizar com a ferramenta, mas após algumas pesquisas e experimentação, consegui superar os desafios e concluir a implementação.

## Clone o repositório:

```bash
git clone https://github.com/mtzdantas/etl-ecommerce.git
```
