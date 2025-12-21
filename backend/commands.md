python3 scripts/run_rl_agent.py \
    --backend-url http://localhost:8000 \
    --goal-file scripts/stripe_subscription_goal.json \
    --actions-file scripts/stripe_subscription_actions.json \
    --export-datasets \
    --dataset-dir generated_output/datasets/stripe \
    --sft-min-reward -1 \
    --push-finetune \
    --sft-model gpt-3.5-turbo-0125

cd backend
  python3 scripts/export_rl_dataset.py \
    --discover-all \
    --sft-min-reward -1 \
    --output-dir generated_output/datasets/stripe \
    --sft-file sft_merged.jsonl \
    --ppo-file ppo_merged.jsonl

3. Kick off SFT with the merged file:

  python3 scripts/push_finetune.py \
    --sft-file generated_output/datasets/stripe/sft_merged.jsonl \
    --sft-model gpt-3.5-turbo-0125 \
    --api-key $OPENAI_API_KEY

  4. When the SFT job finishes, copy its fine_tuned_model and start PPO:

  python3 scripts/push_finetune.py \
    --ppo-file generated_output/datasets/stripe/ppo_merged.jsonl \
    --ppo-model <fine_tuned_model_id> \
    --api-key $OPENAI_API_KEY