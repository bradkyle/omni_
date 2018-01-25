from enum import Enum
import re
import numpy as np

class PROCESSING(Enum):
    ONE_HOT = 0
    DISCRETE = 1
    ONE_HOT_UNPADDED = 2
    DISCRETE_UNPADDED = 4

async def process(input,
                  protocol=PROCESSING.ONE_HOT,
                  max_length=1000,
                  padding_char=" ",
                  charset="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{}\n"
                  ):
    if type(input) is not str:
        input = str(input)

    # replace
    input = re.sub('\n', '', input)
    input = re.sub('\r', '', input)
    input = re.sub('  ', '', input)

    # encoding and padding
    input = list(input)
    num_padding = max_length - len(input)

    if protocol != PROCESSING.ONE_HOT_UNPADDED or PROCESSING.DISCRETE_UNPADDED:
        input = input + [padding_char] * num_padding
    result = np.array([charset.find(char) for char in input], dtype=np.int8)
    res = result[:max_length]

    if protocol == PROCESSING.ONE_HOT:
        batch_one_hot = np.zeros(shape=[len(res.tolist()), len(charset), 1])
        for example_i, char_seq_indice in enumerate(res.tolist()):
            if char_seq_indice != -1:
                batch_one_hot[example_i][char_seq_indice][0] = 1

        return batch_one_hot
    elif protocol == PROCESSING.DISCRETE:
        return res
