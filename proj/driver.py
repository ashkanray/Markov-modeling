import sys
from markov import identify_speaker

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <k> <hashtable-or-dict>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, k, hashtable_or_dict = sys.argv[1:]
    k = int(k)
    if hashtable_or_dict not in ("hashtable", "dict"):
        print("Final parameter must either be 'hashtable' or 'dict'")
        sys.exit(1)

    try:
        with open (filenameA, 'r') as fileA:
            fileA_text = fileA.read()

        with open (filenameB, 'r') as fileB:
            fileB_text = fileB.read()

        with open (filenameC, 'r') as fileC:
            fileC_text = fileC.read()
    
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


    # TODO: add code to call identify_speaker & print results
    if hashtable_or_dict == "hashtable":
        markov_output = identify_speaker(fileA_text, fileB_text, fileC_text, k, True)
    else: 
        markov_output = identify_speaker(fileA_text, fileB_text, fileC_text, k, False)

    print("Speaker A: %f" %markov_output[0])
    print("Speaker B: %f" %markov_output[1])
    print("\nConclusion: Speaker %s is most likely" %markov_output[2])

    #python3 driver.py speeches/mccain1+2.txt speeches/obama1+2.txt speeches/obama-mccain3/OBAMA-0.txt 3 hashtable
    #python driver.py speeches/bush1+2.txt speeches/kerry1+2.txt speeches/bush-kerry3/BUSH-0.txt 2 hashtable