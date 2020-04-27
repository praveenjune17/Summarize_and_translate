# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import sys
sys.path.insert(0, 'D:\\Local_run\\Summarize_and_translate\\scripts')
sys.path.insert(0, 'D:\\Local_run\\models')
import tensorflow as tf
tf.keras.backend.clear_session()
tf.random.set_seed(100)
import time
from tqdm import tqdm
from preprocess import create_dataset
from configuration import config
from calculate_metrics import mask_and_calculate_loss
from creates import log
from create_model import finalize_tokenizer_and_architecture
from local_tf_ops import (check_ckpt, eval_step, train_step, batch_run_check, 
                          evaluate_validation_set, training_results)

(source_tokenizer, target_tokenizer, _) = finalize_tokenizer_and_architecture()
val_dataset = create_dataset(
                             split='validation', 
                             source_tokenizer=source_tokenizer, 
                             target_tokenizer=target_tokenizer, 
                             from_=0, 
                             to=100, 
                             batch_size=1,
                             drop_remainder=True
                             )
count=0
for _ in val_dataset:
  count+=1
print(f'Total records count is {count}')
# if a checkpoint exists, restore the latest checkpoint.
ck_pt_mgr = check_ckpt(config.checkpoint_path)

step = 1
start_time = time.time()
(rouge_score, bert_score, bleu) = evaluate_validation_set(       
                                                      val_dataset.take(1),
                                                      step
                                                      )  
training_results(
                  step, 
                  rouge_score, 
                  bert_score,
                  bleu,
                  (time.time() - start_time),
                  'none'
                  )
sys.exit()
