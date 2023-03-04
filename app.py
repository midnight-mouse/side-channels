import streamlit as st
import time

with open("code.txt") as f:
    code = f.read().strip()

# check function
def check_attempt(attempt):
    for i in range(len(code)):
        if code[i] != attempt[i]:
            return False
        
        time.sleep(0.03)
            
    return True

st.title("Timing Side Channel Attack")

st.write("The following piece of check function for a PIN is vulnerable to a time side channel attack.")

st.code("""
def check(attempt):
    for i in range(len(code)):
        if code[i] != attempt[i]:
            return False
        
        time.sleep(0.03)
            
    return True
""", language="python")

st.write("The function takes longer to evaluate for every correct digit. By comparing the time it takes to check a PIN attempt, an attacker could deduce if a digit is correct or not. ")
st.code("""
start = time.time()
check(attempt)
end = time.time()

if (end - start) > last_diff: # correct digit! Move on!
""", language="python")

st.write("")
code = st.text_input("Enter a PIN to be cracked:", placeholder="Ex. 937462")
st.write(f"Attempting to crack: {code}")

crack_btn = st.button("Crack")

if crack_btn:
    with st.empty():
        cracked = False

        attempt_list = ["0"] * len(code)

        # combination checker
        combination_checks = 0

        for i in range(len(code)):

            last_time = None

            if cracked:
                break

            for num in "01234567890":
                attempt_list[i] = str(num)
                attempt = ''.join(attempt_list)
                print(f"Testing {attempt}...")
                st.metric(f"Testing #{combination_checks}...", value=attempt)
                
                start = time.time()
                if check_attempt(attempt): 
                    cracked = True
                    st.metric(f"Cracked!", value=attempt)
                    break
                end = time.time()
                combination_checks += 1
                
                diff = end - start

                if last_time == None:
                    last_time = diff
                    continue
                    
                #print(f"\t{diff} vs {last_time}")
                #print(f"\t{round(diff, 2)} vs {round(last_time, 2)}")

                if round(diff, 3) > round(last_time, 3) + 0.025:
                    break

                last_time = diff

    if cracked:

        print()
        print("Cracked!")
        print(f"The code was {''.join(attempt_list)}")
        print()

        brute = str(10**len(code))
        print(f"Brute force Attempts : {brute} combinations")
        print(f"Side Channel Attempts: {str(combination_checks).ljust(len(brute))} combinations")

        st.write(f"**Brute force Attempts:** {brute} combinations")
        st.write(f"**Side Channel Attempts:** {str(combination_checks).ljust(len(brute))} combinations")
