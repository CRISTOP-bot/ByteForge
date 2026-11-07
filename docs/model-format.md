# ByteForge n-gram model format, version 1

UTF-8 text file with tab-separated records; current trainer writes ASCII-safe hex for vocabulary entries. Newlines delimit records.

- Header: `BYTEFORGE_NGRAM_V1<TAB>order<TAB>vocabulary_size<TAB>bos_id`
- Vocabulary: `v<TAB>token_id<TAB>UTF8_HEX`
- Transition: `n<TAB>context_id_0...context_id_(order-1)<TAB>next_token_id<TAB>frequency`

IDs are nonnegative decimal integers. Token IDs are contiguous from 0 through `vocabulary_size - 1`; `bos_id` equals the vocabulary size and is reserved for start-of-text padding. Frequencies are positive integers. Runtime must reject malformed headers, invalid IDs, invalid UTF-8, nonpositive order, and zero/negative frequencies rather than reading out of bounds.

The current trainer creates fixed-width order contexts, pads the beginning with BOS, and counts the next token. The reference generator deterministically chooses the most frequent valid continuation. Other runtimes use the same rule, breaking ties by the lowest token ID.
