import hashlib
import time

def hash_password(password):
    """Converts a password into its SHA-256 hash."""
    return hashlib.sha256(password.encode()).hexdigest()

def benchmark_hash_rate(attempts=10000):
    """Measures how long it takes to perform a number of SHA-256 hashes."""
    password = "testpassword"  # Test with a sample password
    start_time = time.time()
    
    for _ in range(attempts):
        hash_password(password)
    
    end_time = time.time()
    duration = end_time - start_time
    hashes_per_second = attempts / duration
    
    print(f"Hashed {attempts} passwords in {duration:.2f} seconds.")
    print(f"Hashing rate: {hashes_per_second:.2f} attempts per second.")
    
    return hashes_per_second

if __name__ == "__main__":
    benchmark_hash_rate()
