import random
from typing import List, Dict

class Party:
    def __init__(self, party_id: int, direction: str, start_index: int):
        self.id = party_id
        self.direction = direction  # 'forward' or 'backward'
        self.start_index = start_index  # Starting pad index for this party
        self.last_used_index = None  # Tracks the last pad index used by this party

class MultipartyOTPProtocol:
    def __init__(self, m: int, pad_length: int, d: int):
        self.m = m
        self.n = pad_length
        self.d = d
        self.used_indices = set()  # Tracks all used pad indices
        self.parties = []  # List of Party objects
        self.wasted_pads = 0

        # Initialize parties with directions and starting indices
        # Example for m=3: two forward parties, one backward
        # making it generalized for any value of m
        directions = ['forward' if i % 2 == 0 else 'backward' for i in range(self.m)]

        if self.m == 1:
            start_indices = [0]
        elif self.m == 2:
            start_indices = [0, pad_length - 1]
        else:
            start_indices = [0, pad_length - 1] + [
                (i * pad_length) // (self.m - 1) for i in range(1, self.m - 1)
            ]

        # this does not seems to be professional
        # if self.m == 3:
        #     directions = ['forward', 'backward', 'forward']
        #     start_indices = [0, pad_length - 1, pad_length // 2]
        # elif self.m == 4:
        #     directions = ['forward', 'backward', 'forward', 'backward']
        #     start_indices = [0, pad_length - 1, pad_length // 4, 3 * pad_length // 4]
        # elif self.m == 5:
        #     directions = ['forward', 'backward', 'forward', 'backward', 'forward']
        #     start_indices = [0, pad_length - 1, pad_length // 5, 2 * pad_length // 5, 3 * pad_length // 5]
        
        # print(directions)
        # print(start_indices)
        
        for i in range(m):
            self.parties.append(Party(i, directions[i], start_indices[i]))

    def send_message(self, sender_id: int) -> bool:
        """
        Simulate sending a message by the specified party.
        Returns True if successful, False if no pads are available.
        """
        sender = self.parties[sender_id]
        direction = sender.direction

        # Determine the next intended pad index for the sender
        if sender.last_used_index is None:
            # First message: use the starting index
            intended_index = sender.start_index
        else:
            if direction == 'forward':
                intended_index = sender.last_used_index + 1
            else:
                intended_index = sender.last_used_index - 1

        # Find the next valid pad that satisfies the d-separation rule
        while True:
            # Check if the index is out of bounds
            if intended_index < 0 or intended_index >= self.n:
                return False

            # Check if the pad is already used
            if intended_index in self.used_indices:
                self.wasted_pads += 1
                intended_index = intended_index + 1 if direction == 'forward' else intended_index - 1
                continue

            # Check d-separation from all other parties' last used pads
            safe = True
            for party in self.parties:
                if party.id == sender_id or party.last_used_index is None:
                    continue
                if abs(intended_index - party.last_used_index) < self.d:
                    safe = False
                    break

            if safe:
                break
            else:
                # Skip this pad and count it as wasted
                self.wasted_pads += 1
                intended_index = intended_index + 1 if direction == 'forward' else intended_index - 1

        # Mark the pad as used
        self.used_indices.add(intended_index)
        sender.last_used_index = intended_index
        return True

    def reset(self):
        """Reset the protocol state for a new simulation."""
        self.used_indices = set()
        self.wasted_pads = 0
        for party in self.parties:
            party.last_used_index = None
