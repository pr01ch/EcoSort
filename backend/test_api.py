#!/usr/bin/env python3
"""
Test script to verify Gemini API setup
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("🧪 Testing Gemini API Configuration\n")

# Check API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key or api_key == 'your_gemini_api_key_here':
    print("GEMINI_API_KEY not set in .env file")
    print("Please edit .env and add your API key")
    exit(1)

print(f"✅ API Key found: {api_key[:20]}...")

# Configure Gemini
try:
    genai.configure(api_key=api_key)
    print("✅ Gemini API configured successfully")
except Exception as e:
    print(f"❌ Error configuring API: {e}")
    exit(1)

# Test text model
print("\n📝 Testing text model (gemini-flash-latest)...")
try:
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content("Say 'Hello' if you can hear me.")
    print(f"✅ Text model works: {response.text}")
except Exception as e:
    print(f"❌ Text model error: {e}")
    exit(1)

# Test vision capabilities
print("\n👁️  Testing vision model (gemini-flash-latest)...")
try:
    vision_model = genai.GenerativeModel('gemini-flash-latest')
    # Create a simple test image file
    import PIL.Image
    import os
    
    # Create test image file
    test_img_path = 'test_image.png'
    img = PIL.Image.new('RGB', (100, 100), color='red')
    img.save(test_img_path)
    
    # Load image from file
    img = PIL.Image.open(test_img_path)
    response = vision_model.generate_content(["What color is this image?", img])
    print(f"✅ Vision model works: {response.text}")
    
    # Clean up
    if os.path.exists(test_img_path):
        os.remove(test_img_path)
except Exception as e:
    print(f"❌ Vision model error: {e}")
    print(f"   Full error: {repr(e)}")
    exit(1)

print("\n🎉 All tests passed! Your Gemini API is configured correctly.")
print("\nYou can now run: python app.py")
