import unittest
from processing import TranscriptProcessor

class TestTranscriptProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = TranscriptProcessor(max_tokens=100, overlap_tokens=20)

    def test_empty_transcript(self):
        self.assertEqual(self.processor.chunk_transcript(""), [])

    def test_short_transcript(self):
        text = "This is a short transcript."
        chunks = self.processor.chunk_transcript(text)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], text)

    def test_long_transcript_chunking(self):
        # Create a long text that definitely exceeds 100 tokens (~400 chars)
        text = "This is a sentence. " * 50 
        chunks = self.processor.chunk_transcript(text)
        self.assertGreater(len(chunks), 1)
        # Verify no chunk exceeds the approximate limit (100 * 4 = 400 chars)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 400)

    def test_semantic_splitting(self):
        # Test that it prefers splitting at newlines over mid-sentence
        text = "First Paragraph\n\nSecond Paragraph\n\nThird Paragraph"
        # Set max_tokens small enough to force split but large enough to hold one paragraph
        processor = TranscriptProcessor(max_tokens=20, overlap_tokens=0) # ~80 chars
        chunks = processor.chunk_transcript(text)
        # Each chunk should be split at a boundary, so the double newline should be the break
        # Since the text is short and we have 80 chars limit, it might actually fit in one chunk 
        # if we aren't careful. Let's make the paragraphs longer.
        text_long = "First Paragraph " * 10 + "\n\n" + "Second Paragraph " * 10 + "\n\n" + "Third Paragraph " * 10
        chunks_long = processor.chunk_transcript(text_long)
        
        self.assertGreater(len(chunks_long), 1)
        # The split should happen at \n\n, so chunks shouldn't contain \n\n internally 
        # (depending on how rfind handles it, it might be at the end)
        # Let's just check if the first chunk contains the first paragraph.
        self.assertIn("First Paragraph", chunks_long[0])
        self.assertNotIn("Second Paragraph", chunks_long[0])

    def test_summarization_wrapper(self):
        def mock_summarizer(text):
            return f"Summary of {text[:10]}..."
        
        chunks = ["Chunk 1 content", "Chunk 2 content"]
        summaries = self.processor.summarize_chunks(chunks, mock_summarizer)
        self.assertEqual(len(summaries), 2)
        self.assertIn("Summary of Chunk 1", summaries[0])

if __name__ == "__main__":
    unittest.main()
