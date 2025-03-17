''' 
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

import requests
import pandas as pd
import io
import sys
from time import sleep
from requests.exceptions import RequestException, HTTPError, Timeout

# Configuration constants
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
REQUEST_TIMEOUT = 30  # seconds
# Setting the BioMart URL
BIOMART_URL = "http://www.ensembl.org/biomart/martservice"

def get_chromosome_data(chromosome, retry_count=0):
    try:
        
        # Using the global BIOMART_URL const
        xml_query = f"""<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE Query>
        <Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
            <Dataset name = "hsapiens_gene_ensembl" interface = "default" >
                <Filter name = "chromosome_name" value = "{chromosome}"/>
                <Attribute name = "ensembl_gene_id" />
                <Attribute name = "external_gene_name" />
                <Attribute name = "ensembl_peptide_id" />
                <Attribute name = "uniprotswissprot" />
                <Attribute name = "chromosome_name" />
                <Attribute name = "band" />
            </Dataset>
        </Query>"""
        
        # Using the column names to match the requested attributes
        column_names = [
            'ensembl_gene_id',          # Gene Stable ID
            'external_gene_name',       # Gene name
            'ensembl_peptide_id',       # Protein Stable ID
            'uniprotswissprot',         # UniProtKB/Swiss-Prot ID
            'chromosome_name',          # Chromosome
            'band'                      # Band
        ]
        
        
        # Running the query using a POST request
        print(f"Fetching data for chromosome {chromosome}...")
        response = requests.post(BIOMART_URL, data={'query': xml_query}, timeout=REQUEST_TIMEOUT)

        # Check if the request was successful
        response.raise_for_status()
        
        # Process response (which is tab-separated data)
        response_text = response.text

        # Validate response content
        if not response_text or not response_text.strip():
            print(f"Warning: Empty response for chromosome {chromosome}")
            return pd.DataFrame(columns=column_names)
            
        # checking for error messages in the response
        if response_text.strip().startswith('<?xml') or '[ERROR]' in response_text:
            print(f"Error in BioMart response for chromosome {chromosome}: {response_text[:100]}...")
            return pd.DataFrame(columns=column_names)
            
        # Analyzing the data separated by tabulation
        try:
            df = pd.read_csv(io.StringIO(response_text), sep='\t', names=column_names, header=None)
        except pd.errors.EmptyDataError:
            print(f"Warning: No data in response for chromosome {chromosome}")
            return pd.DataFrame(columns=column_names)
        except Exception as e:
            print(f"Error parsing data for chromosome {chromosome}: {str(e)}")
            print(f"Response preview: {response_text[:100]}...")
            return pd.DataFrame(columns=column_names)
        
        # Remove duplicates
        df = df.drop_duplicates()

        # Data validation
        if df.empty:
            print(f"Warning: No data found for chromosome {chromosome} after processing")
        else:
            print(f"Retrieved {len(df)} unique records for chromosome {chromosome}")
        # Save in individual chromosome file
        # e.g. chromosome_1_genes.csv
        filename = f'chromosome_{chromosome}_genes.csv'
        df.to_csv(filename, index=False)
        print(f"Saved data for chromosome {chromosome} to {filename}")
        
        return df
        
    # Adding error messages to debug
    except HTTPError as e:
        print(f"HTTP Error for chromosome {chromosome}: {str(e)}")
        if retry_count < MAX_RETRIES:
            print(f"Retrying ({retry_count + 1}/{MAX_RETRIES}) in {RETRY_DELAY} seconds...")
            sleep(RETRY_DELAY)
            return get_chromosome_data(chromosome, retry_count + 1)
        return None
    except Timeout:
        print(f"Timeout error for chromosome {chromosome}")
        if retry_count < MAX_RETRIES:
            print(f"Retrying ({retry_count + 1}/{MAX_RETRIES}) in {RETRY_DELAY} seconds...")
            sleep(RETRY_DELAY)
            return get_chromosome_data(chromosome, retry_count + 1)
        return None
    except RequestException as e:
        print(f"Request error for chromosome {chromosome}: {str(e)}")
        if retry_count < MAX_RETRIES:
            print(f"Retrying ({retry_count + 1}/{MAX_RETRIES}) in {RETRY_DELAY} seconds...")
            sleep(RETRY_DELAY)
            return get_chromosome_data(chromosome, retry_count + 1)
        return None
    except Exception as e:
        print(f"Error processing chromosome {chromosome}: {str(e)}")
        return None

def main():
    # Listing all chromosomes (1-22, X, Y) "or trying"
    chromosomes = [str(i) for i in range(1, 23)] + ['X', 'Y']
        
    print(f"Will process {len(chromosomes)} chromosomes: {', '.join(chromosomes)}")
        
    # Store all dataframes and track progress
    all_data = []
    successful_count = 0
    failed_count = 0
    total_chromosomes = len(chromosomes)

    # Process each chromosome in the workdir
    for i, chrom in enumerate(chromosomes, 1):
        print(f"\nProcessing chromosome {chrom} ({i}/{total_chromosomes})...")
        # Get data for the chromosome and store it in df
        df = get_chromosome_data(chrom)
        if df is not None and not df.empty:
            all_data.append(df)
            successful_count += 1
        elif df is not None and df.empty:
            print(f"No data retrieved for chromosome {chrom}")
            successful_count += 1
        else:
            failed_count += 1

        # Add delay to prevent overwhelming the server
        # Except for the last chromosome
        if i < total_chromosomes:  
            print(f"Waiting before next request...")
            sleep(1)
    
    # print summary
    print("\n" + "="*50)
    print(f"Processing Summary:")
    print(f"  - Chromosomes processed: {total_chromosomes}")
    print(f"  - Successful retrievals: {successful_count}")
    print(f"  - Failed retrievals: {failed_count}")

    # Combine all data
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv('all_chromosomes_genes.csv', index=False)
        print("\nCreated combined file: all_chromosomes_genes.csv")
        print(f"Total records: {len(combined_df)}")
        print(f"Unique genes: {combined_df['ensembl_gene_id'].nunique()}")
        print(f"Unique proteins: {combined_df['ensembl_peptide_id'].nunique()}")
    else:
        print("\nNo data was retrieved for any chromosome.")
        sys.exit(1)  # Exit with error code

if __name__ == "__main__":
    try:
        print("="*50)
        print("Starting Ensembl BioMart data retrieval...")
        print("="*50)
        main()
        print("\nProcess completed successfully.")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(130)  # Exit with standard interrupt code
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)  # Exit with error code

