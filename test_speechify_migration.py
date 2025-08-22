#!/usr/bin/env python3
"""
Test suite for Speechify TTS migration
This script tests the migration from edge-tts to Speechify API
"""

import os
import sys
import asyncio
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import base64

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from text_to_speech import tts, convert_edge_tts_voice_to_speechify, extract_language_from_voice
from voice_manager import VoicesManager, filter_voice_models


class TestSpeechifyMigration(unittest.TestCase):
    """Test cases for Speechify migration"""

    def setUp(self):
        """Set up test environment"""
        # Set a mock API key for testing
        os.environ['SPEECHIFY_API_KEY'] = 'test_api_key_12345'
        
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.test_output_file = os.path.join(self.temp_dir, 'test_output.mp3')

    def tearDown(self):
        """Clean up test environment"""
        # Remove test files
        if os.path.exists(self.test_output_file):
            os.remove(self.test_output_file)
        
        # Remove temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_convert_edge_tts_voice_to_speechify(self):
        """Test voice conversion from edge-tts format to Speechify"""
        # Test known mappings
        self.assertEqual(convert_edge_tts_voice_to_speechify("en-US-ChristopherNeural"), "scott")
        self.assertEqual(convert_edge_tts_voice_to_speechify("en-US-JennyNeural"), "sarah")
        self.assertEqual(convert_edge_tts_voice_to_speechify("en-GB-RyanNeural"), "scott")
        
        # Test Speechify voice IDs (should return as-is)
        self.assertEqual(convert_edge_tts_voice_to_speechify("scott"), "scott")
        self.assertEqual(convert_edge_tts_voice_to_speechify("sarah"), "sarah")
        
        # Test unknown voice (should default to scott)
        self.assertEqual(convert_edge_tts_voice_to_speechify("unknown-voice"), "scott")

    def test_extract_language_from_voice(self):
        """Test language extraction from voice names"""
        # Test edge-tts format
        self.assertEqual(extract_language_from_voice("en-US-ChristopherNeural"), "en-US")
        self.assertEqual(extract_language_from_voice("fr-FR-DeniseNeural"), "fr-FR")
        self.assertEqual(extract_language_from_voice("de-DE-KatjaNeural"), "de-DE")
        
        # Test Speechify voice IDs (should return None)
        self.assertIsNone(extract_language_from_voice("scott"))
        self.assertIsNone(extract_language_from_voice("sarah"))
        
        # Test invalid formats
        self.assertIsNone(extract_language_from_voice("invalid"))
        self.assertIsNone(extract_language_from_voice(""))

    @patch('text_to_speech.Speechify')
    def test_tts_function_success(self, mock_speechify):
        """Test successful TTS generation"""
        # Mock the Speechify client
        mock_client = MagicMock()
        mock_speechify.return_value = mock_client
        
        # Mock the TTS response
        mock_response = MagicMock()
        mock_response.audio_data = base64.b64encode(b"fake_audio_data").decode('utf-8')
        mock_client.tts.audio.speech.return_value = mock_response
        
        # Test TTS generation
        result = asyncio.run(tts("Hello world", outfile=self.test_output_file))
        
        # Verify the function was called correctly
        mock_client.tts.audio.speech.assert_called_once()
        call_args = mock_client.tts.audio.speech.call_args
        
        # Check that the function returns True on success
        self.assertTrue(result)
        
        # Check that the output file was created
        self.assertTrue(os.path.exists(self.test_output_file))

    @patch('text_to_speech.Speechify')
    def test_tts_function_failure(self, mock_speechify):
        """Test TTS generation failure"""
        # Mock the Speechify client to raise an exception
        mock_client = MagicMock()
        mock_speechify.return_value = mock_client
        mock_client.tts.audio.speech.side_effect = Exception("API Error")
        
        # Test TTS generation
        result = asyncio.run(tts("Hello world", outfile=self.test_output_file))
        
        # Check that the function returns False on failure
        self.assertFalse(result)
        
        # Check that the output file was not created
        self.assertFalse(os.path.exists(self.test_output_file))

    def test_tts_missing_api_key(self):
        """Test TTS function with missing API key"""
        # Remove the API key
        if 'SPEECHIFY_API_KEY' in os.environ:
            del os.environ['SPEECHIFY_API_KEY']
        
        # Test that the function raises an error
        with self.assertRaises(ValueError):
            asyncio.run(tts("Hello world", outfile=self.test_output_file))

    @patch('voice_manager.Speechify')
    def test_voices_manager_creation(self, mock_speechify):
        """Test VoicesManager creation"""
        # Mock the Speechify client
        mock_client = MagicMock()
        mock_speechify.return_value = mock_client
        
        # Test VoicesManager creation
        voices_manager = VoicesManager()
        
        # Verify the client was created
        mock_speechify.assert_called_once_with(token='test_api_key_12345')
        self.assertEqual(voices_manager.client, mock_client)

    def test_voices_manager_missing_api_key(self):
        """Test VoicesManager creation with missing API key"""
        # Remove the API key
        if 'SPEECHIFY_API_KEY' in os.environ:
            del os.environ['SPEECHIFY_API_KEY']
        
        # Test that the VoicesManager raises an error
        with self.assertRaises(ValueError):
            VoicesManager()

    def test_filter_voice_models(self):
        """Test voice filtering functionality"""
        # Create mock voice objects
        mock_voice1 = MagicMock()
        mock_voice1.gender = 'male'
        mock_voice1.tags = ['timbre:deep']
        mock_model1 = MagicMock()
        mock_lang1 = MagicMock()
        mock_lang1.locale = 'en-US'
        mock_model1.languages = [mock_lang1]
        mock_voice1.models = [mock_model1]
        mock_model1.name = 'scott'
        
        mock_voice2 = MagicMock()
        mock_voice2.gender = 'female'
        mock_voice2.tags = ['timbre:bright']
        mock_model2 = MagicMock()
        mock_lang2 = MagicMock()
        mock_lang2.locale = 'fr-FR'
        mock_model2.languages = [mock_lang2]
        mock_voice2.models = [mock_model2]
        mock_model2.name = 'sarah'
        
        voices = [mock_voice1, mock_voice2]
        
        # Test filtering by gender
        male_voices = filter_voice_models(voices, gender='male')
        self.assertEqual(male_voices, ['scott'])
        
        # Test filtering by locale
        en_voices = filter_voice_models(voices, locale='en-US')
        self.assertEqual(en_voices, ['scott'])
        
        # Test filtering by tags
        deep_voices = filter_voice_models(voices, tags=['timbre:deep'])
        self.assertEqual(deep_voices, ['scott'])
        
        # Test filtering by multiple criteria
        male_en_voices = filter_voice_models(voices, gender='male', locale='en-US')
        self.assertEqual(male_en_voices, ['scott'])

    @patch('voice_manager.Speechify')
    def test_voices_manager_find(self, mock_speechify):
        """Test voice finding functionality"""
        # Mock the Speechify client and response
        mock_client = MagicMock()
        mock_speechify.return_value = mock_client
        
        mock_voice = MagicMock()
        mock_voice.gender = 'male'
        mock_voice.tags = []
        mock_model = MagicMock()
        mock_lang = MagicMock()
        mock_lang.locale = 'en-US'
        mock_model.languages = [mock_lang]
        mock_voice.models = [mock_model]
        mock_model.name = 'scott'
        
        mock_response = MagicMock()
        mock_response.voices = [mock_voice]
        mock_client.tts.voices.list.return_value = mock_response
        
        # Test voice finding
        voices_manager = VoicesManager()
        result = asyncio.run(VoicesManager.find(voices_manager, 'Male', 'en-US'))
        
        # Verify the result
        self.assertEqual(result['Name'], 'scott')

    def test_backward_compatibility(self):
        """Test backward compatibility with edge-tts voice format"""
        # Test that edge-tts voice names are properly converted
        edge_tts_voices = [
            "en-US-ChristopherNeural",
            "en-US-JennyNeural", 
            "en-GB-RyanNeural",
            "fr-FR-DeniseNeural",
            "de-DE-KatjaNeural"
        ]
        
        for voice in edge_tts_voices:
            # Should not raise any exceptions
            converted = convert_edge_tts_voice_to_speechify(voice)
            self.assertIsInstance(converted, str)
            self.assertIn(converted, ['scott', 'sarah'])

    def test_language_detection(self):
        """Test language detection for non-English content"""
        # Test English voices
        en_voices = ["en-US-ChristopherNeural", "en-GB-RyanNeural"]
        for voice in en_voices:
            lang = extract_language_from_voice(voice)
            self.assertTrue(lang.startswith('en'))
        
        # Test non-English voices
        non_en_voices = ["fr-FR-DeniseNeural", "de-DE-KatjaNeural", "es-ES-ElviraNeural"]
        for voice in non_en_voices:
            lang = extract_language_from_voice(voice)
            self.assertFalse(lang.startswith('en'))


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete migration"""

    def setUp(self):
        """Set up test environment"""
        os.environ['SPEECHIFY_API_KEY'] = 'test_api_key_12345'

    def test_import_compatibility(self):
        """Test that all modules can be imported without errors"""
        try:
            from src.text_to_speech import tts
            from src.voice_manager import VoicesManager
            from src.arg_parser import parse_args
            print("✓ All modules imported successfully")
        except ImportError as e:
            self.fail(f"Import failed: {e}")

    def test_environment_variables(self):
        """Test environment variable handling"""
        # Test with API key set
        self.assertIn('SPEECHIFY_API_KEY', os.environ)
        
        # Test with missing API key
        original_key = os.environ.get('SPEECHIFY_API_KEY')
        del os.environ['SPEECHIFY_API_KEY']
        
        with self.assertRaises(ValueError):
            VoicesManager()
        
        # Restore the key
        if original_key:
            os.environ['SPEECHIFY_API_KEY'] = original_key


def run_tests():
    """Run all tests"""
    print("Running Speechify Migration Tests...")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases using the newer TestLoader method
    loader = unittest.TestLoader()
    test_suite.addTest(loader.loadTestsFromTestCase(TestSpeechifyMigration))
    test_suite.addTest(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1) 