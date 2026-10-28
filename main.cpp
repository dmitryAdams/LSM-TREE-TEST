#include "cstdlib"
#include "string"


int main(){
    for(int i = 1; i <= 8; ++i){
        for(int j = 0; j <= 1; ++j){
            std::string out = "out" +std::to_string(i) + "-" + std::to_string(j);
            std::string command = "db_bench >" + out + " --benchmarks=fillrandom --num=100000000 --db=/tmp/rocks-level --compaction_style="+std::to_string(j) + " --key_size=16 --value_size=984 --threads="+std::to_string(i);
            std::system(command.c_str());
            std::system("rm -rf /tmp/rocks-level");
        }
    }
}