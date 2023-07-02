STATES = {
  state: i
  for i, state in enumerate([
    "transaction_branch_command",
    "transaction_add_branch_category",
    "transaction_add_loop_amount",
    "transaction_add_branch_description",
    "transaction_add_branch_confirmation"
  ])
}

CATEGORIES = [
  "Food",
  "Entertainment",
  "Park"
]