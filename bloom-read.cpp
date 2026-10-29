#include "cstdlib"
#include "string"


int main(){
    int ops_cnt = 1e8;
    for(auto bloom_bits_cnt: {0, 5, 10, 15, 20}){
                std::string command1 = "db_bench" \
                                    "> /dev/null" \
                                    " --benchmarks=fillseq,compact" \
                                    " --db=/tmp/rocks-level"\
                                    " --key_size=16"\
                                    " --value_size=984"\
                                    " --num=" + std::to_string(ops_cnt) +
                                    " --bloom_bits=" + std::to_string(bloom_bits_cnt);
                std::system(command1.c_str());
                std::string out = "out_readrandom"+std::to_string(ops_cnt) + "-" + std::to_string(bloom_bits_cnt);
                std::string command = "db_bench" \
                                    ">" + out +
                                    " --benchmarks=readmissing" \
                                    "--use_existing_db=1" \
                                    " --db=/tmp/rocks-level"\
                                    " --key_size=16"\
                                    " --value_size=984"\
                                    " --num=" + std::to_string(ops_cnt) +
                                    " --bloom_bits=" + std::to_string(bloom_bits_cnt);
                std::system(command.c_str());
                std::system("rm -rf /tmp/rocks-level");
        }

}