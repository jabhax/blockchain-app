# average_block_rate.py

import time

from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS


blockchain = Blockchain()
times = []

# Check how long it takes to mine a block
for i in range(1, 1000):
    start_time = time.time_ns()
    blockchain.add_block(i)
    end_time = time.time_ns()

    time_to_mine = (end_time - start_time) / SECONDS
    times.append(time_to_mine)

    avg_time = sum(times) / len(times)

    print(f'New block difficulty: {blockchain.chain[-1].difficulty}')
    print(f'Time to mine new block: {time_to_mine}s')
    print(f'Average time to mine new blocks: {avg_time}s\n')
