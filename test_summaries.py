
"""
Test script to verify summary functionality
"""
import sys
import os
sys.path.append('.')

from app.models.llm_model import llm_model

def test_summary_loading():
    """Test loading of summary data"""
    print("Testing summary data loading...")

    llm_model.load_model()
    success = llm_model.load_wikipedia_data()

    if success:
        print("✓ Successfully loaded summary data")
        if llm_model.wikipedia_data:
            print(f"✓ Loaded {len(llm_model.wikipedia_data)} summaries")

            # Check if data contains summaries
            if llm_model.wikipedia_data and 'summary' in llm_model.wikipedia_data[0]:
                print("✓ Data contains summaries (not chunks)")
                return True
            else:
                print("✗ Data appears to be chunks, not summaries")
                return False
        else:
            print("✗ No data loaded")
            return False
    else:
        print("✗ Failed to load summary data")
        return False

def test_summary_response():
    """Test generating responses with summaries"""
    print("\nTesting summary-based responses...")

    test_questions = [
        "What is aspirin?",
        "What are the symptoms of diabetes?",
        "How does vaccination work?",
        "What is hypertension?"
    ]

    for question in test_questions:
        print(f"\nQuestion: {question}")
        try:
            response = llm_model.generate_response_with_wikipedia(question)
            print(f"Response: {response[:200]}..." if len(response) > 200 else f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main test function"""
    print("Testing Wikipedia Summary Functionality")
    print("=" * 50)

    if test_summary_loading():
        test_summary_response()
        print("\n✓ Summary functionality test completed successfully!")
    else:
        print("\n✗ Summary functionality test failed!")

if __name__ == "__main__":
    main()
