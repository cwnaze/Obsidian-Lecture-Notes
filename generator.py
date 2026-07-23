import re
from typing import List, Dict, Any, Callable
from processing import TranscriptProcessor

class NoteGenerator:
    """
    Orchestrates the transformation of a raw transcript into a structured note
    by processing chunks via an LLM and mapping results to specific H2 headers.
    """

    def __init__(self, llm_fn: Callable[[str], str], system_prompts: Dict[str, str]):
        """
        Args:
            llm_fn: A callable that takes a prompt and returns the LLM's response.
            system_prompts: A dictionary mapping header keys (e.g., 'summary', 'action_items')
                            to their respective system instructions.
        """
        self.llm_fn = llm_fn
        self.system_prompts = system_prompts
        self.processor = TranscriptProcessor()

    def generate_note(self, transcript: str) -> str:
        """
        Processes a full transcript and returns a structured markdown note.
        """
        # 1. Chunk the transcript to handle long inputs
        chunks = self.processor.chunk_transcript(transcript)
        
        # 2. Map to produce content for each desired H2 header
        note_sections = {}
        
        for header_key, prompt in self.system_prompts.items():
            # We process each header's requirement across all chunks
            # In a production setting, this could be done in parallel.
            section_content = self._process_section(header_key, prompt, chunks)
            note_sections[header_key] = section_content

        # 3. Assemble the final note
        return self._assemble_note(note_sections)

    def _process_section(self, header_key: str, prompt: str, chunks: List[str]) -> str:
        """
        Processes the transcript chunks to extract information relevant to a specific header.
        """
        summaries = []
        
        # We use the processor's summarize_chunks logic but with our specific section prompt
        def section_summarizer(chunk_text: str) -> str:
            full_prompt = f"{prompt}\n\nTEXT TO PROCESS:\n{chunk_text}"
            return self.llm_fn(full_prompt)

        summaries = self.processor.summarize_chunks(chunks, section_summarizer)
        
        # Final synthesis step: Combine the chunk-level extractions into one cohesive section
        combined_text = "\n\n".join(summaries)
        synthesis_prompt = (
            f"{prompt}\n\n"
            "The following are partial extractions from different parts of the transcript. "
            "Please synthesize them into a single, cohesive, and non-redundant section. "
            "Maintain the requested format and omit any meta-commentary (like 'Here is the summary').\n\n"
            f"PARTIAL EXTRACTIONS:\n{combined_text}"
        )
        
        return self.llm_fn(synthesis_prompt).strip()

    def _assemble_note(self, sections: Dict[str, str]) -> str:
        """
        Converts the sections dictionary into a Markdown string with H2 headers.
        """
        markdown_lines = []
        for header_key, content in sections.items():
            # Convert key to title case for the H2 header (e.g., 'action_items' -> 'Action Items')
            title = header_key.replace('_', ' ').title()
            markdown_lines.append(f"## {title}")
            markdown_lines.append(content)
            markdown_lines.append("") # Add spacing
            
        return "\n".join(markdown_lines).strip()

# Example usage / Mock testing
if __name__ == "__main__":
    # Mock LLM function
    def mock_llm(prompt: str) -> str:
        if "Summary" in prompt: return "This is a synthesized summary of the meeting."
        if "Action Items" in prompt: return "- Item 1\n- Item 2"
        return "Generic LLM response"

    # Define prompts for the headers we want
    prompts = {
        "summary": "Provide a concise summary of the key discussion points.",
        "action_items": "Extract a bulleted list of all commitments and action items."
    }

    generator = NoteGenerator(llm_fn=mock_llm, system_prompts=prompts)
    transcript = "This is a long transcript. " * 500 # Force chunking
    result = generator.generate_note(transcript)
    print(result)
