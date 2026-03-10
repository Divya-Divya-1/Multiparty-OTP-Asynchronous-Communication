import random
from Divya_Navadia_Thaker_protocol import MultipartyOTPProtocol

def simulate_scenario_a(m: int, n: int, d: int, trials: int) -> float:
    """Scenario (a): Only one party repeatedly sends messages."""
    total_wasted = 0
    for _ in range(trials):
        protocol = MultipartyOTPProtocol(m, n, d)
        sender_id = random.randint(0, m-1)
        while protocol.send_message(sender_id):
            pass
        total_wasted += protocol.wasted_pads
    return total_wasted / trials

def simulate_scenario_b(m: int, n: int, d: int, trials: int) -> float:
    """Scenario (b): Two parties send messages alternately."""
    total_wasted = 0
    for _ in range(trials):
        protocol = MultipartyOTPProtocol(m, n, d)
        senders = random.sample(range(m), 2)
        current_sender = 0  # Alternate between the two senders
        while True:
            success = protocol.send_message(senders[current_sender])
            if not success:
                break
            current_sender = 1 - current_sender  # Toggle between 0 and 1
        total_wasted += protocol.wasted_pads
    return total_wasted / trials

def simulate_scenario_c(m: int, n: int, d: int, trials: int) -> float:
    """Scenario (c): All parties send messages with random probabilities."""
    total_wasted = 0
    max_value = 0
    for _ in range(trials):
        protocol = MultipartyOTPProtocol(m, n, d)
        # Generate random probabilities for each party
        probabilities = [random.random() for _ in range(m)]
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        while True:
            # Choose a sender based on probabilities
            sender_id = random.choices(range(m), weights=probabilities, k=1)[0]
            if not protocol.send_message(sender_id):
                break
        total_wasted += protocol.wasted_pads
        if protocol.wasted_pads > max_value:
            max_value = protocol.wasted_pads
    # print(max_value)
    return total_wasted / trials

if __name__ == "__main__":
    m = 4  # Number of parties
    n = 100  # Pad length
    d = 2  # Undelivery parameter
    trials = 6000

    # print((m-1)*d)

    # Run simulations
    avg_wasted_a = simulate_scenario_a(m, n, d, trials)
    avg_wasted_b = simulate_scenario_b(m, n, d, trials)
    avg_wasted_c = simulate_scenario_c(m, n, d, trials)

    print(f"Scenario (a) Average Wasted Pads: {avg_wasted_a:.2f}")
    print(f"Scenario (b) Average Wasted Pads: {avg_wasted_b:.2f}")
    print(f"Scenario (c) Average Wasted Pads: {avg_wasted_c:.2f}")
