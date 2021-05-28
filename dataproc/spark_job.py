import sys, re
from pyspark.sql.functions import udf, to_timestamp
from pyspark.sql.types import StringType, StructField, StructType
from pyspark.sql import SQLContext, Row, SparkSession


def main(argv):
    #Recebe os arquivos da execução da DAG para processamento posteriormente.
    words_file = argv[0]
    customer_file = argv[1]

    spark = SparkSession.builder.master("yarn").appName("process-files").getOrCreate()
    
    sc = spark.sparkContext
    sc.setLogLevel("WARN")
    
    sqlContext = SQLContext(sc)
    
    #Importa o CSV de pedidos de cliente.
    df_csv = (
        spark.read.format("csv")
        .option("header", "True")
        .option("delimiter", ",")
        .option("inferSchema", "True")
        .load(words_file)
    )
    
    #Cria uma view temporária para executar as tranformações e a seleção dos dados que serão exportados para o CSV final.
    df_csv.createOrReplaceTempView("tb1")
    df_export = spark.sql(
        """
    with pre_table as(
    select 
        codigo_cliente,
        ARRAY(codigo_pedido, CAST(CAST(data_pedido as TIMESTAMP) as DATE)) AS lista_pedidos,
        CASE WHEN MONTH (current_date()) < MONTH(CAST(data_nascimento_cliente as DATE)) OR
        (MONTH(current_date()) = MONTH(CAST(data_nascimento_cliente as DATE)) AND DAY(current_date()) < DAY(CAST(data_nascimento_cliente as DATE)))
             THEN YEAR(current_date()) - YEAR(CAST(data_nascimento_cliente as DATE)) - 1
        ELSE YEAR(current_date()) - YEAR(CAST(data_nascimento_cliente as DATE))
        END AS IDADE,
        CAST(CAST(data_pedido as TIMESTAMP) as DATE) as data_pedido
    from tb1)

    select 
           codigo_cliente,
           COUNT(*) as numero_pedidos,
           COLLECT_SET(lista_pedidos) AS lista_pedidos,
           idade
    from pre_table
    where data_pedido in ('2018-11-23', '2019-11-29', '2020-11-27')
    and IDADE < 30
    group by codigo_cliente, idade
    HAVING COUNT(*) > 2
    order by codigo_cliente
    """
    )
    
    #Importa o arquivo de palavras.
    df_txt = spark.read.format("text").load(customer_file)
    
    #Cria uma view temporária para retirar as linhas em branco.
    df_txt.createOrReplaceTempView("tb1")
    
    #Cria um novo DataFrame a partir das consulta que remove as linhas em branco.
    df_txt = spark.sql(
        """
    select * from tb1 where value not in ('', ' ')
    """
    )
    
    #Cria uma lista com os valores da tabela, para passar na função de RegEx.
    words_array = [str(row.value) for row in df_txt.collect()]
    
    #Cria um DataFrame vazio, que será preenchido com a execução da função de RegEx.
    schema = StructType([StructField("words", StringType(), True)])
    df_txt = spark.createDataFrame([], schema)
    
    #Executa um laço baseado no tamanho da lista que retornou do arquivo, 
    #aplica a função de Regex para separar as palvras e insere no DataFrame criado anteriormente.
    for word in words_array:
        x = re.findall("[^\s.,]+", word)
        rdd1 = sc.parallelize(x)
        row_rdd = rdd1.map(lambda x: Row(x))
        df_temp = sqlContext.createDataFrame(row_rdd, ["words"])
        df_txt = df_txt.union(df_temp)
        
    #Cria a view temporária com as palavras já parseadas pela função de RegEx.
    df_final = df_txt.createOrReplaceTempView("tbwords")
    
    #Cria um DataFrame final, contendo as informações necessárias para exportação,
    #Colocando todas as palavras em forma maiúscula para evitar duplicidade devido ao case sensitive.
    df_final = spark.sql(
        """
    select 
        case when LENGTH(UPPER(tw.words)) <= 10 
             then UPPER(tw.words) 
        else 'MAIORES QUE 10' end as word,
        count(tw.words) as appears
    from tbwords tw
    group by word
    """
    )
    
    #Executa as exportações dos DataFrames finais como CSV para o bucket onde os arquivos iniciais foram processados.
    df_final.withColumn("word", df_final.word)\
            .withColumn("appears",df_final.appears)\
            .coalesce(1)\
            .write.format("csv")\
            .option("header", "True")\
            .save("gs://YOUR_PROJECT_ID-spark-files/extract_words.csv")

    df_export.withColumn("codigo_cliente", df_export.codigo_cliente)\
             .withColumn("numero_pedidos", df_export.numero_pedidos)\
             .withColumn("lista_pedidos", df_export.lista_pedidos.cast("string"))\
             .withColumn("idade", df_export.idade)\
             .coalesce(1)\
             .write.format("csv")\
             .option("header", "True")\
             .save("gs://YOUR_PROJECT_ID-spark-files/clientes_pedidos_novo.csv")


if __name__ == "__main__":
    main(sys.argv[1:])
