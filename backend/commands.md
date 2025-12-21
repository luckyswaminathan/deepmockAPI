python3 scripts/run_rl_agent.py \
    --backend-url http://localhost:8000 \
    --goal-file scripts/stripe_subscription_goal.json \
    --actions-file scripts/stripe_subscription_actions.json \
    --export-datasets \
    --dataset-dir generated_output/datasets/stripe \
    --sft-min-reward -1 \
    --push-finetune \
    --sft-model gpt-3.5-turbo-0125