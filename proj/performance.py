import sys
from markov import identify_speaker
import pandas as pd
from tabulate import tabulate
import time
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <max-k> <runs>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, max_k, runs = sys.argv[1:]
    max_k = int(max_k)
    runs = int(runs)
    use_hashtable = [True, False]

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


    data = {}
    data["Implementation"] = ["hashtable"] * max_k + ["dict"] * max_k
    data["K"] = []
    data["Total Runs"] = []
    data["Average Time"] = []


    for hash in use_hashtable:
        for k in range(1, max_k+1):

            total_time = 0

            for run in range(1, runs+1):
                start = time.perf_counter()
                markov_output = identify_speaker(fileA_text, fileB_text, fileC_text, k, hash)
                elapsed = time.perf_counter() - start

                total_time+=elapsed

            data["K"].append(k)
            data["Total Runs"].append(run)
            data["Average Time"].append(total_time / runs)

    df = pd.DataFrame(data)
    df.style.hide_index()
    print(tabulate(df, headers = 'keys', tablefmt = 'psql'))


    # TODO: write execution_graph.png

  
    # draw pointplot
    sns.pointplot(x = "K", y = "Average Time", hue = "Implementation", data = df, linestyles='-', markers='o').set(title='Hashtable vs. Python Dict')
    fig1 = plt.gcf()
    plt.show()
    fig1.savefig('execution_graph.png')


#python performance.py speeches/bush1+2.txt speeches/kerry1+2.txt speeches/bush-kerry3/BUSH-0.txt 2 1