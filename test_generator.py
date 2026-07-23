import unittest
from generator import NoteGenerator

class TestNoteGenerator(unittest.TestCase):
    def setUp(self):
        # Mock LLM that reflects the input to verify mapping and synthesis
        def mock_llm(prompt: str) -> str:
            if "synthesize" in prompt.lower():
                return f"Synthesized version of: {prompt.split('PARTIAL EXTRACTIONS:')[1].strip()}"
            if "Summary" in prompt:
                return "Summary Chunk"
            if "Action Items" in prompt:
                return "Action Item Chunk"
            return "Generic response"
        
        self.prompts = {
            "summary": "Summarize the text.",
            "action_items": "List action items."
        }
        self.generator = NoteGenerator(llm_fn=mock_llm, system_prompts=self.prompts)

    def test_generate_note_structure(self):
        transcript = "Small transcript."
        result = self.generator.generate_note(transcript)
        
        self.assertIn("## Summary", result)
        self.assertIn("## Action Items", result)
        self.assertIn("Synthesized version of", result)

    def test_chunking_integration(self):
        # Create a transcript long enough to trigger chunking
        # TranscriptProcessor defaults to 4000 tokens (~16k chars)
        long_transcript = "Long text. " * 2000 
        result = self.generator.generate_note(long_transcript)
        
        self.assertIn("## Summary", result)
        self.assertIn("## Action Items", result)

if __name__ == "__main__":
    unittest.main()
