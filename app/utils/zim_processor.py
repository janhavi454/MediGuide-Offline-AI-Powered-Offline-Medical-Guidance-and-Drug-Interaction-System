from zimply.zimply import ZIMFile
import json
import re
import html
from tqdm import tqdm
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class MedicalZIMProcessor:
    def __init__(self, zim_path):
        self.zim_path = zim_path
        self.medical_categories = {
            'disease', 'symptom', 'treatment', 'medication', 'drug',
            'surgery', 'diagnosis', 'therapy', 'pharmacology', 'anatomy',
            'physiology', 'first_aid', 'emergency', 'side_effect',
            'interaction', 'prevention', 'screening', 'vaccine', 'vitamin'
        }
    
    def clean_html(self, raw_html):
        """Remove HTML tags and decode HTML entities from text"""
        if not raw_html:
            return ""
        
        text = html.unescape(raw_html)
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', text)
        cleantext = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', cleantext)
        cleantext = re.sub(r'\s+', ' ', cleantext).strip()
        
        return cleantext
    
    def is_medical_article(self, title, content):
        """Check if article is medical-related"""
        title_lower = title.lower()
        content_lower = content.lower()
        
        title_medical = any(term in title_lower for term in self.medical_categories)
        content_medical = any(term in content_lower for term in self.medical_categories)
        
        medical_patterns = {
            'itis', 'osis', 'opathy', 'ectomy', 'otomy', 'scopy',
            'ology', 'emia', 'algia', 'derma', 'cardia', 'pnea'
        }
        
        pattern_medical = any(title_lower.endswith(pattern) or 
                             f' {pattern} ' in title_lower 
                             for pattern in medical_patterns)
        
        return title_medical or content_medical or pattern_medical
    
    def chunk_text(self, text, chunk_size=400, overlap=50):
        """Split text into overlapping chunks"""
        words = text.split()
        if len(words) <= chunk_size:
            return [text]

        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
            if i + chunk_size >= len(words):
                break
        return chunks

    def summarize_text(self, text, max_length=400):
        """Generate a summary of the text"""
        if len(text) <= max_length:
            return text

        # Simple extractive summarization as fallback
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= 3:
            return text[:max_length] + "..."

        # Take first and last sentences, and middle if available
        summary_sentences = []
        summary_sentences.append(sentences[0])  # First sentence

        if len(sentences) > 2:
            summary_sentences.append(sentences[len(sentences)//2])  # Middle sentence

        if len(sentences) > 1:
            summary_sentences.append(sentences[-1])  # Last sentence

        summary = '. '.join(summary_sentences)
        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."

        return summary

    def generate_llm_summary(self, text, title=""):
        """Generate summary using LLM if available, otherwise extractive"""
        try:
            import litellm
            prompt = f"Summarize the following medical article in 2-3 sentences:\n\nTitle: {title}\n\nContent: {text[:2000]}"  # Limit content length

            messages = [
                {"role": "system", "content": "You are a medical expert who creates concise, accurate summaries."},
                {"role": "user", "content": prompt}
            ]

            response = litellm.completion(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.3
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"LLM summarization failed: {e}. Using extractive summarization.")
            return self.summarize_text(text)
    
    def process_articles(self, output_dir="app/data/medical_wikipedia_data"):
        """Process all articles in the ZIM file"""
        
        os.makedirs(output_dir, exist_ok=True)
        all_articles = []
        medical_articles = []
        
        try:
            print(f"Opening ZIM file: {self.zim_path}")
            # Open ZIM file with explicit encoding
            zim = ZIMFile(self.zim_path, encoding="utf-8")
            
            total_entries = len(zim)
            print(f"Total entries found: {total_entries:,}")
            
            # Iterate through ZIM file entries using index-based access
            for i in tqdm(range(total_entries), desc="Processing articles"):
                try:
                    # Get the directory entry by index
                    dir_entry = zim.read_directory_entry_by_index(i)
                    
                    # Check if it's an article entry (not a redirect)
                    if 'redirectIndex' not in dir_entry:
                        # Get the article content
                        article = zim._get_article_by_index(i)
                        
                        if article and article.mimetype == 'text/html':
                            # Decode the article content
                            try:
                                html_content = article.data.decode('utf-8', errors='ignore')
                            except Exception:
                                try:
                                    html_content = article.data.decode('latin-1', errors='ignore')
                                except Exception:
                                    html_content = str(article.data)
                            
                            plain_text = self.clean_html(html_content)
                            
                            if len(plain_text) > 200:
                                article_data = {
                                    "id": i,  # Using index as ID
                                    "title": dir_entry['title'],
                                    "url": dir_entry['url'],
                                    "content": plain_text,
                                    "length": len(plain_text),
                                    "is_medical": self.is_medical_article(
                                        dir_entry['title'],
                                        plain_text
                                    )
                                }
                                
                                all_articles.append(article_data)
                                if article_data['is_medical']:
                                    medical_articles.append(article_data)
                                    
                except Exception as e:
                    print(f"Error processing entry {i}: {e}")
                    continue
            
            # Save all files to data/ folder
            all_output_path = os.path.join(output_dir, "all_articles.json")
            with open(all_output_path, 'w', encoding='utf-8') as f:
                json.dump(all_articles, f, indent=2, ensure_ascii=False)
            
            medical_output_path = os.path.join(output_dir, "medical_articles.json")
            with open(medical_output_path, 'w', encoding='utf-8') as f:
                json.dump(medical_articles, f, indent=2, ensure_ascii=False)
            
            self.create_summaries(medical_articles, output_dir)
            
            print(f"\nProcessing complete!")
            print(f"Total articles processed: {len(all_articles):,}")
            print(f"Medical articles identified: {len(medical_articles):,}")
            print(f"Files saved to: {output_dir}")
            
            return {
                "status": "success",
                "total_articles": len(all_articles),
                "medical_articles": len(medical_articles),
                "output_dir": output_dir
            }
            
        except Exception as e:
            error_msg = f"Error processing ZIM file: {e}"
            print(error_msg)
            return {"status": "error", "message": error_msg}
    
    def create_chunks(self, articles, output_dir, chunk_size=400):
        """Create chunks for vector database"""
        chunks = []
        chunk_id = 0
        
        for article in tqdm(articles, desc="Creating chunks"):
            article_chunks = self.chunk_text(article['content'], chunk_size)
            
            for chunk_index, chunk_content in enumerate(article_chunks):
                chunk_data = {
                    "id": f"{article['id']}_chunk{chunk_index}",
                    "article_title": article['title'],
                    "article_url": article['url'],
                    "chunk_index": chunk_index,
                    "content": chunk_content,
                    "length": len(chunk_content),
                    "source": "wikipedia_medical_mini"
                }
                chunks.append(chunk_data)
                chunk_id += 1
        
        chunks_path = os.path.join(output_dir, "medical_chunks.json")
        with open(chunks_path, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
        print(f"Created {len(chunks):,} chunks from {len(articles):,} medical articles")

    def create_summaries(self, articles, output_dir):
        """Create summaries for articles"""
        summaries = []

        for article in tqdm(articles, desc="Creating summaries"):
            # Generate summary using LLM or fallback
            summary_text = self.generate_llm_summary(article['content'], article['title'])

            summary_data = {
                "id": article['id'],
                "title": article['title'],
                "url": article['url'],
                "summary": summary_text,
                "summary_length": len(summary_text),
                "original_length": article['length'],
                "source": "wikipedia_medical_mini"
            }
            summaries.append(summary_data)

        summaries_path = os.path.join(output_dir, "medical_summaries.json")
        with open(summaries_path, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, indent=2, ensure_ascii=False)

        print(f"Created {len(summaries):,} summaries from {len(articles):,} medical articles")

# Standalone function to run the processor
def process_medical_wikipedia():
    """Process the medical Wikipedia ZIM file"""
    zim_filename = "app/data/wikipedia_en_medicine_mini_2025-08.zim"
    output_directory = "app/data/medical_wikipedia_data"
    
    if not os.path.exists(zim_filename):
        return {
            "status": "error",
            "message": f"ZIM file '{zim_filename}' not found. Please place it in the app/data/ folder."
        }
    
    print(f"Processing Medical Wikipedia ZIM file from app/data folder...")
    print("=" * 60)
    
    processor = MedicalZIMProcessor(zim_filename)
    return processor.process_articles(output_directory)

if __name__ == "__main__":
    # Allow running this file standalone
    result = process_medical_wikipedia()
    print(result)  # Print the result of processing
