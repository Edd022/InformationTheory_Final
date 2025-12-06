"""
Test script for LZ78 Compressor
Tests all functionalities without GUI
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.model import LZ78Compressor, FileHandler


def test_compression():
    """Test compression functionality."""
    print("=" * 60)
    print("TEST 1: Compression")
    print("=" * 60)
    
    # Read test file
    file_handler = FileHandler()
    test_file = "test_sample.txt"
    
    try:
        text = file_handler.read_text_file(test_file)
        print(f"✓ Successfully read file: {test_file}")
        print(f"  Original text length: {len(text)} characters")
        print(f"  First 100 chars: {text[:100]}...")
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return False
    
    # Compress
    compressor = LZ78Compressor()
    try:
        compressed_data, dictionary = compressor.compress(text)
        print(f"\n✓ Successfully compressed file")
        print(f"  Dictionary size: {len(dictionary)} entries")
        print(f"  Compressed data length: {len(compressed_data)} tuples")
        print(f"  First 10 entries: {compressed_data[:10]}")
    except Exception as e:
        print(f"✗ Error compressing: {e}")
        return False
    
    # Get statistics
    stats = compressor.get_statistics(text)
    print(f"\n📊 Compression Statistics:")
    print(f"  Original size: {stats['original_size']} bytes")
    print(f"  Compressed size: {stats['compressed_size']} bytes")
    print(f"  Compression ratio: {stats['compression_ratio']}%")
    print(f"  Dictionary size: {stats['dictionary_size']} entries")
    
    return compressed_data, dictionary, text


def test_save_and_load():
    """Test saving and loading compressed files."""
    print("\n" + "=" * 60)
    print("TEST 2: Save and Load Compressed File")
    print("=" * 60)
    
    compressed_data, dictionary, original_text = test_compression()
    
    file_handler = FileHandler()
    compressed_file = "test_compressed.lz78"
    
    # Save compressed file
    try:
        file_handler.save_compressed_file(
            compressed_file,
            compressed_data,
            dictionary,
            "test_sample.txt"
        )
        print(f"\n✓ Successfully saved compressed file: {compressed_file}")
    except Exception as e:
        print(f"✗ Error saving compressed file: {e}")
        return False
    
    # Load compressed file
    try:
        loaded_data, loaded_dict, original_filename = file_handler.load_compressed_file(compressed_file)
        print(f"✓ Successfully loaded compressed file")
        print(f"  Original filename: {original_filename}")
        print(f"  Loaded dictionary size: {len(loaded_dict)} entries")
        print(f"  Loaded data length: {len(loaded_data)} tuples")
    except Exception as e:
        print(f"✗ Error loading compressed file: {e}")
        return False
    
    # Verify data integrity
    if loaded_data == compressed_data and loaded_dict == dictionary:
        print("✓ Data integrity verified - loaded data matches original")
    else:
        print("✗ Data integrity check failed")
        return False
    
    return loaded_data, loaded_dict, original_text


def test_decompression():
    """Test decompression functionality."""
    print("\n" + "=" * 60)
    print("TEST 3: Decompression")
    print("=" * 60)
    
    compressed_data, dictionary, original_text = test_save_and_load()
    
    # Decompress
    compressor = LZ78Compressor()
    try:
        decompressed_text = compressor.decompress(compressed_data, dictionary)
        print(f"\n✓ Successfully decompressed data")
        print(f"  Decompressed text length: {len(decompressed_text)} characters")
        print(f"  First 100 chars: {decompressed_text[:100]}...")
    except Exception as e:
        print(f"✗ Error decompressing: {e}")
        return False
    
    # Verify decompression
    if decompressed_text == original_text:
        print("\n✅ DECOMPRESSION VERIFICATION: SUCCESS")
        print("   Original and decompressed texts match perfectly!")
    else:
        print("\n❌ DECOMPRESSION VERIFICATION: FAILED")
        print(f"   Original length: {len(original_text)}")
        print(f"   Decompressed length: {len(decompressed_text)}")
        return False
    
    return True


def test_save_decompressed():
    """Test saving decompressed file."""
    print("\n" + "=" * 60)
    print("TEST 4: Save Decompressed File")
    print("=" * 60)
    
    # Get decompressed text
    compressed_file = "test_compressed.lz78"
    file_handler = FileHandler()
    
    compressed_data, dictionary, _ = file_handler.load_compressed_file(compressed_file)
    compressor = LZ78Compressor()
    decompressed_text = compressor.decompress(compressed_data, dictionary)
    
    # Save decompressed file
    output_file = "test_decompressed.txt"
    try:
        file_handler.save_text_file(output_file, decompressed_text)
        print(f"✓ Successfully saved decompressed file: {output_file}")
    except Exception as e:
        print(f"✗ Error saving decompressed file: {e}")
        return False
    
    # Verify saved file
    try:
        saved_text = file_handler.read_text_file(output_file)
        if saved_text == decompressed_text:
            print("✓ Saved file verification successful")
        else:
            print("✗ Saved file verification failed")
            return False
    except Exception as e:
        print(f"✗ Error verifying saved file: {e}")
        return False
    
    return True


def test_error_handling():
    """Test error handling."""
    print("\n" + "=" * 60)
    print("TEST 5: Error Handling")
    print("=" * 60)
    
    file_handler = FileHandler()
    
    # Test non-existent file
    print("\nTesting non-existent file...")
    try:
        file_handler.read_text_file("non_existent_file.txt")
        print("✗ Should have raised FileNotFoundError")
    except FileNotFoundError:
        print("✓ Correctly raised FileNotFoundError")
    except Exception as e:
        print(f"✗ Wrong exception: {e}")
    
    # Test invalid compressed file
    print("\nTesting invalid compressed file...")
    try:
        file_handler.load_compressed_file("test_sample.txt")
        print("✗ Should have raised ValueError")
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")
    except Exception as e:
        print(f"✗ Wrong exception: {e}")
    
    # Test empty file
    print("\nTesting empty file...")
    empty_file = "test_empty.txt"
    with open(empty_file, 'w') as f:
        f.write("")
    
    try:
        file_handler.read_text_file(empty_file)
        print("✗ Should have raised ValueError for empty file")
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")
    except Exception as e:
        print(f"✗ Wrong exception: {e}")
    
    # Clean up
    Path(empty_file).unlink(missing_ok=True)
    
    return True


def test_dictionary_structure():
    """Test dictionary structure and content."""
    print("\n" + "=" * 60)
    print("TEST 6: Dictionary Structure")
    print("=" * 60)
    
    compressor = LZ78Compressor()
    test_text = "abababcabcd"
    
    compressed_data, dictionary = compressor.compress(test_text)
    
    print(f"\nTest text: '{test_text}'")
    print(f"\nDictionary entries:")
    for phrase, index in sorted(dictionary.items(), key=lambda x: x[1]):
        print(f"  {index}: '{phrase}'")
    
    print(f"\nCompressed data (index, char):")
    for i, (idx, char) in enumerate(compressed_data):
        print(f"  {i+1}. ({idx}, '{char}')")
    
    # Verify decompression
    decompressed = compressor.decompress(compressed_data, dictionary)
    if decompressed == test_text:
        print(f"\n✓ Dictionary verification successful")
        print(f"  Original: '{test_text}'")
        print(f"  Decompressed: '{decompressed}'")
    else:
        print(f"✗ Dictionary verification failed")
        return False
    
    return True


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "LZ78 COMPRESSOR - TEST SUITE" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    tests = [
        ("Compression", test_compression),
        ("Save and Load", test_save_and_load),
        ("Decompression", test_decompression),
        ("Save Decompressed", test_save_decompressed),
        ("Error Handling", test_error_handling),
        ("Dictionary Structure", test_dictionary_structure),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result or result is None:
                passed += 1
            else:
                failed += 1
                print(f"\n❌ {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"\n❌ {test_name} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests: {len(tests)}")
    print(f"✓ Passed: {passed}")
    print(f"✗ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\nThe LZ78 compressor is working correctly!")
        print("\nYou can now run the GUI application:")
        print("  python main.py")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
    
    # Clean up test files
    print("\n" + "=" * 60)
    print("Cleaning up test files...")
    test_files = ["test_compressed.lz78", "test_decompressed.txt", "test_empty.txt"]
    for f in test_files:
        if Path(f).exists():
            Path(f).unlink()
            print(f"  Removed: {f}")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
