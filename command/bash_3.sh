cd ..
export http_proxy=http://10.40.3.139:7899
export https_proxy=http://10.40.3.139:7899
# CUDA_VISIBLE_DEVICES=5 python run_meta_mmd_trans_auroc.py --id 61005 --sigma0 45 --lr 0.00005  --no_meta_flag   --n_samples 3900 --target_senten_num 3000 --val_num 50 --sigma 30 --max_length  100 --trial_num 3 --num_hidden_layers 1 --target_datasets HC3 --text_generated_model_name  chatGPT --base_model_name roberta-base-openai-detector --skip_baselines --mask_flag --transformer_flag --meta_test_flag --epochs 100 --two_sample_test
# CUDA_VISIBLE_DEVICES=5 python run_meta_mmd_trans_auroc.py --id 61006 --sigma0 50 --lr 0.00005  --no_meta_flag   --n_samples 3900 --target_senten_num 3000 --val_num 50 --sigma 30 --max_length  100 --trial_num 3 --num_hidden_layers 1 --target_datasets HC3 --text_generated_model_name  chatGPT --base_model_name roberta-base-openai-detector --skip_baselines --mask_flag --transformer_flag --meta_test_flag --epochs 100 --two_sample_test
CUDA_VISIBLE_DEVICES=5 python run_meta_mmd_trans_auroc.py --id 62007 --sigma0 55 --lr 0.00005  --no_meta_flag   --n_samples 3900 --target_senten_num 3000 --val_num 50 --sigma 30 --max_length  100 --trial_num 3 --num_hidden_layers 1 --target_datasets HC3 --text_generated_model_name  chatGPT --base_model_name roberta-base-openai-detector --skip_baselines --mask_flag --transformer_flag --meta_test_flag --epochs 100 --two_sample_test
