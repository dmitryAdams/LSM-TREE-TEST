#include "cstdlib"
#include "string"


int main(){
    int ops_cnt = 1e7;
    for(int threads_cnt = 1; threads_cnt <= 8; ++threads_cnt){
        for(int merge_policy = 0; merge_policy <= 1; ++merge_policy){
            std::string out = "out" +std::to_string(threads_cnt) + "-" + std::to_string(merge_policy);
            std::string command = "db_bench" \
                                   ">" + out +
                                   " --benchmarks=fillrandom" \
                                   " --db=/tmp/rocks-level"\
                                   " --key_size=16"\
                                   " --value_size=984"\
                                   " --num=" + std::to_string(ops_cnt / threads_cnt) +
                                   " --compaction_style="+std::to_string(merge_policy) +
                                   " --threads="+std::to_string(threads_cnt);
            std::system(command.c_str());
            std::system("rm -rf /tmp/rocks-level");
        }
    }
}