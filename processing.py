import re
from typing import List, Dict, Any

class TranscriptProcessor:
    """
    Handles the chunking and preparation of long transcripts for LLM processing.
    Ensures chunks fit within context limits while attempting to preserve 
    semantic coherence by splitting at natural boundaries.
    """
    
    def __init__(self, max_tokens: int = 4000, overlap_tokens: int = 200):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        # Approximation of tokens per character (roughly 0.25-0.3 tokens per char for English)
        self.char_per_token = 4 

    def _estimate_tokens(self, text: str) -> int:
        """Simple token estimation. In production, use tiktoken or similar."""
        return len(text) // self.char_per_token

    def chunk_transcript(self, text: str) -> List[str]:
        """
        Splits a transcript into chunks that fit within max_tokens.
        Tries to split at paragraphs or sentences to preserve coherence.
        """
        if not text:
            return []

        chunks = []
        start_char = 0
        text_len = len(text)

        while start_char < text_len:
            # Calculate available window for this chunk
            # Subtract overlap from the first chunk if it's not the start
            effective_max = self.max_tokens if not chunks else (self.max_tokens - self.overlap_tokens)
            char_limit = effective_max * self.char_per_token
            
            end_char = start_char + char_limit
            
            if end_char >= text_len:
                chunks.append(text[start_char:])
                break
            
            # Try to find a natural break point within the limit
            chunk_candidate = text[start_char:end_char]
            
            # Priority for break points: Paragraph -> Sentence -> Space
            break_point = -1
            for separator in ['\n\n', '\n', '. ', ' ']:
                idx = chunk_candidate.rfind(separator)
                if idx != -1:
                    break_point = idx + len(separator)
                    # If we found a strong break (paragraph/newline), take it
                    if separator in ['\n\n', '\n']:
                        break
            
            if break_point == -1:
                # Hard cut if no natural break found
                end_char = start_char + char_limit
            else:
                end_char = start_char + break_point

            chunks.append(text[start_char:end_char])
            
            # Move start_char forward, accounting for overlap
            # The next chunk starts 'overlap_tokens' back from the current end_char
            overlap_char = self.overlap_tokens * self.char_per_token
            start_char = max(end_char - overlap_char, start_char + 1)
            
            # Ensure we don't get stuck if overlap is larger than the chunk
            if start_char >= end_char and len(chunks) > 0:
                # This is a safety fallback to prevent infinite loops
                start_char = end_char

        return chunks

    def summarize_chunks(self, chunks: List[str], summarizer_fn) -> List[str]:
        """
        Processes chunks through a provided summarization function.
        The summarizer_fn should be a callable that takes text and returns a summary.
        """
        summaries = []
        for i, chunk in enumerate(chunks):
            # Add metadata to the chunk for the summarizer
            context_prompt = f"Chunk {i+1}/{len(chunks)}\n---\n{chunk}"
            summaries.append(summarizer_fn(context_prompt))
        return summaries

# Example usage / minimal test
if __name__ == "__main__":
    processor = TranscriptProcessor(max_tokens=100, overlap_tokens=20)
    sample_text = "This is a long transcript. " * 100
    chunks = processor.chunk_transcript(sample_text)
    print(f"Split into {len(chunks)} chunks.")
    for i, c in enumerate(chunks):
        print(f"Chunk {i+1} length: {len(c)} chars")
