echo "Checking duplicates in external_gene_name of the file chromosome_1_genes.csv:"
tail -n +2 chromosome_1_genes.csv | cut -d',' -f2 | sort | uniq -d | head -n 5

for file in *_genes.csv; do
    if [ -f "$file" ]; then
        output_file="${file%.*}_unique_fixed.csv"
        # Preserves the header
        head -n 1 "$file" > "$output_file"
        # Catch the first occurrence of each external_gene_name
        awk -F, 'NR>1 {
            if (!seen[$2]++) {
                print $0
            }
        }' "$file" >> "$output_file"
        echo "Processed $file -> $output_file"
        echo "Original count in $file: $(wc -l < "$file")"
        echo "Unique count in $output_file: $(wc -l < "$output_file")"
        echo "------------------------"
    fi
done
