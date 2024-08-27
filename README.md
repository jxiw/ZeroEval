Please refer to [this link](https://github.com/yuchenlin/ZeroEval) for installation and evaluation. If you utilize this evaluation, please remember to cite the original repository.

## Usage

To evaluate on gsm8k, please run
`bash zero_eval_mamba.sh MambaInLlama_0_50 gsm`

To evalute on CRUX, please run
`bash zero_eval_mamba.sh MambaInLlama_0_50 crux`

### Examples

- GSM: `python src/evaluation/gsm_eval.py` --> [Full results](result_dirs/gsm.summary.md)
- CRUX: `python src/evaluation/crux_eval.py` --> [Full results](result_dirs/crux.summary.md)

