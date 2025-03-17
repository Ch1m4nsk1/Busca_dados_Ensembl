 * Projeto: Busca Automatizada no Ensembl via BioMart / Automated Ensembl Data Retrieval via BioMart
 * 
 * Descrição (PT):
 * Este script automatiza a busca de dados no banco de dados Ensembl utilizando a ferramenta BioMart. 
 * Realiza os seguintes passos:
 *   1. Acessa o "Ensembl Genes 113" e o dataset "Human genes (GRCh38.p14)".
 *   2. Filtra os dados por um cromossomo específico e bandas cromossômicas (ex.: cromossomo 21, bandas q21.1 e q21.2 ...).
 *   3. Seleciona os atributos: Gene Stable ID, Gene name, Protein Stable ID e UniProtKB/Swiss-Prot ID.
 *   4. Conta os resultados e realiza o download dos dados em formato CSV para a pasta de trabalho.
 * 
 * Observação: Este código foi desenvolvido como parte de uma tarefa para a disciplina de Evolução Molecular do curso
 * de Biologia da UFPR, ministrado pela professora Desiree.
 * Foi feito às pressas e de forma improvisada, apenas para evitar evitar que eu precisasse usar a interface gráfica para
 * obter o que eu desejava. Também quis demonstrar aos meus futuros colegas biólogos como a programação pode reduzir
 * significativamente o tempo gasto em uma tarefa, algo que, se feito manualmente, levaria horas para buscar os genes
 * em todos os cromossomos.
 * 
 *
 * 
 * Description (EN):
 * This script automates the retrieval of data from the Ensembl database using the BioMart tool.
 * It performs the following steps:
 *   1. Accesses "Ensembl Genes 113 and the dataset "Human genes (GRCh38.p14)".
 *   2. Filters the data by a specific chromosome and adjacent karyotype bands (e.g., chromosome 21, bands q21.1 and q21.2).
 *   3. Selects the attributes: Gene Stable ID, Gene name, Protein Stable ID, and UniProtKB/Swiss-Prot ID.
 *   4. Counts the results and enables CSV download of the data.
 * 
 * Note: This code was developed as part of an assignment for the Molecular Evolution course in the Biology program at UFPR,
 * taught by Professor Desiree. It was created quickly and in a somewhat improvised manner, simply to avoid having to use the
 * graphical interface to obtain the desired results. I also wanted to demonstrate to my future colleagues in biology how
 * programming can significantly reduce the time spent on a task, something that, if done manually, would take hours to search
 * for genes across all cromossomos.
 * 
 * Author: João Guilherme Chimanski (Ch1m4nsk1)
 * Data: 16/03/2025
'''
