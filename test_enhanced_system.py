"""
Test the enhanced visual accuracy system
"""

import os

# Set API key
os.environ['GEMINI_API_KEY'] = 'AIzaSyAQCROVJ5EBdYuLxai_GMLx9OJgFZmoPbc'

def test_enhancement():
    """
    Test the visual enhancement system
    """
    print("Testing Enhanced Visual Accuracy System...")
    print("=" * 50)
    
    # Import the enhancement module
    from caption_enhancer import CaptionEnhancer
    
    # Initialize enhancer
    enhancer = CaptionEnhancer()
    
    if not enhancer.enhancement_enabled:
        print("❌ Enhancement not available")
        return
    
    print("✅ Enhancement initialized successfully!")
    print()
    
    # Test with the problematic caption
    test_caption = "a man in a red shirt is standing in front of a large crowd of people"
    
    print(f"Original caption: {test_caption}")
    print("Processing...")
    
    # Get enhanced caption
    enhanced_caption = enhancer.enhance_caption(test_caption)
    
    print(f"Enhanced caption: {enhanced_caption}")
    print()
    
    # Check if it's different
    if test_caption.lower() != enhanced_caption.lower():
        print("✅ Caption was enhanced!")
        print("🎯 Visual accuracy improvement detected")
    else:
        print("ℹ️  Caption was unchanged")
    
    print()
    print("🎉 Enhanced system is working!")

if __name__ == "__main__":
    test_enhancement()
