import os
import numpy as np

def _get_best_epochs(results, epochs, window_size):
    # results: (epoch_num, )

    max_value = 0
    max_index = -1
    for o in range(len(epochs)-window_size+1):
        if results[o:o+window_size].mean() > max_value:
            max_value = results[o:o+window_size].mean()
            max_index = o
        
    return epochs[max_index:max_index+window_size], max_value


def get_best_epochs(result_dir, prefix, suffix, mode, subset, repeat_ids, split_ids, epochs, window_size, result_key='AP_IVT'):

	results = np.zeros((len(repeat_ids), len(split_ids), len(epochs)))

	for r_id, repeat_id in enumerate(repeat_ids):
		for s_id, split_id in enumerate(split_ids):
			naming = f'{prefix}-S{split_id}-{repeat_id}{suffix}'
			for e_id, epoch in enumerate(epochs):
				result_file = os.path.join(result_dir, naming, f'{subset}_results_{mode}_epoch{epoch}.npy')
				try:
					result = np.load(result_file, allow_pickle=True).item()
					results[r_id, s_id, e_id] = result[result_key]
				except Exception as exception:
					results[r_id, s_id, e_id] = 0
					print(exception, result_file)

	results = results.mean(0).mean(0)
	best_epochs, best_value = _get_best_epochs(results, epochs, window_size)

	return best_epochs, best_value


def get_result(result_dir, prefix, suffix, mode, subset, repeat_ids, split_ids, epochs, result_key='AP_IVT'):

	results = np.zeros((len(repeat_ids), len(split_ids), len(epochs)))

	for r_id, repeat_id in enumerate(repeat_ids):
		for s_id, split_id in enumerate(split_ids):
			naming = f'{prefix}-S{split_id}-{repeat_id}{suffix}'
			for e_id, epoch in enumerate(epochs):
				result_file = os.path.join(result_dir, naming, f'{subset}_results_{mode}_epoch{epoch}.npy')
				try:
					result = np.load(result_file, allow_pickle=True).item()
					results[r_id, s_id, e_id] = result[result_key]
				except Exception as exception:
					results[r_id, s_id, e_id] = np.nan
					print(exception, result_file)

	results = results * 100

	return results.mean(), results.mean(2).std(1).mean(0)


# To add STD summary (STD cross splits?)
####################################################################################################

print('All Same: Select on Test')

result_dir = '/g/data/zg12/result'
mode = 'decoder-agg'
repeat_ids = [0, 1, 2]
split_ids = [1, 2, 3, 4, 5]
# split_ids = [1]
# epochs = [i for i in range(100, 1101, 100)]
epochs = [400, 500]
window_size = 2

naming_paris = [

	# ['RDV-T45RealExp1st', '-baseline-R1'],
	# ['RDV-T45RealExp1st', '-baseline-R2'],
	# ['RDV-T45RealExp1st', '-baseline-R3'],
	['RDV-T45RealExp2nd', '-baseline-R1'], # Selected
	# ['RDV-T45RealExp2nd', '-baseline-R2'],
	# ['RDV-T45RealExp2nd', '-baseline-R3'],

	['RDV-T45RealExp1stExtra', '-causal-False'], # Selected
	# ['RDV-T45RealExp2nd', '-causal-False'],

	# ['RDV-T50RealExp1st', '-baseline-R1'],
	['RDV-T50RealExp1st', '-baseline-R2'], # Selected
	# ['RDV-T50RealExp1st', '-baseline-R3'],
	# ['RDV-T50RealExp2nd', '-baseline-R1'],
	# ['RDV-T50RealExp2nd', '-baseline-R2'],
	# ['RDV-T50RealExp2nd', '-baseline-R3'],

	# ['RDV-T50RealExp1st', '-causal-False'],
	['RDV-T50RealExp2nd', '-causal-False'], # selected

	['RDV-T50RealExp1stExtra', '-class_weighting-ivt'], # selected
	# ['RDV-T50RealExp2nd', '-class_weighting-ivt'],

	['RDV-T50RealExp1st', '-class_weighting-i_v_t'], # selected
	# ['RDV-T50RealExp2nd', '-class_weighting-i_v_t'],

	['RDV-T50RealExp1st', '-class_weighting-ivt_i_v_t'], # selected
	# ['RDV-T50RealExp2nd', '-class_weighting-ivt_i_v_t'],

	['RDV-T50RealExp1st', '-diffusion_cross_att_decoder-True'], # selected 
	# ['RDV-T50RealExp2nd', '-diffusion_cross_att_decoder-True'],

	['RDV-T50RealExp1st', '-target_components-ivt'], # selected
	# ['RDV-T50RealExp2nd', '-target_components-ivt'],

	['RDV-T50RealExp1st', '-target_components-ivt_i_v_t_iv_it'], # selected
	# ['RDV-T50RealExp2nd', '-target_components-ivt_i_v_t_iv_it'],

	['RDV-T50RealExp1stInfer', '-diffusion_guidance_scale-0.0'], # all selected, 400, 500, 'RDV-T50RealExp1st', '-baseline-R2'
	# ['RDV-T50RealExp1stInfer', '-diffusion_guidance_scale-0.25'],
	['RDV-T50RealExp1stInfer', '-diffusion_guidance_scale-0.5'],
	# ['RDV-T50RealExp1stInfer', '-diffusion_guidance_scale-0.75'],
	['RDV-T50RealExp1stInfer', '-diffusion_guidance_scale-1.0'],
	# ['RDV-T50RealExp1stInfer', '-diffusion_sampling_timesteps-1'],
	# ['RDV-T50RealExp1stInfer', '-diffusion_sampling_timesteps-2'],
	# ['RDV-T50RealExp1stInfer', '-diffusion_sampling_timesteps-4'],
	# ['RDV-T50RealExp1stInfer', '-diffusion_sampling_timesteps-8'],
	# ['RDV-T50RealExp1stInfer', '-diffusion_sampling_timesteps-16'],
	# ['RDV-T50RealExp1stInfer', '-diffusion_sampling_timesteps-32'],
	# ['RDV-T50RealExp1stInfer', '-diffusion_sampling_timesteps-64'],
	# ['RDV-T50RealExp1stInfer', '-diffusion_sampling_timesteps-128'],

	# ['Swin-T45InitTry', '-feature_prefix-feature-SelfDistillSwin'],
	['Swin-T45RealExp2nd', '-baseline-R1'], # selected
	# ['Swin-T45RealExp2nd', '-baseline-R2'],
	# ['Swin-T45RealExp2nd', '-baseline-R3'],
	['Swin-T45RealExp2nd', '-causal-False'],

	# ['Swin-T50RealExp2nd', '-baseline-R1'],
	['Swin-T50RealExp2nd', '-baseline-R2'],
	# ['Swin-T50RealExp2nd', '-baseline-R3'],
	['Swin-T50RealExp2nd', '-causal-False'],


	# ['RDV-ChallengeInitTry', '-causal-False'],
	# ['RDV-ChallengeInitTry', '-weight_decay-1e-06'],
	# ['RDV-ChallengeInitTry', '-weight_decay-1e-05'],
	# ['RDV-ChallengeInitTry', '-weight_decay-2e-05'],
	# ['RDV-ChallengeInitTry', '-weight_decay-5e-05'],
	# ['RDV-ChallengeInitTry', '-weight_decay-0.0001'],

]

all_results_aps = {}
all_results_topns = {}

for prefix, suffix in naming_paris:
	selected_epochs, selected_value = get_best_epochs(result_dir, prefix, suffix, mode, 'test', repeat_ids, split_ids, epochs, window_size, result_key='AP_IVT')
	print(selected_epochs)

	AP_I_mean, AP_I_std = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, split_ids, selected_epochs, result_key='AP_I')
	AP_V_mean, AP_V_std = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, split_ids, selected_epochs, result_key='AP_V')
	AP_T_mean, AP_T_std = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, split_ids, selected_epochs, result_key='AP_T')
	AP_IV_mean, AP_IV_std = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, split_ids, selected_epochs, result_key='AP_IV')
	AP_IT_mean, AP_IT_std = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, split_ids, selected_epochs, result_key='AP_IT')
	AP_IVT_mean, AP_IVT_std = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, split_ids, selected_epochs, result_key='AP_IVT')
	result_line1 = f'{AP_I_mean:.1f}±{AP_I_std:.1f} & {AP_V_mean:.1f}±{AP_V_std:.1f} & {AP_T_mean:.1f}±{AP_T_std:.1f} & {AP_IV_mean:.1f}±{AP_IV_std:.1f} & {AP_IT_mean:.1f}±{AP_IT_std:.1f} & {AP_IVT_mean:.1f}±{AP_IVT_std:.1f}'
	all_results_aps[''.join([prefix, suffix])] = result_line1

	Top1_mean, Top1_std = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, split_ids, selected_epochs, result_key='Top-1')
	Top5_mean, Top5_std = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, split_ids, selected_epochs, result_key='Top-5')
	Top10_mean, Top10_std = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, split_ids, selected_epochs, result_key='Top-10')
	Top20_mean, Top20_std = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, split_ids, selected_epochs, result_key='Top-20')

	result_line2 = f'{Top1_mean:.1f}±{Top1_std:.1f} & {Top5_mean:.1f}±{Top5_std:.1f} & {Top10_mean:.1f}±{Top10_std:.1f} & {Top20_mean:.1f}±{Top20_std:.1f}'
	all_results_topns[''.join([prefix, suffix])] = result_line2


for key in all_results_aps.keys():
	print(key)
	print(all_results_aps[key])
	print(all_results_topns[key])
	print('')


# ####################################################################################################

# print('All Same: Select on Val')

# result_dir = './result'
# mode = 'decoder-agg'
# repeat_ids = [0]
# split_ids = [1, 2, 3, 4, 5]
# epochs = [i for i in range(0, 12001, 150)]
# window_size = 3

# naming_paris = [
# 	['RDV-IVT131FullValCV', '-baseline-None'],
# 	['RDV-IVT131FullValCV', '-decoder_num_f_maps-64'],
# 	['RDV-IVT131FullValCV', '-encoder_num_f_maps-64'],
# ]

# all_results = {}

# for prefix, suffix in naming_paris:
# 	selected_epochs, selected_value = get_best_epochs(result_dir, prefix, suffix, mode, 'val', repeat_ids, split_ids, epochs, window_size)
# 	selected_result = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, split_ids, selected_epochs)
# 	all_results[''.join([prefix, suffix])] = selected_result

# for key in all_results.keys():
# 	print(key, all_results[key])

# ####################################################################################################

# print('Per Split: Select on Test')

# result_dir = './result'
# mode = 'decoder-agg'
# repeat_ids = [0]
# split_ids = [1, 2, 3, 4, 5]
# epochs = [i for i in range(0, 12001, 150)]
# window_size = 3

# naming_paris = [
# 	['RDV-IVT131FullCV', '-baseline-None'],
# 	['RDV-IVT131FullCV', '-decoder_num_f_maps-64'],
# 	['RDV-IVT131FullCV', '-encoder_num_f_maps-64'],
# 	['RDV-IVT131FullValCV', '-baseline-None'],
# 	['RDV-IVT131FullValCV', '-decoder_num_f_maps-64'],
# 	['RDV-IVT131FullValCV', '-encoder_num_f_maps-64'],
# ]

# all_results = {}

# for prefix, suffix in naming_paris:
# 	all_results[''.join([prefix, suffix])] = []
# 	for split_id in split_ids:
# 		selected_epochs, selected_value = get_best_epochs(result_dir, prefix, suffix, mode, 'test', repeat_ids, [split_id], epochs, window_size)
# 		selected_result = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, [split_id], selected_epochs)
# 		all_results[''.join([prefix, suffix])].append(selected_result)
# 	all_results[''.join([prefix, suffix])] = np.mean(all_results[''.join([prefix, suffix])])

# for key in all_results.keys():
# 	print(key, all_results[key])

# ####################################################################################################

# print('Per Split: Select on Val')

# result_dir = './result'
# mode = 'decoder-agg'
# repeat_ids = [0]
# split_ids = [1, 2, 3, 4, 5]
# epochs = [i for i in range(0, 12001, 150)]
# window_size = 3

# naming_paris = [
# 	['RDV-IVT131FullValCV', '-baseline-None'],
# 	['RDV-IVT131FullValCV', '-decoder_num_f_maps-64'],
# 	['RDV-IVT131FullValCV', '-encoder_num_f_maps-64'],
# ]

# all_results = {}

# for prefix, suffix in naming_paris:
# 	all_results[''.join([prefix, suffix])] = []
# 	for split_id in split_ids:
# 		selected_epochs, selected_value = get_best_epochs(result_dir, prefix, suffix, mode, 'val', repeat_ids, [split_id], epochs, window_size)
# 		selected_result = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, [split_id], selected_epochs)
# 		all_results[''.join([prefix, suffix])].append(selected_result)
# 	all_results[''.join([prefix, suffix])] = np.mean(all_results[''.join([prefix, suffix])])

# for key in all_results.keys():
# 	print(key, all_results[key])

# ####################################################################################################

# print('Per Run: Select on Test')

# result_dir = './result'
# mode = 'decoder-agg'
# repeat_ids = [0]
# split_ids = [1, 2, 3, 4, 5]
# epochs = [i for i in range(0, 12001, 150)]
# window_size = 3

# naming_paris = [
# 	['RDV-IVT131FullCV', '-baseline-None'],
# 	['RDV-IVT131FullCV', '-decoder_num_f_maps-64'],
# 	['RDV-IVT131FullCV', '-encoder_num_f_maps-64'],
# 	['RDV-IVT131FullValCV', '-baseline-None'],
# 	['RDV-IVT131FullValCV', '-decoder_num_f_maps-64'],
# 	['RDV-IVT131FullValCV', '-encoder_num_f_maps-64'],
# ]

# all_results = np.zeros((len(naming_paris), len(split_ids)))

# for n_id, (prefix, suffix) in enumerate(naming_paris):
# 	for s_id, split_id in enumerate(split_ids):
# 		selected_epochs, selected_value = get_best_epochs(result_dir, prefix, suffix, mode, 'test', repeat_ids, [split_id], epochs, window_size)
# 		selected_result = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, [split_id], selected_epochs)
# 		all_results[n_id, s_id] = selected_result

# print('Best:', all_results.max(0).mean(0))

# ####################################################################################################

# print('Per Run: Select on Val')

# result_dir = './result'
# mode = 'decoder-agg'
# repeat_ids = [0]
# split_ids = [1, 2, 3, 4, 5]
# epochs = [i for i in range(0, 12001, 150)]
# window_size = 3

# naming_paris = [
# 	['RDV-IVT131FullValCV', '-baseline-None'],
# 	['RDV-IVT131FullValCV', '-decoder_num_f_maps-64'],
# 	['RDV-IVT131FullValCV', '-encoder_num_f_maps-64'],
# ]

# all_results = np.zeros((len(naming_paris), len(split_ids)))

# for n_id, (prefix, suffix) in enumerate(naming_paris):
# 	for s_id, split_id in enumerate(split_ids):
# 		selected_epochs, selected_value = get_best_epochs(result_dir, prefix, suffix, mode, 'val', repeat_ids, [split_id], epochs, window_size)
# 		selected_result = get_result(result_dir, prefix, suffix, mode, 'test', repeat_ids, [split_id], selected_epochs)
# 		all_results[n_id, s_id] = selected_result

# print('Best:', all_results.max(0).mean(0))

# ####################################################################################################

# repeat_ids are all averaged, none is selecting the best






####################################################################################################

# print('Temp')

# result_dir = './result'
# mode = 'decoder-agg'
# repeat_ids = [0]
# split_ids = [1]
# epochs = [1950]
# window_size = 1


# print(get_result(result_dir, 'RDV-IVT131FullCV', '-baseline-None', mode, 'test', repeat_ids, split_ids, epochs))
