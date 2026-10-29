#include <bits/stdc++.h>
using namespace std;

int main() {
    int ops_cnt = 1e8;
    for (int merge_policy = 0; merge_policy <= 1; ++merge_policy) {
        system("rm -rf /tmp/rocks-level");
        string command =
            "db_bench"
            " --benchmarks=fillseq,compact"
            " --db=/tmp/rocks-level" 
            " --num=" + to_string(ops_cnt) +
            " --key_size=16"
            " --value_size=984"
            " --compaction_style=" + to_string(merge_policy) +
            " > out-" + to_string(merge_policy) + "-build.log 2>&1";
        system(command.c_str());
        int read_cnt=1e6;
            for (int threads_cnt = 4; threads_cnt <= 8; ++threads_cnt) {
                for (string test : {"readrandom", "readmissing"}) {
                        string out = test + "-" +
                            to_string(merge_policy) + "-" +
                            to_string(threads_cnt);

                        string command =
                            "db_bench"
                            " --benchmarks=" + test +
                            " --use_existing_db=1"
                            " --db=/tmp/rocks-level" 
                            " --num=" + to_string(ops_cnt) +
                            " --reads=" + std::to_string(read_cnt/threads_cnt) +
                            " --threads=" + to_string(threads_cnt) +
                            " --key_size=16"
                            " --value_size=984"
                            " --compaction_style=" + to_string(merge_policy) +
                            " > " + out + " 2>&1";

                        system(command.c_str());
                }
            }
    }
    system("rm -rf /tmp/rocks-level");
}
