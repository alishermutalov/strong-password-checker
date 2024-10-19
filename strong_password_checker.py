def strong_password_checker(password: str) -> int:
    n = len(password)
    
    # Check if we have at least one lowercase, one uppercase, and one digit
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    # Count how many character types are missing
    missing_types = 3 - (has_lower + has_upper + has_digit)
    
    # Step 1: Handle length constraints
    if n < 6:
        # If the password is too short, the number of steps is the max of:
        # - Characters to add to reach 6
        # - Missing character types (we need to ensure the new characters also meet the type requirements)
        return max(missing_types, 6 - n)
    
    # Step 2: Identify repeated characters
    replace_count = 0  # Number of replacements to fix consecutive repeating characters
    one_mod = two_mod = 0  # To optimize replacements with deletions (used for long passwords)
    i = 2
    while i < n:
        if password[i] == password[i - 1] == password[i - 2]:
            length = 2
            while i < n and password[i] == password[i - 1]:
                length += 1
                i += 1
            
            # For repeated sequences of length L, we need L // 3 replacements
            replace_count += length // 3
            
            # To optimize, we classify the sequences into mod 3 cases (for deletion handling)
            if length % 3 == 0:
                one_mod += 1
            elif length % 3 == 1:
                two_mod += 1
        else:
            i += 1
    
    # Step 3: Handle long passwords (n > 20)
    if n > 20:
        # The number of deletions needed to get the password to length 20
        excess = n - 20
        
        # First delete from sequences that require 1 replacement (i.e., mod 3 == 0)
        replace_count -= min(excess, one_mod)
        # Then delete from sequences that require 2 replacements (i.e., mod 3 == 1)
        replace_count -= min(max(excess - one_mod, 0), two_mod * 2) // 2
        # Finally, delete from the remaining sequences
        replace_count -= max(excess - one_mod - 2 * two_mod, 0) // 3
        
        # Total steps: number of deletions + max of remaining replacements or missing character types
        return excess + max(missing_types, replace_count)
    
    # Step 4: Handle valid length (6 <= n <= 20)
    else:
        # If length is valid, the steps needed are the max of:
        # - The number of missing character types (lower, upper, digit)
        # - The replacements needed for repeated characters
        return max(missing_types, replace_count)


# Example usage:
password = "Baaabb0"
print(strong_password_checker(password))  # Output: 1