model_name="anthropic/claude-3-sonnet-20240229"
model_pretty_name="claude-3-sonnet-20240229"
output_dir="result_dirs/wild_bench/"
TEMP=0; TOP_P=1.0; MAX_TOKENS=2048;

# shard_size should be 1024 // n_shards
n_shards=8
shard_size=128
start_gpu=0
shards_dir="${output_dir}/tmp_${model_pretty_name}"
for ((start = 0, end = (($shard_size)), gpu = $start_gpu; gpu < $n_shards+$start_gpu; start += $shard_size, end += $shard_size, gpu++)); do
    echo "python src/unified_infer.py \
        --data_name wild_bench \
        --start_index $start --end_index $end \
        --engine anthropic \
        --model_name $model_name \
        --top_p $TOP_P --temperature $TEMP \
        --max_tokens $MAX_TOKENS \
        --output_folder $shards_dir/ \
        --overwrite "
done 
wait 
python src/merge_results.py $shards_dir/ $model_pretty_name
cp $shards_dir/${model_pretty_name}.json $output_dir/${model_pretty_name}.json
