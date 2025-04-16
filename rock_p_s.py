import random

emojis = {'r': '🪨', 's': '✂️', 'p': '📃'}
choices = ('r','p','s')
user_choice = input('Rock, paper, or scissors? (r/p/s): ').lower()
if user_choice not in choices:
  print('Invalid choice!')
random.choice(choices)
computer_choice = random.choice(choices)

print(f'You chose {emojis[user_choice]}' )
print(f'Computer chose {emojis[computer_choice]}' )
